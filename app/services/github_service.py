import json
from typing import List, Dict
import httpx
from fastapi import HTTPException, status
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)


class GitHubService:
    BASE_URL = "https://api.github.com"

    def __init__(self) -> None:
        self.headers = {
            "Authorization": f"token {settings.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }

    async def get_default_branch(self, repo_url: str) -> str:
        """Fetches the default branch of the repository."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.BASE_URL}/repos/{repo_url}", headers=self.headers)
                response.raise_for_status()
                repo_info = response.json()
                return repo_info.get('default_branch', 'main')  # Default to 'main' if not found
        except httpx.HTTPStatusError as e:
            logger.error(f"Error fetching repository information: {e}")
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Error fetching repository information: {e.response.text}"
            )
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred while fetching repository information."
            )

    async def get_repository_contents(self, repo_url: str, path: str = "") -> List[Dict[str, str]]:
        all_files = []
        readable_extensions = ('.py', '.js', '.txt', '.json', '.html', '.yml', 'md')
        try:
            # Get the default branch of the repository
            default_branch = await self.get_default_branch(repo_url)

            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.BASE_URL}/repos/{repo_url}/contents/{path}?ref={default_branch}",
                                            headers=self.headers)
                response.raise_for_status()
                contents = response.json()
                for item in contents:
                    if item['type'] == 'file' and any(item['name'].endswith(ext) for ext in readable_extensions):
                        # Append files with downloadable link to the result list if they have a readable extension
                        all_files.append({
                            'name': item['path'],
                            'url': f'https://raw.githubusercontent.com/{repo_url}/refs/heads/{default_branch}/{item['path']}'
                        })
                    elif item['type'] == 'dir' and item['name'] != '__pycache__':
                        # Recursively fetch the contents of subdirectories, excluding __pycache__
                        subdir_files = await self.get_repository_contents(repo_url, item['path'])
                        all_files.extend(subdir_files)
                return all_files

        except httpx.HTTPStatusError as e:
            logger.error(f"Error fetching repository contents: {e}")
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Error fetching repository contents: {e.response.text}"
            )
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred while fetching repository contents."
            )

