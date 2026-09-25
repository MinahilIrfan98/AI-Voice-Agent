# AI Voice Agent

Talk to an AI in your browser and it talks back. You speak, it answers out loud, and the whole conversation shows up as live captions on screen. The agent runs on LiveKit, tokens are issued by a small FastAPI backend, and the web interface is hand-built from scratch.

**Live demo:** [ai-voice-agent-mu-seven.vercel.app](https://ai-voice-agent-mu-seven.vercel.app)

Works on desktop and mobile browsers. The layout adapts to the screen size, and I have tested it on laptop and phone.

<!-- Add a screenshot or a 60-90 second demo GIF here -->

## What it does

Click the mic button, allow microphone access, and start speaking. The agent waits until you finish your sentence, thinks, and replies in a natural voice. The interface has mic controls, call management (start and end a session) and live transcription of both sides of the conversation.

## How it works

When a user opens the app, the frontend asks the backend for a session token and uses it to join a LiveKit room. LiveKit dispatches the agent into that room, and from there every turn goes through the same pipeline:

1. The microphone audio is cleaned up by an audio enhancer.
2. Deepgram Nova-3 transcribes it to text.
3. A turn detector decides when you have actually finished speaking.
4. The transcript goes to the LLM, which writes a reply.
5. A text-to-speech service turns the reply into audio and streams it back through LiveKit.
6. The browser plays the audio and prints the transcript.

## Project structure

| File | Role |
| --- | --- |
| `agent.py` | The voice agent. Started by LiveKit when a user joins, and runs the AI pipeline. |
| `server.py` | Local FastAPI server. Issues LiveKit tokens and serves the frontend. |
| `api/token.py` | Vercel serverless function that issues tokens for the deployed site. |
| `index.html` | The web interface: mic button, call controls, live captions. |
| `app.js` | Browser client. Joins the room, publishes the mic, renders responses. |
| `app.py` | Early Gradio prototype, kept for reference. |
| `run.py` | Starts the agent and the frontend server together. |

## Tech stack

- **Realtime:** LiveKit (WebRTC, agent dispatch, rooms)
- **AI pipeline:** Deepgram Nova-3 for speech-to-text, plus an LLM, text-to-speech and turn detection
- **Backend:** Python, FastAPI, LiveKit Agents SDK, uv
- **Frontend:** HTML, CSS, JavaScript with the LiveKit client SDK
- **Hosting:** Vercel for the frontend and token endpoint, LiveKit Cloud for the agent worker

## Run it locally

You need Python 3.13, [uv](https://docs.astral.sh/uv/), and a LiveKit Cloud project with API keys.

```bash
uv sync
```

Create a `.env` file in the project root:
LIVEKIT_URL=your-livekit-url
LIVEKIT_API_KEY=your-api-key
LIVEKIT_API_SECRET=your-api-secret

Then start everything with one command:

```bash
uv run run.py
```

Open http://127.0.0.1:8000, click the mic button and allow microphone access.

## Deployment

The frontend and the token endpoint are deployed on Vercel. The agent itself is deployed as a persistent worker on LiveKit Cloud, so it stays online and responds around the clock, independent of whether my laptop is on. It's built and shipped straight from this repo using the LiveKit CLI (`lk agent deploy`), with a Dockerfile that installs dependencies via `uv` and runs `agent.py` as the entrypoint.

## Notes

The project started from LiveKit's starter agent template. The token server, the frontend, the caption and call controls, and the deployment setup are my additions.