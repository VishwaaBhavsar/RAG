"""Core configuration models and loaders.

Purpose:
    Define the typed config objects used by the core container and load them from YAML plus env vars.

Responsibilities:
    - Represent provider selections in a typed, framework-owned way.
    - Parse startup config from YAML and environment variables using pydantic-settings.
    - Merge tenant overrides over base config in a validated way.

Usage example:
    app_config = AppConfig.load(Path("config/base.yaml"))
    tenant_config = merge_tenant_config(app_config, {"llm": {"provider": "ollama"}})
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, cast

from pydantic import BaseModel, ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_settings.sources import YamlConfigSettingsSource


class _ConfigFields:
    """Shared configuration fields for base and tenant config models."""

    llm: ProviderSelection
    embedding: ProviderSelection
    vectordb: ProviderSelection
    loader: ProviderSelection | None = None
    tools: tuple[ProviderSelection, ...] = ()
    reranker: ProviderSelection | None = None
    memory: ProviderSelection | None = None


class ProviderSelection(BaseModel):
    """A selected provider name for a single component slot."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    provider: str


class TenantConfig(_ConfigFields, BaseModel):
    """Typed tenant configuration used by the DI container."""

    model_config = ConfigDict(extra="forbid", frozen=True)


class TenantConfigPatch(BaseModel):
    """Partial tenant configuration used for override merges."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    llm: ProviderSelection | None = None
    embedding: ProviderSelection | None = None
    vectordb: ProviderSelection | None = None
    loader: ProviderSelection | None = None
    tools: tuple[ProviderSelection, ...] | None = None
    reranker: ProviderSelection | None = None
    memory: ProviderSelection | None = None


class AppConfig(_ConfigFields, BaseSettings):
    """Base application configuration loaded from YAML and environment variables."""

    model_config = SettingsConfigDict(
        env_prefix="RAG_FRAMEWORK_",
        env_nested_delimiter="__",
        env_ignore_empty=True,
        extra="forbid",
        frozen=True,
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings,
        env_settings,
        dotenv_settings,
        file_secret_settings,
    ):
        """Add YAML configuration as a lower-priority source than env vars."""

        yaml_source = YamlConfigSettingsSource(
            settings_cls,
            yaml_file=cls.model_config.get("yaml_file"),
            yaml_file_encoding=cls.model_config.get("yaml_file_encoding"),
        )
        return init_settings, env_settings, yaml_source, dotenv_settings, file_secret_settings

    @classmethod
    def load(cls, yaml_file: Path | None = None) -> "AppConfig":
        """Load app config from YAML and env vars."""

        settings_cls = _settings_class_for_yaml(cls, yaml_file)
        return cast("AppConfig", settings_cls())


class ConfigLoaderError(Exception):
    """Raised when configuration loading or merging fails."""


def merge_tenant_config(
    base_config: AppConfig,
    tenant_override: TenantConfigPatch | Mapping[str, Any] | None,
) -> TenantConfig:
    """Merge a tenant override over the loaded base config."""

    if tenant_override is None:
        return TenantConfig.model_validate(base_config.model_dump(mode="python"))

    override_model = (
        tenant_override
        if isinstance(tenant_override, TenantConfigPatch)
        else TenantConfigPatch.model_validate(tenant_override)
    )
    merged_data = base_config.model_dump(mode="python")
    merged_data.update(override_model.model_dump(exclude_unset=True, mode="python"))
    return TenantConfig.model_validate(merged_data)


def load_app_config(yaml_file: Path | None = None) -> AppConfig:
    """Load base app config from YAML and env vars."""

    return AppConfig.load(yaml_file=yaml_file)


def _settings_class_for_yaml(
    settings_cls: type[AppConfig],
    yaml_file: Path | None,
) -> type[AppConfig]:
    """Create a settings subclass with the configured YAML file baked in."""

    model_config = SettingsConfigDict(
        env_prefix=settings_cls.model_config.get("env_prefix", "RAG_FRAMEWORK_"),
        env_nested_delimiter=settings_cls.model_config.get("env_nested_delimiter", "__"),
        env_ignore_empty=settings_cls.model_config.get("env_ignore_empty", True),
        extra=settings_cls.model_config.get("extra", "forbid"),
        frozen=True,
        yaml_file=yaml_file,
        yaml_file_encoding="utf-8",
    )
    runtime_cls = cast(
        type[AppConfig],
        type(f"{settings_cls.__name__}Runtime", (settings_cls,), {"model_config": model_config}),
    )
    return runtime_cls
