"""
Configuración centralizada del backend.
Lee las variables desde el archivo .env usando pydantic-settings.
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Todas las variables de configuración del proyecto."""

    SECRET_KEY: str = "clave_por_defecto_solo_para_desarrollo"
    DATABASE_URL: str = "sqlite:///./funeraria.db"
    CORS_ORIGINS: str = "http://127.0.0.1:5500,http://localhost:5500"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

    @property
    def cors_origins_list(self) -> list[str]:
        """Convierte la cadena de orígenes en una lista."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


# Instancia global (se importa en otros módulos)
settings = Settings()
