import httpx
from fastapi import HTTPException
import xml.etree.ElementTree as ET
import html


async def extract_visual_response(agent_message: dict) -> str:
    if not agent_message:
        raise HTTPException(
            status_code=500,
            detail="AgentMessage is empty or null"
        )

    if not isinstance(agent_message, dict):
        raise HTTPException(
            status_code=500,
            detail="AgentMessage is not a valid object"
        )

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "http://192.168.123.82:9000/evaluation",
                json=agent_message
            )
            response.raise_for_status()

        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="Evaluation endpoint timed out")

        except httpx.HTTPStatusError:
            raise HTTPException(status_code=502, detail="Evaluation endpoint returned an error")

        except httpx.RequestError:
            raise HTTPException(status_code=502, detail="Evaluation endpoint is unreachable")

    # parse the response
    try:
        result = response.json()
    except Exception:
        raise HTTPException(status_code=500, detail="Could not parse evaluation endpoint response")

    # extract visual response
    try:
        if result.get("responseType") != "AgentMessage":
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected responseType: {result.get('responseType')}"
            )

        info = result["display"]["info"]
        if info.get("type") != "Details":
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected info type: {info.get('type')}"
            )

        data = info["data"]["details"]["resultFields"]

        xml_message = next(
            (field["values"][0] for field in data if field["name"] == "Response"),
            None
        )
        if not xml_message:
            raise HTTPException(
                status_code=500,
                detail="Response field not found in resultFields"
            )

        try:
            root = ET.fromstring(xml_message)
        except ET.ParseError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to parse XML from Response field: {str(e)}"
            )

        # search for <Param type="MarkupHTML">
        visual_response = None
        for param in root.iter("Param"):
            if param.get("type") == "MarkupHTML":
                visual_response = str(html.unescape(param.text))
                break

        if not visual_response:
            raise HTTPException(
                status_code=500,
                detail="Could not find <Param type='MarkupHTML'> in XML"
            )

    except HTTPException:
        raise

    except (KeyError, TypeError) as e:
        raise HTTPException(
            status_code=500,
            detail=f"Could not extract visual response: {str(e)}"
        )

    # check extracted value is not empty
    if not visual_response.strip():
        raise HTTPException(
            status_code=500,
            detail="Visual response is empty"
        )

    return visual_response
