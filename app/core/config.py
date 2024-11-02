from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()
class Settings(BaseSettings):
    openai_api_key: Optional[str] = None
    github_token: Optional[str] = None

    class Config:
        env_file = os.path.join(os.path.dirname(__file__), '..', '..', '.env')


settings = Settings()
