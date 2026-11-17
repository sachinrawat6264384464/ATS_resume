import re
from typing import Dict, List, Set, Tuple, Optional


class SkillTaxonomy:
    """Canonical skill taxonomy, category hierarchy, alias dictionary, and relationship map."""

    # 1. Taxonomy: Canonical Name -> Category
    TAXONOMY: Dict[str, str] = {
        # Programming Languages
        "python": "Programming Languages",
        "javascript": "Programming Languages",
        "typescript": "Programming Languages",
        "java": "Programming Languages",
        "c++": "Programming Languages",
        "c#": "Programming Languages",
        "c": "Programming Languages",
        "go": "Programming Languages",
        "rust": "Programming Languages",
        "ruby": "Programming Languages",
        "php": "Programming Languages",
        "swift": "Programming Languages",
        "kotlin": "Programming Languages",
        "scala": "Programming Languages",
        "r": "Programming Languages",
        "dart": "Programming Languages",
        "sql": "Programming Languages",
        "html5": "Programming Languages",
        "css3": "Programming Languages",
        "shell": "Programming Languages",
        "powershell": "Programming Languages",

        # Frontend Frameworks & Libraries
        "react": "Frontend",
        "next.js": "Frontend",
        "vue.js": "Frontend",
        "angular": "Frontend",
        "svelte": "Frontend",
        "tailwind css": "Frontend",
        "bootstrap": "Frontend",
        "redux": "Frontend",
        "zustand": "Frontend",
        "graphql": "Frontend",
        "html/css": "Frontend",

        # Backend Frameworks & Runtimes
        "fastapi": "Backend",
        "django": "Backend",
        "flask": "Backend",
        "node.js": "Backend",
        "express.js": "Backend",
        "nest.js": "Backend",
        "spring boot": "Backend",
        "asp.net core": "Backend",
        "ruby on rails": "Backend",
        "gin": "Backend",
        "actix": "Backend",
        "restful api": "Backend",
        "grpc": "Backend",
        "websockets": "Backend",

        # Databases & Storage
        "postgresql": "Databases",
        "mysql": "Databases",
        "sqlite": "Databases",
        "mongodb": "Databases",
        "redis": "Databases",
        "cassandra": "Databases",
        "elasticsearch": "Databases",
        "neo4j": "Databases",
        "dynamodb": "Databases",
        "pgvector": "Databases",
        "snowflake": "Databases",
        "bigquery": "Databases",

        # Cloud & DevOps
        "docker": "Cloud & DevOps",
        "kubernetes": "Cloud & DevOps",
        "aws": "Cloud & DevOps",
        "google cloud platform": "Cloud & DevOps",
        "microsoft azure": "Cloud & DevOps",
        "terraform": "Cloud & DevOps",
        "ansible": "Cloud & DevOps",
        "ci/cd": "Cloud & DevOps",
        "github actions": "Cloud & DevOps",
        "gitlab ci": "Cloud & DevOps",
        "jenkins": "Cloud & DevOps",
        "linux": "Cloud & DevOps",
        "nginx": "Cloud & DevOps",

        # Data, AI & Machine Learning
        "machine learning": "Data & AI",
        "deep learning": "Data & AI",
        "nlp": "Data & AI",
        "llm": "Data & AI",
        "rag": "Data & AI",
        "langchain": "Data & AI",
        "langgraph": "Data & AI",
        "pytorch": "Data & AI",
        "tensorflow": "Data & AI",
        "scikit-learn": "Data & AI",
        "pandas": "Data & AI",
        "numpy": "Data & AI",
        "apache spark": "Data & AI",
        "apache kafka": "Data & AI",
        "celery": "Data & AI",
        "airflow": "Data & AI",

        # Architecture & Methodologies
        "microservices": "Architecture",
        "distributed systems": "Architecture",
        "system design": "Architecture",
        "event-driven architecture": "Architecture",
        "agile / scrum": "Architecture",
        "test-driven development": "Architecture",
        "domain-driven design": "Architecture"
    }

    # 2. Aliases -> Canonical Name
    ALIASES: Dict[str, str] = {
        "py": "python",
        "python3": "python",
        "js": "javascript",
        "es6": "javascript",
        "ts": "typescript",
        "golang": "go",
        "cpp": "c++",
        "csharp": "c#",
        "reactjs": "react",
        "react.js": "react",
        "next": "next.js",
        "nextjs": "next.js",
        "vue": "vue.js",
        "vuejs": "vue.js",
        "tailwind": "tailwind css",
        "tailwindcss": "tailwind css",
        "postgres": "postgresql",
        "psql": "postgresql",
        "mongo": "mongodb",
        "k8s": "kubernetes",
        "gcp": "google cloud platform",
        "amazon web services": "aws",
        "azure": "microsoft azure",
        "github action": "github actions",
        "ml": "machine learning",
        "natural language processing": "nlp",
        "large language models": "llm",
        "retrieval augmented generation": "rag",
        "spark": "apache spark",
        "kafka": "apache kafka",
        "rest": "restful api",
        "rest api": "restful api",
        "rest apis": "restful api",
        "tdd": "test-driven development",
        "agile": "agile / scrum",
        "scrum": "agile / scrum"
    }

    # 3. Related Skills Graph (Canonical -> Set of related Canonical skills)
    RELATED_SKILLS: Dict[str, List[str]] = {
        "fastapi": ["django", "flask", "python", "restful api"],
        "django": ["fastapi", "flask", "python"],
        "flask": ["fastapi", "django", "python"],
        "react": ["next.js", "vue.js", "angular", "typescript"],
        "vue.js": ["react", "angular", "javascript"],
        "angular": ["react", "vue.js", "typescript"],
        "postgresql": ["mysql", "sqlite", "sql", "pgvector"],
        "mysql": ["postgresql", "sqlite", "sql"],
        "mongodb": ["dynamodb", "cassandra", "redis"],
        "docker": ["kubernetes", "ci/cd", "linux"],
        "kubernetes": ["docker", "terraform", "aws", "cloud & devops"],
        "aws": ["google cloud platform", "microsoft azure", "cloud & devops"],
        "google cloud platform": ["aws", "microsoft azure"],
        "pytorch": ["tensorflow", "scikit-learn", "deep learning"],
        "tensorflow": ["pytorch", "scikit-learn", "deep learning"],
        "apache kafka": ["rabbitmq", "celery", "distributed systems", "event-driven architecture"],
        "celery": ["redis", "apache kafka", "python"]
    }

    @classmethod
    def normalize_skill(cls, term: str) -> Tuple[str, str]:
        """Normalizes a raw skill string to (canonical_name, category)."""
        cleaned = term.strip().lower()
        cleaned = re.sub(r"^[^\w+#.-]+|[^\w+#.-]+$", "", cleaned).strip()

        # Direct alias check
        if cleaned in cls.ALIASES:
            canonical = cls.ALIASES[cleaned]
            return canonical, cls.TAXONOMY.get(canonical, "Technical Skills")

        # Direct taxonomy check
        if cleaned in cls.TAXONOMY:
            return cleaned, cls.TAXONOMY[cleaned]

        # Check punctuation variations (e.g. "react-js" -> "react")
        sub_cleaned = cleaned.replace("-", " ").replace(".", "")
        if sub_cleaned in cls.ALIASES:
            canonical = cls.ALIASES[sub_cleaned]
            return canonical, cls.TAXONOMY.get(canonical, "Technical Skills")

        # Fallback to title-cased term
        return cleaned, "Technical Skills"

    @classmethod
    def get_related_skills(cls, canonical_name: str) -> List[str]:
        return cls.RELATED_SKILLS.get(canonical_name, [])

