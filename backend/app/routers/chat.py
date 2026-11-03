from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api/chat", tags=["chat"])

# Phases 3-4: wired to services.ai once the OpenAI integration is implemented.


@router.get("/today")
def today():
    raise HTTPException(501, "chat is not implemented yet")


@router.post("/messages")
def send_message():
    raise HTTPException(501, "chat is not implemented yet")
