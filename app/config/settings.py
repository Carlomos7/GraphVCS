import os
from pathlib import Path
from typing import Type, Optional, Union, Dict
#from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    # Application Info
    APP_NAME: str = "graphvcs"
    APP_VERSION: str = "0.1.0"

    # Paths
    BASE_DIR: Path = Path.cwd()
    LOGS_DIR: Path = Field(default_factory=lambda: Path.cwd() / ".gvcs" / "logs")

    # Repository Settings
    REPO_DIR_NAME: str = ".gvcs"
    OBJECTS_DIR_NAME: str = "objects"
    REFS_DIR_NAME: str = "refs"

    # Neo4j settings
    NEO4J_URI: Optional[str] = None
    NEO4J_USERNAME: Optional[str] = None
    NEO4J_PASSWORD: Optional[str] = None

    # Default user info
    DEFAULT_USER_NAME: Optional[str] = None
    DEFAULT_USER_EMAIL: Optional[str] = None

    # Logging Settings
    LOG_LEVEL: str = "INFO"
    DEBUG: bool = False
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Content Storage Settings
    COMPRESSION_ENABLED: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="GRAPHVCS_",
        #case_sensitive=True,
    )

    def get_repo_path(self, base_path: Optional[Union[str, Path]] = None) -> Path:
        """Get the repository path."""
        base = Path(base_path) if base_path else self.BASE_DIR
        return base / self.REPO_DIR_NAME

    def get_objects_path(self, base_path: Optional[Union[str, Path]] = None) -> Path:
        """Get the objects path."""
        repo_path = self.get_repo_path(base_path)
        return repo_path / self.OBJECTS_DIR_NAME

    def get_refs_path(self, base_path: Optional[Union[str, Path]] = None) -> Path:
        """Get the refs path."""
        repo_path = self.get_repo_path(base_path)
        return repo_path / self.REFS_DIR_NAME


class DevSettings(Settings):
    """Development settings."""

    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG"
    NEO4J_URI: str = "neo4j://localhost:7687"


class TestSettings(Settings):
    """Test settings."""

    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG"
    NEO4J_URI: str = "neo4j://localhost:7687"


class ProdSettings(Settings):
    """Production settings."""

    NEO4J_URI: str
    LOG_LEVEL: str = "INFO"


"""@lru_cache()
def get_settings() -> Type[BaseSettings]:
    #Get the settings class based on the environment.
    env = os.getenv("ENVIRONMENT", "DEVELOPMENT")
    if env == "DEVELOPMENT":
        return DevSettings
    if env == "TEST":
        return TestSettings
    if env == "PRODUCTION":
        return ProdSettings
    raise ValueError("Invalid environment setting.")"""

environments: Dict[str, Type[Settings]] = {
    "DEVELOPMENT": DevSettings,
    "TEST": TestSettings,
    "PRODUCTION": ProdSettings,
}


def get_settings() -> Settings:
    """Get the settings instance based on the environment."""
    env = os.getenv("ENVIRONMENT", "DEVELOPMENT")
    return environments.get(env, DevSettings)()


settings = get_settings()