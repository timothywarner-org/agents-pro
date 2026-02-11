"""
Configuration management for the agent MVP.

Loads settings from environment variables with sensible defaults.
Supports Anthropic, OpenAI (including DeepSeek), and Azure OpenAI providers.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


class LLMProvider(str, Enum):
    """Supported LLM providers."""
    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    AZURE = "azure"


@dataclass
class Config:
    """Application configuration loaded from environment."""

    # LLM settings
    llm_provider: LLMProvider = LLMProvider.ANTHROPIC
    llm_model: str = "claude-sonnet-4-20250514"
    llm_temperature: float = 0.2

    # Provider-specific credentials
    anthropic_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    openai_base_url: Optional[str] = None  # For OpenAI-compatible APIs (DeepSeek, etc.)
    azure_openai_endpoint: Optional[str] = None
    azure_openai_api_key: Optional[str] = None
    azure_openai_deployment: Optional[str] = None
    azure_openai_api_version: str = "2024-02-15-preview"

    # Runtime settings
    watch_poll_seconds: int = 3
    checkpoint_path: Optional[Path] = None
    log_level: str = "INFO"

    # Directories (relative to project root)
    project_root: Path = field(default_factory=Path.cwd)
    incoming_dir: Path = field(init=False)
    processed_dir: Path = field(init=False)
    outgoing_dir: Path = field(init=False)
    mock_issues_dir: Path = field(init=False)

    def __post_init__(self):
        """Set up derived paths."""
        self.incoming_dir = self.project_root / "incoming"
        self.processed_dir = self.project_root / "processed"
        self.outgoing_dir = self.project_root / "outgoing"
        self.mock_issues_dir = self.project_root / "mock_issues"

    @classmethod
    def from_env(cls, project_root: Optional[Path] = None) -> Config:
        """Load configuration from environment variables."""
        # Load .env file if present
        if project_root:
            env_path = project_root / ".env"
        else:
            env_path = Path.cwd() / ".env"

        # override=True forces .env to override system env vars
        load_dotenv(env_path, override=True)

        # Parse provider
        provider_str = os.getenv("LLM_PROVIDER", "anthropic").lower()
        try:
            provider = LLMProvider(provider_str)
        except ValueError:
            provider = LLMProvider.ANTHROPIC

        # Parse checkpoint path
        checkpoint_str = os.getenv("LANGGRAPH_CHECKPOINT_PATH", "")
        checkpoint_path = Path(checkpoint_str) if checkpoint_str else None

        # Determine default model based on provider
        default_models = {
            LLMProvider.ANTHROPIC: "claude-sonnet-4-20250514",
            LLMProvider.OPENAI: "gpt-4o",
            LLMProvider.AZURE: os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o"),
        }

        return cls(
            llm_provider=provider,
            llm_model=os.getenv("LLM_MODEL", default_models[provider]),
            llm_temperature=float(os.getenv("LLM_TEMPERATURE", "0.2")),
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            openai_base_url=os.getenv("OPENAI_BASE_URL"),
            azure_openai_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            azure_openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_openai_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            azure_openai_api_version=os.getenv(
                "AZURE_OPENAI_API_VERSION", "2024-02-15-preview"
            ),
            watch_poll_seconds=int(os.getenv("WATCH_POLL_SECONDS", "3")),
            checkpoint_path=checkpoint_path,
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            project_root=project_root or Path.cwd(),
        )

    def get_llm(self):
        """Create and return the configured LLM instance."""
        if self.llm_provider == LLMProvider.ANTHROPIC:
            if not self.anthropic_api_key:
                raise ValueError(
                    "ANTHROPIC_API_KEY not set. "
                    "Please set it in your .env file or environment."
                )
            from langchain_anthropic import ChatAnthropic
            return ChatAnthropic(
                model=self.llm_model,
                temperature=self.llm_temperature,
                api_key=self.anthropic_api_key,
            )

        elif self.llm_provider == LLMProvider.OPENAI:
            if not self.openai_api_key:
                raise ValueError(
                    "OPENAI_API_KEY not set. "
                    "Please set it in your .env file or environment."
                )
            from langchain_openai import ChatOpenAI
            kwargs = {
                "model": self.llm_model,
                "temperature": self.llm_temperature,
                "api_key": self.openai_api_key,
            }
            # Add base_url for OpenAI-compatible APIs (DeepSeek, etc.)
            if self.openai_base_url:
                kwargs["base_url"] = self.openai_base_url
            return ChatOpenAI(**kwargs)

        elif self.llm_provider == LLMProvider.AZURE:
            if not all([
                self.azure_openai_endpoint,
                self.azure_openai_api_key,
                self.azure_openai_deployment,
            ]):
                raise ValueError(
                    "Azure OpenAI credentials not complete. "
                    "Set AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, "
                    "and AZURE_OPENAI_DEPLOYMENT in your .env file."
                )
            from langchain_openai import AzureChatOpenAI
            return AzureChatOpenAI(
                azure_endpoint=self.azure_openai_endpoint,
                api_key=self.azure_openai_api_key,
                azure_deployment=self.azure_openai_deployment,
                api_version=self.azure_openai_api_version,
                temperature=self.llm_temperature,
            )

        raise ValueError(f"Unknown LLM provider: {self.llm_provider}")

    def validate(self) -> list[str]:
        """Validate the configuration and return any issues."""
        errors = []

        # Check provider credentials
        if self.llm_provider == LLMProvider.ANTHROPIC and not self.anthropic_api_key:
            errors.append("ANTHROPIC_API_KEY is required when using Anthropic provider")
        elif self.llm_provider == LLMProvider.OPENAI and not self.openai_api_key:
            errors.append("OPENAI_API_KEY is required when using OpenAI provider")
        elif self.llm_provider == LLMProvider.AZURE:
            if not self.azure_openai_endpoint:
                errors.append("AZURE_OPENAI_ENDPOINT is required for Azure provider")
            if not self.azure_openai_api_key:
                errors.append("AZURE_OPENAI_API_KEY is required for Azure provider")
            if not self.azure_openai_deployment:
                errors.append("AZURE_OPENAI_DEPLOYMENT is required for Azure provider")

        # Check directories exist
        for dir_name, dir_path in [
            ("incoming", self.incoming_dir),
            ("processed", self.processed_dir),
            ("outgoing", self.outgoing_dir),
        ]:
            if not dir_path.exists():
                errors.append(f"Directory does not exist: {dir_path}")

        return errors


# Global config instance - lazy loaded
_config: Optional[Config] = None


def get_config() -> Config:
    """Get the global configuration instance."""
    global _config
    if _config is None:
        _config = Config.from_env()
    return _config


def reset_config():
    """Reset the global config (useful for testing)."""
    global _config
    _config = None
