from fastapi import HTTPException

def parse_bearer_token(authorization: str) -> tuple[str, str, str]:
    # check if header exists at all
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    
    # check if it starts with "Bearer "
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization format")

    # strip the "Bearer " prefix to get the raw token
    token = authorization.removeprefix("Bearer ")

    # split by underscore — expect exactly 3 parts
    parts = token.split("_")

    if len(parts) != 3:
        raise HTTPException(status_code=401, detail="Invalid token format")

    access_code = parts[0]
    env = parts[1]      
    user_id = parts[2]

    return access_code, env, user_id