from pydantic import BaseSettings

class Settings(BaseSettings):# type: ignore
    openai_api_key: str
    github_token: str

    class Config:
        env_file = ".env"

settings = Settings()
