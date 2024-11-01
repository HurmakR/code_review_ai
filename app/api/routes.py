from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.post("/review")
async def review():
    return {"message": "Code review started"}