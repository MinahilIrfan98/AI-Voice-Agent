# AI Voice Agent

An AI voice agent built with **LiveKit**, using real-time speech-to-text, LLM, and text-to-speech pipelines for natural voice conversations. Includes a custom FastAPI backend for secure token generation and a responsive web frontend with live transcription, mic controls, and call management — built end to end from backend to UI design.

🔗 **Live Demo:** [ai-voice-agent-mu-seven.vercel.app](#)

---

## Architecture

The system is split into four layers:

### 1. Session Access
Handles how a client gets permission to join a voice session.
- **`api/token.py`** (Vercel Token Route) — serverless function that issues a LiveKit access token for the deployed frontend.
- **`server.py`** (FastAPI Server) — local backend that also issues tokens when running on a laptop, and serves the static web shell.

### 2. Client Experience
What the user actually sees and interacts with.
- **`index.html`** (Static Web Shell) — the polished custom UI: mic button, call controls, live captions.
- **`app.py`** (Gradio UI) — an earlier prototype interface that generates a token and passes credentials to the browser client.
- **`app.js`** (Browser Client) — connects to the LiveKit room, publishes the user's microphone, dispatches the agent, and renders the agent's responses back to the user.

### 3. Realtime Runtime
The live communication layer, powered by LiveKit.
- **LiveKit Platform** — the real-time WebRTC infrastructure that routes audio between the browser and the agent.
- **`agent.py`** (Agent Server + Voice Session) — dispatched by LiveKit when a user joins; starts a voice session that orchestrates the AI pipeline and publishes responses back to the room.

### 4. AI Processing
The pipeline that turns speech into a spoken response.
- **STT Service** — transcribes incoming audio (Deepgram Nova-3).
- **Turn Detector** — detects when the user has finished speaking.
- **Audio Enhancer** — cleans/enhances microphone input before transcription.
- **LLM Service** — generates the agent's response.
- **TTS Service** — synthesizes the response back into speech.

---

## How a Conversation Flows

1. User opens the web app → a session token is requested and issued.
2. Browser client connects to the LiveKit room and publishes the user's microphone.
3. LiveKit dispatches the agent, which starts a voice session.
4. Audio is enhanced, transcribed (STT), and turn-detection determines when the user has finished speaking.
5. The transcript goes to the LLM, which generates a response.
6. The response is converted to speech (TTS) and streamed back through LiveKit.
7. The browser client plays the audio and renders the live transcript/response for the user.

---

## Tech Stack

- **Real-time infrastructure:** LiveKit (WebRTC, agent dispatch, room management)
- **AI pipeline:** Deepgram (STT), LLM inference, TTS synthesis, turn detection
- **Backend:** Python, FastAPI, LiveKit Agents SDK, `uv` for dependency management
- **Frontend:** HTML/CSS/JavaScript with the LiveKit client SDK
- **Deployment:** Vercel (frontend + token endpoint)

---

## Running Locally

**Prerequisites:** Python 3.13, [uv](https://docs.astral.sh/uv/), a LiveKit Cloud project with API keys.

1. Clone the repo and install dependencies:
   ```bash
   uv sync
   ```

2. Create a `.env` file in the project root with:
   ```
   LIVEKIT_URL=your-livekit-url
   LIVEKIT_API_KEY=your-api-key
   LIVEKIT_API_SECRET=your-api-secret
   ```

3. Run the full stack (agent + frontend server) with a single command:
   ```bash
   uv run run.py
   ```

4. Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser, click the mic button, and allow microphone access.

---

## Deployment

The frontend (`index.html`) and token endpoint (`api/token.py`) are deployed on **Vercel**. The voice agent (`agent.py`) needs to run persistently — either locally via `uv run agent.py dev`, or deployed independently to **LiveKit Cloud** for full 24/7 availability.

---

## Notes

This project started from LiveKit's starter agent template and was extended with a custom token server, a hand-built frontend (mic controls, live captions, call management), and a full local-to-cloud deployment pipeline.