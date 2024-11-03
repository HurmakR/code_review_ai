from typing import Dict, Optional, List
import httpx
from fastapi import HTTPException, status
import logging
from app.core.config import settings
import openai
import json
from app.services.cache_service import CacheService

logger = logging.getLogger(__name__)

openai.api_key = settings.openai_api_key

cache_service = CacheService(settings.redis_url)

class GPTService:
    async def analyze_code(self, code_files: List[Dict[str, str]], assignment_description: str, candidate_level: str) -> Optional[Dict[str, str]]:
        cache_key = f"{assignment_description}:{candidate_level}:{str(code_files)}"

        logger.debug(f"Generated cache key: {cache_key}")
        cached_result = await cache_service.get(cache_key)
        if cached_result:
            logger.info("Cache hit, returning cached result.")
            return json.loads(cached_result)

        logger.info("Cache miss, fetching file contents.")
        file_contents = await self.fetch_file_contents(code_files)
        prompt = self.create_prompt(file_contents, assignment_description, candidate_level)
        logger.debug(f"Generated prompt: {prompt}")

        try:
            logger.info("Sending request to OpenAI API.")
            response = openai.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful code review assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            logger.info("Received response from OpenAI API.")
            if response.choices[0].message.content is not None:
                try:
                    result = json.loads(response.choices[0].message.content)
                    logger.debug(f"Decoded response: {result}")
                    await cache_service.set(cache_key, json.dumps(result))
                    logger.info("Result cached successfully.")
                    return result
                except json.JSONDecodeError as e:
                    logger.error(f"JSON decoding error: {e}")
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Failed to decode response content from OpenAI."
                    )
            else:
                logger.warning("The response content is None.")
                raise ValueError("The response content is None")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred while processing the code analysis."
            )

    async def fetch_file_contents(self, code_files: List[Dict[str, str]]) -> Dict[str, str]:
        file_contents = {}
        async with httpx.AsyncClient() as client:
            for file in code_files:
                try:
                    logger.info(f"Fetching content for file: {file['name']}")
                    response = await client.get(file['url'])
                    response.raise_for_status()
                    file_contents[file['name']] = response.text
                    logger.debug(f"Content for {file['name']} fetched successfully.")
                except httpx.HTTPStatusError as e:
                    logger.error(f"Error fetching file {file['name']}: {e}")
                    raise HTTPException(
                        status_code=e.response.status_code,
                        detail=f"Error fetching file {file['name']}: {e.response.text}"
                    )
                except Exception as e:
                    logger.error(f"Unexpected error while fetching file {file['name']}: {e}")
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"An unexpected error occurred while fetching file {file['name']}."
                    )
        logger.info("All file contents fetched successfully.")
        return file_contents

    def create_prompt(self, file_contents: Dict[str, str], assignment_description: str, candidate_level: str) -> str:
        files_text = '\n'.join([f"### {name}\n{content}" for name, content in file_contents.items()])
        prompt = (
            f"Task description: {assignment_description}\n"
            f"Candidate level: {candidate_level}\n"
            f"\nFiles for analysis:\n{files_text}\n"
            f"\nPlease provide your response in the following JSON format:\n"
            f"{{\n"
            f"  \"comments\": \"<detailed comments on the code>\",\n"
            f"  \"rating\": \"<rating on a scale of 1 to 5> out of 5\",\n"
            f"  \"conclusion\": \"<summary conclusion based on the rating and comments>\"\n"
            f"}}"
        )
        logger.debug(f"Prompt created successfully.")
        return prompt
