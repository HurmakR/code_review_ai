from typing import List, Dict
import httpx
from pydantic_core import Url

from app.core.config import settings
from fastapi import HTTPException
import asyncio

class GitHubService:
    def __init__(self) -> None:
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {settings.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }

    async def get_repository_contents(self, repo_url: str) -> List[Dict[str, str]]:
        repo_path = repo_url.replace("https://github.com/", "")
        url = f"{self.base_url}/repos/{repo_path}/contents"
        print(url)
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=self.headers)
                response.raise_for_status()
                print(response)
                return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise HTTPException(status_code=401, detail="Unauthorized: Please check your GitHub token.")
            raise HTTPException(status_code=e.response.status_code, detail=f"GitHub API error: {e}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

#async def main():
#    gitdata = GitHubService()
#    await gitdata.get_repository_contents('https://github.com/HurmakR/BB_Rosan')
#
#asyncio.run(main())