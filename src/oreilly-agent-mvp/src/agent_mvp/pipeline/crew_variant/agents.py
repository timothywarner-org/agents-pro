"""
CrewAI agent definitions for PM, Dev, and QA roles.

Each agent class encapsulates the role, goal, and backstory that
CrewAI uses to shape the LLM's behavior. These are reusable across
different orchestration patterns.
"""

from __future__ import annotations

from typing import Optional

from crewai import Agent, LLM

from ...config import get_config, LLMProvider


# =============================================================================
# Agent Definitions
# =============================================================================


class PMAgent:
    """Product Manager agent that analyzes issues and creates plans."""

    ROLE = "Product Manager"
    GOAL = "Analyze GitHub issues and create clear, actionable implementation plans"
    BACKSTORY = """You are a seasoned Product Manager with experience in software development.
You excel at breaking down feature requests into clear requirements and actionable plans.
You focus on user value and practical implementation paths."""

    @classmethod
    def create(cls, llm: Optional[LLM] = None) -> Agent:
        """Create the PM agent instance."""
        return Agent(
            role=cls.ROLE,
            goal=cls.GOAL,
            backstory=cls.BACKSTORY,
            llm=llm or get_crew_llm(),
            verbose=True,
            allow_delegation=False,
        )


class DevAgent:
    """Developer agent that implements features."""

    ROLE = "Senior Developer"
    GOAL = "Implement features with clean, tested code"
    BACKSTORY = """You are a Senior Developer with strong coding skills.
You write practical, maintainable code and always include tests.
You focus on getting things done right the first time."""

    @classmethod
    def create(cls, llm: Optional[LLM] = None) -> Agent:
        """Create the Dev agent instance."""
        return Agent(
            role=cls.ROLE,
            goal=cls.GOAL,
            backstory=cls.BACKSTORY,
            llm=llm or get_crew_llm(),
            verbose=True,
            allow_delegation=False,
        )


class QAAgent:
    """QA Engineer agent that reviews implementations."""

    ROLE = "QA Engineer"
    GOAL = "Ensure implementations meet requirements and identify issues"
    BACKSTORY = """You are a thorough QA Engineer who catches bugs others miss.
You verify implementations against acceptance criteria.
You provide clear, actionable feedback."""

    @classmethod
    def create(cls, llm: Optional[LLM] = None) -> Agent:
        """Create the QA agent instance."""
        return Agent(
            role=cls.ROLE,
            goal=cls.GOAL,
            backstory=cls.BACKSTORY,
            llm=llm or get_crew_llm(),
            verbose=True,
            allow_delegation=False,
        )


# =============================================================================
# LLM Configuration
# =============================================================================


def get_crew_llm() -> LLM:
    """Get the LLM configured for CrewAI.

    CrewAI uses its own LLM wrapper with provider prefixes.
    """
    config = get_config()

    if config.llm_provider == LLMProvider.ANTHROPIC:
        return LLM(
            model=f"anthropic/{config.llm_model}",
            temperature=config.llm_temperature,
            api_key=config.anthropic_api_key,
        )
    elif config.llm_provider == LLMProvider.OPENAI:
        kwargs = {
            "model": f"openai/{config.llm_model}",
            "temperature": config.llm_temperature,
            "api_key": config.openai_api_key,
        }
        if config.openai_base_url:
            kwargs["base_url"] = config.openai_base_url
        return LLM(**kwargs)
    elif config.llm_provider == LLMProvider.AZURE:
        return LLM(
            model=f"azure/{config.azure_openai_deployment}",
            temperature=config.llm_temperature,
            api_key=config.azure_openai_api_key,
            base_url=config.azure_openai_endpoint,
        )
    else:
        raise ValueError(f"Unsupported LLM provider: {config.llm_provider}")
