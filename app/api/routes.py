from fastapi import APIRouter, HTTPException, status
from typing import Dict, List, Union
from app.services.github_service import GitHubService
from app.services.gpt_service import GPTService
from app.models.request_models import ReviewRequest
from app.models.response_models import ReviewResult

router = APIRouter()
github_service = GitHubService()
gpt_service = GPTService()


@router.post("/review", response_model=ReviewResult)
async def review(request: ReviewRequest) -> Dict[str, Union[str, List[str]]]:
    try:
        repo_url = request.github_repo_url.split("github.com/")[-1]
        code_files = await github_service.get_repository_contents(repo_url)
        print('gitfiles received')
        analysis_result ={'comments': "The code looks rather decent but there are some issues noted that need to be improved on:\n\n 1. Comments are not in English - it's important to keep comments in English as programming is universally done in English.\n\n 2. General organization and structure of the code can be improved. The Python code should be refactored for better organization and easy navigation. For instance, the `app.py` has a `/result` route that is very long and does a lot of things, this hinders readability and testability.\n\n 3. Error handling - currently, the code does not handle for errors such as file not found or csv reading errors.\n\n 4. For the `app.py`, the use of hardcoded string is rampant and might pose a problem when these strings need to be updated or they are reused across other part of the application. You can declare them as constants at the top of your file.\n\n 5. Unit tests are missing - Unit tests help ensure every part of the code behaves as expected and makes debugging easier by narrowing down the list of changes that could have caused the bug.\n\n 6. In `gsx2.py`, the code opens a csv file `gsx = open(values['file2'], encoding='Windows-1251')` but does not ensure to close it. It's better to use `with open...` which automatically closes the file.\n\n 7. The application doesn't look like it can download GitHub repositories, as the task description requested.", 'rating': '2', 'conclusion': "The code generally needs more refinement in several areas: structure, error handling, usage of constants, closing opened files and adding unit tests. It also seems that the code's functionality does not align with the provided task description."}
                          #await gpt_service.analyze_code(code_files, request.assignment_description,
                          #                               request.candidate_level)

        return {
            "found_files": [i['name'] for i in code_files],
            "comments": analysis_result.get("comments", "No comments provided."),
            "rating": analysis_result.get("rating", "Pending"),
            "conclusion": analysis_result.get("conclusion", "Review completed")
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during the review process."
        )