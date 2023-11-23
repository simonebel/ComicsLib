from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()


@router.get("/test/", tags=["test"])
def test_router():
    return {"test": "Test router"}
