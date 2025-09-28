from typing import Dict
from .llm_config import crew, MODEL


def _add_agent(agent_id: str, config: Dict) -> str:
    """
    Register an agent with the shared crew instance and return its identifier.

    Args:
        agent_id: Unique identifier for the agent inside the crew.
        config: Agent configuration including role, goal, backstory, and model params.

    Returns:
        The same agent_id for downstream reference.
    """
    crew.add_agent(agent_id, config)
    return agent_id


def build_parser_agent() -> str:
    """
    Build and register the resume parsing agent.

    Returns:
        Agent id: "resume_parsing_specialist"
    """
    return _add_agent(
        "resume_parsing_specialist",
        {
            "role": "Resume Parsing Specialist",
            "goal": "Extract clean, structured text from a resume suitable for ATS optimization.",
            "backstory": (
                "You efficiently clean resume text by removing artifacts and normalizing formatting. "
                "Focus on speed and accuracy - preserve all important content while removing noise."
            ),
            "model": MODEL,
            "temperature": 0.0,
            "max_tokens": 500,
            "max_iter": 1,
            "max_execution_time": 120,
        },
    )


def build_ats_writer_agent() -> str:
    """
    Build and register the ATS optimization writing agent.

    Returns:
        Agent id: "ats_optimization_writer"
    """
    return _add_agent(
        "ats_optimization_writer",
        {
            "role": "ATS Optimization Writer",
            "goal": "Create a high-scoring ATS-optimized resume that matches job requirements perfectly.",
            "backstory": (
                "You are an expert at transforming resumes into ATS-friendly formats that score 80+ points. "
                "You strategically place keywords, use strong action verbs, and quantify all achievements. "
                "You work quickly and deliver results that pass ATS systems."
            ),
            "model": MODEL,
            "temperature": 0.3,
            "max_tokens": 500,
            "max_iter": 1,
            "max_execution_time": 120,
        },
    )


def build_evaluator_agent() -> str:
    """
    Build and register the ATS evaluator agent.

    Returns:
        Agent id: "ats_evaluator"
    """
    return _add_agent(
        "ats_evaluator",
        {
            "role": "ATS Evaluator",
            "goal": "Provide accurate ATS scores and actionable improvement recommendations.",
            "backstory": (
                "You are a precise ATS scoring expert who quickly identifies gaps and provides specific, "
                "actionable recommendations. You focus on keyword density, section structure, and measurable achievements."
            ),
            "model": MODEL,
            "temperature": 0.0,
            "max_tokens": 500,
            "max_iter": 1,
            "max_execution_time": 120,
        },
    )


def build_refiner_agent() -> str:
    """
    Build and register the bullet point refiner agent.

    Returns:
        Agent id: "bullet_point_refiner"
    """
    return _add_agent(
        "bullet_point_refiner",
        {
            "role": "Bullet Point Refiner",
            "goal": "Transform bullet points into high-impact, ATS-optimized statements with strong metrics.",
            "backstory": (
                "You excel at creating powerful bullet points that combine action verbs, specific achievements, "
                "and quantified results. You work efficiently to maximize impact."
            ),
            "model": MODEL,
            "temperature": 0.2,
            "max_tokens": 500,
            "max_iter": 1,
            "max_execution_time": 120,
        },
    )
