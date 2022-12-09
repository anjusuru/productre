from pydantic import BaseSettings, PostgresDsn, validator, AnyHttpUrl
from typing import Optional, Any, Dict, List, Union


class Settings(BaseSettings):
    PROJECT_NAME: str
    API_V1_STR: str = "/api/v1"

    # Database Configuration
    POSTGRES_SERVER: str
    POSTGRES_PORT: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_SCHEMA: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn | str] = None
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    # @validator("BACKEND_CORS_ORIGINS", pre=True)
    # def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
    #     if isinstance(v, str) and not v.startswith("["):
    #         return [i.strip() for i in v.split(",")]
    #     elif isinstance(v, (list, str)):
    #         return v
    #     raise ValueError(v)

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:

        return PostgresDsn.build(
            scheme="postgresql+psycopg2",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER", ""),
            port=values.get("POSTGRES_PORT"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
