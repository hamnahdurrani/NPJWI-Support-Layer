from fastapi import APIRouter, Header, HTTPException
import httpx

from config import settings
from model import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    Choice,
    ResponseMessage
)
from services.token_parser import parse_bearer_token
from services.request_translator import build_evaluation_request
from services.response_translator import extract_visual_response

router = APIRouter()

@router.post("/v1/chat/completions")
async def chat_completions(
    request: ChatCompletionRequest,
    authorization: str = Header(None)
):
    access_code, env, user_id = parse_bearer_token(authorization)

    if not request.messages or not request.messages[0].content:
        raise HTTPException(status_code=400, detail="Missing or empty message content")

    eval_request = build_evaluation_request(
        access_code=access_code,
        user_id=user_id,
        question=request.messages[0].content
    )

    # Route to correct NPJWI URL based on env
    npjwi_url = settings.env_routing.get(env, settings.npjwi_base_url)

    # POST to NPJWI
    async with httpx.AsyncClient(timeout=settings.npjwi_timeout) as client:
        try:
            response = await client.post(
                npjwi_url,
                json=eval_request.model_dump()
            )
            response.raise_for_status()

        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="NPJWI request timed out")

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 403:
                raise HTTPException(status_code=403, detail="Invalid access code")
            raise HTTPException(status_code=502, detail="NPJWI returned an error")

        except httpx.RequestError:
            raise HTTPException(status_code=502, detail="NPJWI is unreachable")
     # To extract message from agent response
    answer = extract_visual_response(response.json())

    return ChatCompletionResponse(
        choices=[
            Choice(
                message=ResponseMessage(content=answer)
            )
        ]
    )