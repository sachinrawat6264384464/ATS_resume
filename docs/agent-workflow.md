# ResumeIQ — Multi-Agent LangGraph Workflow

## 1. Overview & Architectural Philosophy

ResumeIQ organizes its ATS analysis as a distributed multi-agent state graph orchestrated with **LangGraph `StateGraph`**.

Unlike conventional generative AI wrappers that send entire resumes to an LLM prompt, ResumeIQ assigns discrete tasks to **8 deterministic Python agents**. Generative models are never utilized for calculating scores or extracting facts, guaranteeing mathematical reproducibility, explainability, and elimination of hallucinations.

---

## 2. Shared Typed Graph State (`ATSGraphState`)

All agents read from and mutate a strictly typed state dictionary:

```python
class ATSGraphState(TypedDict):
    analysis_id: str
    resume_id: str
    job_id: str
    resume_file: str
    resume_text: str
    parsed_resume: Dict[str, Any]
    job_description: str
    parsed_job: Dict[str, Any]
    normalized_skills: List[Dict[str, Any]]
    keyword_matches: Dict[str, Any]
    semantic_matches: Dict[str, Any]
    bm25_matches: Dict[str, Any]
    experience_analysis: Dict[str, Any]
    scoring_result: Dict[str, Any]
    recommendations: List[Dict[str, Any]]
    validation_result: Dict[str, Any]
    final_report: Dict[str, Any]
    errors: List[str]
    processing_status: str
```

---

## 3. Agent Responsibilities & Tools

### Agent 1: Resume Parser Agent (`resume_parser`)
- **Responsibility**: Ingests document bytes from `/uploads`, uses geometry-aware PyMuPDF/python-docx parsers, detects 9 distinct resume sections, and extracts contact info, experience, education, and skills.
- **Tools**: PyMuPDF (`fitz`), `python-docx`, SectionDetector, Regex heuristics.

### Agent 2: Job Description Analyzer Agent (`jd_analyzer`)
- **Responsibility**: Parses job postings, extracting required skills, preferred skills, minimum experience years, education prerequisites, responsibilities, and qualifications.
- **Tools**: Tokenizers, requirement pattern extractors, qualification hierarchy lookup.

### Agent 3: Skill Intelligence Agent (`skill_intelligence`)
- **Responsibility**: Normalizes extracted skills into canonical forms using a curated 500+ skill taxonomy and alias dictionary (e.g. `k8s` -> `Kubernetes`, `react.js` -> `React`). Identifies related skill clusters for partial credit.
- **Tools**: `SkillTaxonomy` graph, regex word-boundary matchers.

### Agent 4: Matching Agent (`matching_engine`)
- **Responsibility**: Runs multi-pronged matching:
  1. *Exact Keyword Matcher*: Regex boundary matching.
  2. *BM25 Ranking*: Okapi BM25 scores across resume sections against JD requirements.
  3. *Dense Vector Embeddings*: BGE-small embeddings via `fastembed` with ONNX CPU runtime and cosine similarity.
  4. *Overlapping Experience Matcher*: Chronological timeline parser with interval deduplication (ensuring concurrent jobs are not double-counted).
  5. *Evidence Classifier*: Classifies evidence into `demonstrated_in_experience`, `demonstrated_in_projects`, `mentioned_in_skills`, or `missing`.
- **Tools**: `rank-bm25`, `fastembed`, `scikit-learn`, `dateutil`.

### Agent 5: Scoring Agent (`scoring_engine`)
- **Responsibility**: Applies the versioned heuristic scoring equation:
  $$\text{ATS Score} = (S_{\text{keyword}} \times 0.40) + (S_{\text{semantic}} \times 0.25) + (S_{\text{experience}} \times 0.20) + (S_{\text{project}} \times 0.10) + (S_{\text{education}} \times 0.05)$$
  Isolates mandatory missing skills so critical gaps cannot be obscured by a high aggregate score.
- **Tools**: Deterministic score calculation formula.

### Agent 6: Resume Improvement Agent (`resume_improvement`)
- **Responsibility**: Identifies weak action verbs and missing keywords. Generates concrete, fact-preserving bullet enhancements. Strictly adheres to non-hallucination rules (never invents unverified achievements, employers, or metrics).
- **Tools**: Action verb taxonomy, keyword gap injector.

### Agent 7: Validation Agent (`validation_agent`)
- **Responsibility**: Audits mathematical outputs:
  - Verifies score components sum to overall score within floating-point tolerance ($\epsilon < 0.05$).
  - Validates that evidence snippets are present in original resume text.
  - Flags missing mandatory requirements.
- **Tools**: State auditor, mathematical validator.

### Agent 8: Report Generation Agent (`report_generation`)
- **Responsibility**: Serializes analysis results into standard JSON format, prepares UI dashboard schemas, and ensures ReportLab PDF export compatibility.
- **Tools**: Pydantic models, ReportLab PDF builder.

---

## 4. Conditional Edge & Error Recovery

```python
def validate_results_edge(state: ATSGraphState) -> str:
    validation = state.get("validation_result", {})
    if validation.get("is_valid", False):
        return "valid"
    return "invalid"
```

If validation fails, the workflow branches to `error_remediation`, logging diagnostic errors and updating `ProcessingJob` state rather than failing silently.
