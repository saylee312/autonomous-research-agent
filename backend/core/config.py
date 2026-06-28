from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    GROQ_API_KEY: str

    MONGO_URI: str

    DB_NAME: str

    CHROMA_DB_PATH: str

    TAVILY_API_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()