import numpy as np
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger("resumeiq.semantic")

_EMBEDDING_MODEL_INSTANCE = None


def get_embedding_model():
    """Lazy singleton initializer for local fastembed TextEmbedding (BGE-small)."""
    global _EMBEDDING_MODEL_INSTANCE
    if _EMBEDDING_MODEL_INSTANCE is None:
        try:
            from fastembed import TextEmbedding
            # BAAI/bge-small-en-v1.5 has 384 dimensions and runs fast on CPU via ONNX Runtime
            _EMBEDDING_MODEL_INSTANCE = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
            logger.info("Initialized local BGE-small fastembed model.")
        except Exception as e:
            logger.warning(f"Could not load fastembed: {e}. Falling back to deterministic n-gram vectorizer.")
            _EMBEDDING_MODEL_INSTANCE = None
    return _EMBEDDING_MODEL_INSTANCE


def cosine_similarity(v1: np.ndarray, v2: np.ndarray) -> float:
    """Computes cosine similarity between two 1D vectors."""
    dot = np.dot(v1, v2)
    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return float(dot / (norm1 * norm2))


class SemanticMatcher:
    """Computes dense vector semantic relevance using local BGE-small embeddings."""

    @classmethod
    def match(
        cls,
        resume_chunks: List[str],
        jd_requirements: List[str]
    ) -> Dict[str, Any]:
        if not resume_chunks or not jd_requirements:
            return {
                "score": 0.0,
                "matches": [],
                "average_similarity": 0.0
            }

        model = get_embedding_model()

        if model is not None:
            # Generate embeddings with fastembed
            try:
                resume_embeddings = list(model.embed(resume_chunks))
                jd_embeddings = list(model.embed(jd_requirements))
            except Exception as e:
                logger.error(f"Error during embedding generation: {e}")
                return cls._fallback_tfidf_matching(resume_chunks, jd_requirements)
        else:
            return cls._fallback_tfidf_matching(resume_chunks, jd_requirements)

        matches: List[Dict[str, Any]] = []
        similarities: List[float] = []

        for j_idx, req in enumerate(jd_requirements):
            req_vec = np.array(jd_embeddings[j_idx])
            best_sim = -1.0
            best_chunk = ""

            for r_idx, chunk in enumerate(resume_chunks):
                chunk_vec = np.array(resume_embeddings[r_idx])
                sim = cosine_similarity(req_vec, chunk_vec)
                if sim > best_sim:
                    best_sim = sim
                    best_chunk = chunk

            similarities.append(max(0.0, best_sim))

            matches.append({
                "requirement": req,
                "best_matching_resume_snippet": best_chunk[:200] if best_chunk else "",
                "similarity": round(max(0.0, best_sim), 3),
                "is_semantically_aligned": best_sim >= 0.65
            })

        avg_similarity = float(np.mean(similarities)) if similarities else 0.0
        # Scale to 0-100: cosine similarity in BGE typically ranges 0.40 - 0.90 for related text
        scaled_score = min(100.0, max(0.0, ((avg_similarity - 0.35) / 0.50) * 100.0))

        return {
            "score": round(scaled_score, 1),
            "average_similarity": round(avg_similarity, 3),
            "matches": sorted(matches, key=lambda x: x["similarity"], reverse=True)
        }

    @classmethod
    def _fallback_tfidf_matching(cls, resume_chunks: List[str], jd_requirements: List[str]) -> Dict[str, Any]:
        """Deterministic TF-IDF fallback if fastembed is unavailable."""
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity as sk_cosine

        all_texts = resume_chunks + jd_requirements
        vectorizer = TfidfVectorizer(stop_words="english")
        tfidf_matrix = vectorizer.fit_transform(all_texts)

        resume_vecs = tfidf_matrix[:len(resume_chunks)]
        jd_vecs = tfidf_matrix[len(resume_chunks):]

        sim_matrix = sk_cosine(jd_vecs, resume_vecs)

        matches = []
        max_sims = []
        for i, req in enumerate(jd_requirements):
            row = sim_matrix[i]
            best_idx = int(row.argmax())
            best_sim = float(row[best_idx])
            max_sims.append(best_sim)
            matches.append({
                "requirement": req,
                "best_matching_resume_snippet": resume_chunks[best_idx][:200],
                "similarity": round(best_sim, 3),
                "is_semantically_aligned": best_sim >= 0.35
            })

        avg_sim = float(np.mean(max_sims)) if max_sims else 0.0
        scaled_score = min(100.0, avg_sim * 100.0)

        return {
            "score": round(scaled_score, 1),
            "average_similarity": round(avg_sim, 3),
            "matches": sorted(matches, key=lambda x: x["similarity"], reverse=True)
        }
