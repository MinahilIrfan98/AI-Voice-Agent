"""Vercel serverless function: GET /api/token
Har request pe naya LiveKit token banata hai (agent "my-agent" dispatch ke saath).
Keys .env file se nahi, Vercel ke Project Settings > Environment Variables se aati hain.
"""
from http.server import BaseHTTPRequestHandler
import json
import os
import uuid

from livekit import api

AGENT_NAME = "my-agent"


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            url = os.environ["LIVEKIT_URL"]
            key = os.environ["LIVEKIT_API_KEY"]
            secret = os.environ["LIVEKIT_API_SECRET"]
        except KeyError as missing:
            self._send(500, {"detail": f"{missing} Vercel env vars mein nahi mila"})
            return

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
        self._send(200, {"url": url, "token": jwt})

    def _send(self, status, payload):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())