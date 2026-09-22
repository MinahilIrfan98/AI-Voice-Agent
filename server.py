import os
import uuid
from pathlib import Path

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from livekit import api

BASE = Path(__file__).parent
load_dotenv(BASE / ".env")

# agent.py mein @server.rtc_session(agent_name="my-agent") likha hai, isliye yahi naam
AGENT_NAME = "my-agent"

app = FastAPI()


@app.get("/")
def index():
    return FileResponse(BASE / "index.html")


@app.get("/api/token")
def token():
    try:
        url = os.environ["LIVEKIT_URL"]
        key = os.environ["LIVEKIT_API_KEY"]
        secret = os.environ["LIVEKIT_API_SECRET"]
    except KeyError as missing:
        return JSONResponse(
            {"detail": f"{missing} .env mein nahi mila"}, status_code=500
        )

    room = f"voice-{uuid.uuid4().hex[:8]}"
    jwt = (
        api.AccessToken(key, secret)
        .with_identity(f"user-{uuid.uuid4().hex[:6]}")
        .with_name("User")
        .with_grants(api.VideoGrants(room_join=True, room=room))
        .with_room_config(
            api.RoomConfiguration(
                agents=[api.RoomAgentDispatch(agent_name=AGENT_NAME)]
            )
        )
        .to_jwt()
    )
    return {"url": url, "token": jwt}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)