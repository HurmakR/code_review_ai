import pytest
from unittest.mock import patch, AsyncMock
from app.services.gpt_service import GPTService


@pytest.mark.asyncio
async def test_analyze_code_success():
    gpt_service = GPTService()
    code_files = [{'name': 'test_file.py', 'content': 'print("Hello World")'}]
    assignment_description = "Sample assignment"
    candidate_level = "Junior"

    mock_openai_response = {
        "choices": [
            {
                "message": {
                    "content": '{"comments": "Well-structured code", "rating": "3 out of 5", "conclusion": "Good job with some areas for improvement"}'
                }
            }
        ]
    }

    with patch('openai.chat.completions.create', return_value=AsyncMock(**mock_openai_response)) as mock_openai:
        result = await gpt_service.analyze_code(code_files, assignment_description, candidate_level)

        # Check the actual output against the expected output
        assert result == {
            "comments": "Well-structured code",
            "rating": "3 out of 5",
            "conclusion": "Good job with some areas for improvement"
        }

        mock_openai.assert_called_once()


