import re
from typing import Dict, Any, List
from rank_bm25 import BM25Okapi


class BM25Matcher:
    """Okapi BM25 information retrieval engine for ranking resume sections against JD requirements."""

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        tokens = re.findall(r"\b[a-zA-Z0-9+#.-]+\b", text.lower())
        return [t for t in tokens if len(t) > 1 or t in ["c", "r"]]

    @classmethod
    def match(
        cls,
        resume_sections: Dict[str, str],
        jd_requirements: List[str],
        jd_responsibilities: List[str]
    ) -> Dict[str, Any]:
        corpus_docs: List[Dict[str, Any]] = []
        tokenized_corpus: List[List[str]] = []

        for section_name, text in resume_sections.items():
            if not text.strip():
                continue
            lines = [l.strip() for l in text.splitlines() if len(l.strip()) > 20]
            if lines:
                for line in lines:
                    tokens = cls._tokenize(line)
                    if tokens:
                        tokenized_corpus.append(tokens)
                        corpus_docs.append({
                            "section": section_name,
                            "text": line
                        })
            else:
                tokens = cls._tokenize(text)
                if tokens:
                    tokenized_corpus.append(tokens)
                    corpus_docs.append({
                        "section": section_name,
                        "text": text[:300]
                    })

        if not tokenized_corpus:
            return {
                "score": 0.0,
                "top_passages": [],
                "query_scores": {}
            }

        bm25 = BM25Okapi(tokenized_corpus)

        all_queries = jd_requirements + jd_responsibilities
        if not all_queries:
            all_queries = ["software engineer requirements"]

        query_scores: Dict[str, float] = {}
        top_passages: List[Dict[str, Any]] = []
        total_score_sum = 0.0

        for query in all_queries:
            q_tokens = cls._tokenize(query)
            if not q_tokens:
                continue

            doc_scores = bm25.get_scores(q_tokens)
            max_score = float(max(doc_scores)) if len(doc_scores) > 0 else 0.0
            query_scores[query] = round(max_score, 2)
            total_score_sum += max_score

            # Capture top matching passage if score is positive
            if max_score > 0.0:
                best_idx = int(doc_scores.argmax())
                best_doc = corpus_docs[best_idx]
                if not any(p["text"] == best_doc["text"] for p in top_passages):
                    top_passages.append({
                        "query": query,
                        "matched_section": best_doc["section"],
                        "score": round(max_score, 2),
                        "text": best_doc["text"]
                    })

        avg_score = total_score_sum / max(1, len(all_queries))
        normalized = min(100.0, max(0.0, (avg_score / 10.0) * 100.0))

        return {
            "score": round(normalized, 1),
            "top_passages": top_passages[:8],
            "query_scores": query_scores
        }
