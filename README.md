# LiveKit Voice Agent

A real-time voice AI assistant powered by LiveKit and Python.

## Setup

1. **Environment Variables**
   Create a `.env` file in the root directory with the following keys:
   - `LIVEKIT_URL`: Your LiveKit server URL (e.g., `wss://your-project.livekit.cloud`)
   - `LIVEKIT_API_KEY`: Your LiveKit API Key
   - `LIVEKIT_API_SECRET`: Your LiveKit API Secret

2. **Dependencies**
   Ensure you have `uv` installed. The project uses `uv` for dependency management.

## Running the App

To run the entire stack (Backend Agent + Gradio Frontend) on localhost:

```bash
uv run run.py
```

This will start the agent server and the Gradio UI. Once started, open the local URL provided by Gradio in your browser.

## How it Works
- **Backend**: `agent.py` defines a LiveKit agent that uses STT, LLM, and TTS plugins.
- **Frontend**: `app.py` generates a session-specific LiveKit token with agent dispatch and provides a polished UI for interacting with the agent.
- **Orchestration**: `run.py` manages both processes and handles clean shutdown on Ctrl+C.
