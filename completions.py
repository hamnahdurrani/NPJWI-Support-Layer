from fastapi import APIRouter, Header, HTTPException
import httpx

from config import config
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
    if not request or not request.messages:
        raise HTTPException(status_code=400, detail="Request body is empty or missing messages")

    if not request.messages[0].content or not request.messages[0].content.strip():
        raise HTTPException(status_code=400, detail="Message content is empty")

    access_code, env, user_id = parse_bearer_token(authorization)

    eval_request = build_evaluation_request(
        access_code=access_code,
        user_id=user_id,
        question=request.messages[0].content
    )

    base_url = config.env_routing.get(env, "")
    npjwi_url = f"{base_url}{config.npjwi_base_url}"

    #POST to NPJWI
    async with httpx.AsyncClient(timeout=config.npjwi_timeout) as client:
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

    answer = await extract_visual_response(response.json())

    return ChatCompletionResponse(
        choices=[
            Choice(
                message=ResponseMessage(content=answer)
            )
        ]
    )