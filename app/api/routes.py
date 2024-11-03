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
async def review(request: ReviewRequest) -> Dict[str, Union[str, List[str]]] :
    try:
        repo_url = request.github_repo_url.split("github.com/")[-1]
        print(repo_url)
        code_files = await github_service.get_repository_contents(repo_url)
        analysis = 'dfad'#await gpt_service.analyze_code(code_files, request.assignment_description, request.candidate_level)
        return {"found_files": [i['name'] for i in code_files], "comments": analysis, "rating": "Pending", "conclusion": "Review completed"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during the review process."
        )
