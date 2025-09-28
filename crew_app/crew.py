# crew_app/crew.py

from typing import Tuple
from .agents import (
    build_parser_agent,
    build_ats_writer_agent,
    build_refiner_agent,
    build_evaluator_agent,
)
from .tasks import (
    parse_resume_task,
    rewrite_for_ats_task,
    refine_bullets_task,
    evaluate_ats_task,
)
from .llm_config import crew


def _run_and_get_text(task_crew) -> str:
    """
    Execute the crew pipeline for the given task and return stripped text.
    """
    result = task_crew.run()
    return str(result).strip()


def _reset_crew() -> None:
    """
    Reset the shared crew instance to clear previous task context.
    """
    crew.reset()


def run_pipeline(raw_resume_text: str, job_title: str, job_description: str) -> Tuple[str, str, str, str]:
    """
    End-to-end pipeline:
    1) Parse raw resume text.
    2) Rewrite for ATS against target job.
    3) Refine bullet points.
    4) Evaluate ATS fit.

    Returns:
        A tuple of strings: (cleaned, rewritten, refined, evaluated_json)
    """
    # Parse
    parser_id = build_parser_agent()
    parse_task = parse_resume_task(parser_id, raw_resume_text)
    cleaned = _run_and_get_text(parse_task)
    _reset_crew()

    # Rewrite
    writer_id = build_ats_writer_agent()
    rewrite_task = rewrite_for_ats_task(writer_id, cleaned, job_title, job_description)
    rewritten = _run_and_get_text(rewrite_task)
    _reset_crew()

    # Refine bullets
    refiner_id = build_refiner_agent()
    refine_task = refine_bullets_task(refiner_id, rewritten)
    refined = _run_and_get_text(refine_task)
    _reset_crew()

    # Evaluate
    evaluator_id = build_evaluator_agent()
    evaluate_task = evaluate_ats_task(evaluator_id, refined, job_title, job_description)
    evaluated = _run_and_get_text(evaluate_task)
    _reset_crew()

    return cleaned, rewritten, refined, evaluated
