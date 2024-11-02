from typing import Dict, Optional
import openai
from app.core.config import settings

openai.api_key = settings.openai_api_key


class GPTService:
    async def analyze_code(self, code_files: Dict[str, str], assignment_description: str, candidate_level: str) -> Optional[str]:
        prompt = self.create_prompt(code_files, assignment_description, candidate_level)

        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful code review assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    def create_prompt(self, code_files: Dict[str, str], assignment_description: str, candidate_level: str) -> str:
        return f"Task description: {assignment_description}\nCandidate level: {candidate_level}\nКод:\n{code_files}"
