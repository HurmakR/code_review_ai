import logging
from fastapi import APIRouter, HTTPException, status
from typing import Dict, List, Union
from app.services.github_service import GitHubService
from app.services.gpt_service import GPTService
from app.models.request_models import ReviewRequest
from app.models.response_models import ReviewResult

# Configure logger
logger = logging.getLogger(__name__)

router = APIRouter()
github_service = GitHubService()
gpt_service = GPTService()

@router.post("/review", response_model=ReviewResult)
async def review(request: ReviewRequest) -> Dict[str, Union[str, List[str]]]:
    logger.info("Received review request")
    try:
        repo_url = request.github_repo_url.split("github.com/")[-1]
        logger.debug(f"Parsed repo URL: {repo_url}")

        code_files = await github_service.get_repository_contents(repo_url)
        logger.info(f"Retrieved {len(code_files)} files from the repository")

        # Call to GPT service to analyze the code files
        analysis_result = await gpt_service.analyze_code(
            code_files, request.assignment_description, request.candidate_level
        )
        logger.info("Analysis completed successfully")

        if analysis_result is None:
            logger.warning("Analysis result is None, returning default values")
            return {
                "found_files": [i['name'] for i in code_files],
                "comments": "No comments provided.",
                "rating": "Pending",
                "conclusion": "Review completed"
            }

        return {
            "found_files": [i['name'] for i in code_files],
            "comments": analysis_result.get("comments", "No comments provided."),
            "rating": analysis_result.get("rating", "Pending"),
            "conclusion": analysis_result.get("conclusion", "Review completed")
        }
    except HTTPException as e:
        logger.error(f"HTTPException occurred: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during the review process."
        )
