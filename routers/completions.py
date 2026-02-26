from fastapi import APIRouter

router = APIRouter()

@router.post("/v1/chat/completions")
async def chat_completions():
    return {"message": "not implemented yet"}