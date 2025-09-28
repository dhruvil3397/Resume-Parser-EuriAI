"""
Euriai LLM configuration.
- Provides a singleton EuriaiCrewAI instance.
- Reads EURIAI_API_KEY from environment.
- MODEL is the default model used across agents.
"""

import os
from typing import Optional
from euriai.crewai import EuriaiCrewAI

# Default model used across the app; make it configurable via env override.
MODEL: str = os.getenv("EURIAI_MODEL", "gpt-4.1-nano")

# Internal singleton holder
_CREW_SINGLETON: Optional[EuriaiCrewAI] = None


def _debug_enabled() -> bool:
    """
    Enable debug logs if EURIAI_DEBUG is set to a truthy value.
    """
    return os.getenv("EURIAI_DEBUG", "").lower() in {"1", "true", "yes", "on"}


def _build_crew(api_key: str, model: str) -> EuriaiCrewAI:
    """
    Construct a EuriaiCrewAI instance with provided credentials and model.
    """
    if _debug_enabled():
        print(f"[euriai] init: model={model}, api_key_present={'YES' if bool(api_key) else 'NO'}")
    return EuriaiCrewAI(api_key=api_key, default_model=model)


def get_crew() -> EuriaiCrewAI:
    """
    Return the global EuriaiCrewAI instance (lazy-initialized).

    Raises:
        RuntimeError: If EURIAI_API_KEY is not set.
    """
    global _CREW_SINGLETON
    if _CREW_SINGLETON is not None:
        return _CREW_SINGLETON

    api_key = os.getenv("EURIAI_API_KEY")
    if not api_key:
        raise RuntimeError("EURIAI_API_KEY environment variable not set.")

    _CREW_SINGLETON = _build_crew(api_key=api_key, model=MODEL)
    return _CREW_SINGLETON


# Backwards-compatible alias for existing imports
crew = get_crew()
