from fastapi import HTTPException

def extract_visual_response(agent_message: dict) -> str:

    # check we actually received something
    if not agent_message:
        raise HTTPException(
            status_code=500,
            detail="AgentMessage is empty or null"
        )

    # check it's a dictionary
    if not isinstance(agent_message, dict):
        raise HTTPException(
            status_code=500,
            detail="AgentMessage is not a valid object"
        )
    
    visual_response = _extract_from_agent_message(agent_message)

    # check extracted value is not empty
    if not visual_response or not visual_response.strip():
        raise HTTPException(
            status_code=500,
            detail="Visual response extracted from AgentMessage is empty"
        )

    return visual_response


def _extract_from_agent_message(agent_message: dict) -> str:
    # ================================================================
    # TO DO :
    # Find the field that contains the answer text in AgentMessage response
    # Add a try/except so it returns a 500 if the field is missing
    # ================================================================
    raise HTTPException(
        status_code=500,
        detail="AgentMessage cannot be parsed"
    )