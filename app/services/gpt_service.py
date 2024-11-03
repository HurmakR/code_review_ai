from typing import Dict, Optional, List
import httpx
from fastapi import HTTPException, status
import logging
from app.core.config import settings
import openai
import json

logger = logging.getLogger(__name__)

openai.api_key = settings.openai_api_key

class GPTService:
    async def analyze_code(self, code_files: List[Dict[str, str]], assignment_description: str, candidate_level: str) -> Optional[Dict[str,str]]:
        file_contents = await self.fetch_file_contents(code_files)
        prompt = self.create_prompt(file_contents, assignment_description, candidate_level)

        try:
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful code review assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            if response.choices[0].message.content is not None:
                return json.loads(response.choices[0].message.content)
            else:
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
                    response = await client.get(file['url'])
                    response.raise_for_status()
                    file_contents[file['name']] = response.text
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
        return file_contents

    def create_prompt(self, file_contents: Dict[str, str], assignment_description: str, candidate_level: str) -> str:
        files_text = '\\n'.join([f"### {name}\\n{content}" for name, content in file_contents.items()])
        prompt = (
            f"Task description: {assignment_description}\\n"
            f"Candidate level: {candidate_level}\\n"
            f"\\nFiles for analysis:\\n{files_text}\\n"
            f"\\nPlease provide your response in the following JSON format:\\n"
            f"{{\\n"
            f"  \"comments\": \"<detailed comments on the code>\",\\n"
            f"  \"rating\": \"<rating on a scale of 1 to 5>\",\\n"
            f"  \"conclusion\": \"<summary conclusion based on the rating and comments>\"\\n"
            f"}}"
        )
        return prompt

    def parse_response(self, response_content: str) -> Dict[str, str]:
        # Parse response to extract comments, rating, and conclusion
        sections = response_content.split('\n\n')
        comments = sections[0] if len(sections) > 0 else "No comments provided."
        rating = "Pending"  # Default value if not found
        conclusion = "Review completed"  # Default value if not found

        for section in sections:
            if "Rating:" in section:
                rating = section.split("Rating:")[-1].strip()
            if "Conclusion:" in section:
                conclusion = section.split("Conclusion:")[-1].strip()

        return {
            "comments": comments,
            "rating": rating,
            "conclusion": conclusion
        }