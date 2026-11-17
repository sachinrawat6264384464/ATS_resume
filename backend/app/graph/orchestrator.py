import logging
from langgraph.graph import StateGraph, START, END
from app.graph.state import ATSGraphState
from app.agents.resume_parser_agent import ResumeParserAgent
from app.agents.jd_analyzer_agent import JDAnalyzerAgent
from app.agents.skill_intelligence_agent import SkillIntelligenceAgent
from app.agents.matching_agent import MatchingAgent
from app.agents.scoring_agent import ScoringAgent
from app.agents.resume_improvement_agent import ResumeImprovementAgent
from app.agents.validation_agent import ValidationAgent
from app.agents.report_generation_agent import ReportGenerationAgent

logger = logging.getLogger("resumeiq.orchestrator")


def validation_router(state: ATSGraphState) -> str:
    """Conditional router based on validation checks."""
    validation = state.get("validation_result", {})
    if validation.get("is_valid", True):
        return "generate_report"
    else:
        logger.warning(f"Validation failed with issues: {validation.get('issues')}")
        return "error_node"


def error_node(state: ATSGraphState) -> dict:
    """Handles failed validation gracefully."""
    issues = state.get("validation_result", {}).get("issues", ["Unknown validation issue."])
    return {
        "processing_status": "failed",
        "errors": state.get("errors", []) + issues,
        "stage": "Validation Check Failed",
        "progress_percentage": 100
    }


def build_ats_graph():
    """Constructs the deterministic LangGraph pipeline for ATS resume analysis."""
    workflow = StateGraph(ATSGraphState)

    # Add Nodes
    workflow.add_node("parse_resume", ResumeParserAgent.execute)
    workflow.add_node("analyze_jd", JDAnalyzerAgent.execute)
    workflow.add_node("skill_intelligence", SkillIntelligenceAgent.execute)
    workflow.add_node("match_engines", MatchingAgent.execute)
    workflow.add_node("calculate_scores", ScoringAgent.execute)
    workflow.add_node("formulate_improvements", ResumeImprovementAgent.execute)
    workflow.add_node("validate_results", ValidationAgent.execute)
    workflow.add_node("generate_report", ReportGenerationAgent.execute)
    workflow.add_node("error_node", error_node)

    # Define Linear Flow
    workflow.add_edge(START, "parse_resume")
    workflow.add_edge("parse_resume", "analyze_jd")
    workflow.add_edge("analyze_jd", "skill_intelligence")
    workflow.add_edge("skill_intelligence", "match_engines")
    workflow.add_edge("match_engines", "calculate_scores")
    workflow.add_edge("calculate_scores", "formulate_improvements")
    workflow.add_edge("formulate_improvements", "validate_results")

    # Conditional Branching after validation
    workflow.add_conditional_edges(
        "validate_results",
        validation_router,
        {
            "generate_report": "generate_report",
            "error_node": "error_node"
        }
    )

    workflow.add_edge("generate_report", END)
    workflow.add_edge("error_node", END)

    return workflow.compile()


ats_pipeline = build_ats_graph()

