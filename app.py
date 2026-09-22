import os
import uuid
import gradio as gr
from dotenv import load_dotenv
from livekit import api

load_dotenv(".env")

LIVEKIT_URL = os.getenv("LIVEKIT_URL")
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET")

def get_token():
    """Generates a LiveKit token that dispatches the 'my-agent' agent."""
    room_name = f"room-{uuid.uuid4().hex[:8]}"
    token = api.AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET) \
        .with_identity(f"user-{uuid.uuid4().hex[:4]}") \
        .with_grants(api.VideoGrants(room_join=True, room=room_name))

    token = token.with_agent_dispatch(api.RoomAgentDispatch(agent_name="my-agent"))

    return {
        "token": token.to_jwt(),
        "url": LIVEKIT_URL,
        "room": room_name
    }

# Polished Design CSS
css = """
.hidden-component { display: none !important; }

body, .gradio-container {
    background: radial-gradient(circle at center, #1a1c2e 0%, #0b0e14 100%) !important;
    color: white !important;
    font-family: 'Inter', sans-serif !important;
}

#main-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 30px;
    padding: 60px 20px;
    min-height: 80vh;
}

#mic-container {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
}

#mic-btn {
    width: 120px !important;
    height: 120px !important;
    border-radius: 50% !important;
    background: #4f46e5 !important;
    border: none !important;
    cursor: pointer !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    transition: all 0.3s ease !important;
    z-index: 10 !important;
    box-shadow: 0 0 30px rgba(79, 70, 229, 0.3) !important;
}

#mic-btn svg {
    width: 50px;
    height: 50px;
    fill: white;
    transition: all 0.3s ease;
}

#mic-btn:hover { transform: scale(1.05); }

/* Pulse Rings */
.pulse {
    position: absolute;
    width: 120px;
    height: 120px;
    border-radius: 50%;
    background: rgba(79, 70, 229, 0.4);
    z-index: 1;
    pointer-events: none;
}

.pulse-listening {
    animation: pulse-slow 2s infinite;
}

.pulse-speaking {
    animation: pulse-fast 1s infinite;
}

.pulse-idle {
    background: rgba(100, 100, 100, 0.2);
    animation: none;
}

@keyframes pulse-slow {
    0% { transform: scale(1); opacity: 0.6; }
    100% { transform: scale(2); opacity: 0; }
}

@keyframes pulse-fast {
    0% { transform: scale(1); opacity: 0.6; }
    100% { transform: scale(1.8); opacity: 0; }
}

#status-label {
    font-size: 14px;
    color: #8b949e;
    font-weight: 600;
    margin-top: 20px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

#chat-container {
    width: 100%;
    max-width: 600px;
    display: none; /* Hidden until conversation starts */
    flex-direction: column;
    gap: 12px;
    margin-top: 40px;
    padding: 20px;
    background: rgba(22, 27, 34, 0.5);
    border-radius: 16px;
    border: 1px solid rgba(48, 54, 61, 0.5);
    max-height: 400px;
    overflow-y: auto;
}

.msg {
    max-width: 80%;
    padding: 12px 16px;
    border-radius: 18px;
    font-size: 15px;
    line-height: 1.4;
}

.msg-user {
    align-self: flex-end;
    background: #4f46e5;
    color: white;
    border-bottom-right-radius: 4px;
}

.msg-agent {
    align-self: flex-start;
    background: #30363d;
    color: #c9d1d9;
    border-bottom-left-radius: 4px;
}
"""

# SVG Mic Icon
MIC_SVG = """
<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
    <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"/>
    <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/>
</svg>
"""

html_content = f"""
<div id="main-container">
    <div id="mic-container">
        <div id="p1" class="pulse pulse-idle"></div>
        <div id="p2" class="pulse pulse-idle" style="animation-delay: 0.5s"></div>
        <button id="mic-btn">{MIC_SVG}</button>
    </div>
    <div id="status-label">Ready</div>
    <div id="chat-container"></div>
</div>
"""

with gr.Blocks() as demo:
    # Use gr.HTML with js_on_load to attach the click listener and setup logic
    with open("app.js", "r", encoding="utf-8") as f:
        js_code = f.read()

    gr.HTML(
        value=html_content,
        head='<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">',
        js_on_load=js_code
    )


    with gr.Row(elem_classes="hidden-component"):
        start_btn = gr.Button("Start", elem_id="start-btn")
        token_out = gr.JSON()

    start_btn.click(
        fn=get_token,
        outputs=token_out,
        js="""
        async (data) => {
            console.log('[UI] Token fetched:', data);
            if (!data || !data.token) {
                console.error('[UI] Invalid token data received');
                return;
            }

            if (!window.LivekitClient) {
                console.log('[UI] Loading LivekitClient script...');
                await new Promise((resolve) => {
                    const script = document.createElement('script');
                    script.src = 'https://cdn.jsdelivr.net/npm/livekit-client@2/dist/livekit-client.umd.min.js';
                    script.onload = resolve;
                    document.head.appendChild(script);
                });
                console.log('[UI] LivekitClient script loaded');
            }

            try {
                await window.joinRoom(data.url, data.token);
                console.log('[UI] joinRoom called successfully');
            } catch (e) {
                console.error('[UI] joinRoom failed:', e);
            }
        }
    """)

if __name__ == "__main__":
    demo.launch(css=css)
