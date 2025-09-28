from .llm_config import crew


def _truncate(text: str, limit: int) -> str:
    """
    Truncate text to a character limit and append ellipsis if needed.
    """
    return text if len(text) <= limit else f"{text[:limit]}..."


def _add_task(task_id: str, description: str, expected_output: str, agent_name: str) -> None:
    """
    Centralized task registration to keep shape consistent.
    """
    crew.add_task(
        task_id,
        {
            "description": description,
            "expected_output": expected_output,
            "agent": agent_name,
        },
    )


def parse_resume_task(agent_name: str, raw_resume_text: str):
    """
    Create a parsing task that cleans resume text and normalizes structure.

    Returns:
        crew instance for chaining
    """
    truncated_text = _truncate(raw_resume_text, 1500)
    description = (
        "Clean this resume text quickly:\n\n"
        f"{truncated_text}\n\n"
        "Remove artifacts, normalize bullets to '-', keep all content. Be fast and direct."
    )
    _add_task(
        "resume_parsing_specialist_task",
        description,
        "Clean resume text with proper structure.",
        agent_name,
    )
    return crew


def rewrite_for_ats_task(agent_name: str, cleaned_text: str, job_title: str, job_description: str):
    """
    Create a rewriting task to optimize a resume for ATS against a target job.

    Returns:
        crew instance for chaining
    """
    truncated_resume = _truncate(cleaned_text, 1200)
    truncated_jd = _truncate(job_description, 300)
    description = (
        f"Rewrite resume for {job_title}:\n\n"
        f"JOB: {truncated_jd}\n\n"
        f"RESUME: {truncated_resume}\n\n"
        "Match keywords, use action verbs, add metrics. Target 80+ ATS score. Be direct and fast."
    )
    _add_task(
        "ats_writer_specialist_task",
        description,
        "ATS-optimized resume with keyword placement and metrics.",
        agent_name,
    )
    return crew


def refine_bullets_task(agent_name: str, rewritten_text: str):
    """
    Create a refinement task to polish bullet points with strong verbs and metrics.

    Returns:
        crew instance for chaining
    """
    truncated_text = _truncate(rewritten_text, 1000)
    description = (
        f"Polish these bullets with action verbs and metrics:\n\n{truncated_text}\n\n"
        "Add strong verbs and numbers. Be fast and direct."
    )
    _add_task(
        "bullet_refiner_specialist_task",
        description,
        "Refined resume.",
        agent_name,
    )
    return crew


def evaluate_ats_task(agent_name: str, final_text: str, job_title: str, job_description: str):
    """
    Create an evaluation task to score ATS fit and produce a JSON report.

    Returns:
        crew instance for chaining
    """
    truncated_resume = _truncate(final_text, 800)
    truncated_jd = _truncate(job_description, 200)
    description = (
        f"Score this resume for {job_title}:\n\n"
        f"JOB: {truncated_jd}\n\n"
        f"RESUME: {truncated_resume}\n\n"
        "Rate 1-5: keywords, structure, metrics, verbs, format. "
        "Return JSON with overall_score (0-100), breakdown, missing_keywords, quick_wins."
    )
    _add_task(
        "ats_evaluator_specialist_task",
        description,
        "JSON evaluation.",
        agent_name,
    )
    return crew
