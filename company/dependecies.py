from fastapi import Header, HTTPException


async def get_token_header(internal_tokken: str = Header()):
    if internal_tokken != "allowed":
        raise HTTPException(status_code=400, detail="Internal-Token header invalid")