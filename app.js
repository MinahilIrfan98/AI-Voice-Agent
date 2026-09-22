(element) => {
    const statusEl = document.getElementById('status-label');
    const chatContainer = document.getElementById('chat-container');
    const btn = document.getElementById('mic-btn');
    const p1 = document.getElementById('p1');
    const p2 = document.getElementById('p2');
    let room;

    const updateStatus = (text, state) => {
        console.log(`[UI] Status: ${text}`);
        statusEl.innerText = text;

        // Update pulse rings
        p1.className = 'pulse';
        p2.className = 'pulse';

        if (state === 'idle') {
            p1.classList.add('pulse-idle');
            p2.classList.add('pulse-idle');
        } else if (state === 'listening') {
            p1.classList.add('pulse-listening');
            p2.classList.add('pulse-listening');
        } else if (state === 'speaking') {
            p1.classList.add('pulse-speaking');
            p2.classList.add('pulse-speaking');
        }
    };

    const addMessage = (text, sender) => {
        chatContainer.style.display = 'flex';
        const div = document.createElement('div');
        div.className = `msg msg-${sender === 'user' ? 'user' : 'agent'}`;
        div.innerText = text;
        chatContainer.appendChild(div);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    };

    window.joinRoom = async (url, token) => {
        try {
            updateStatus('Connecting...', 'idle');
            room = new LivekitClient.Room();

            room.on(LivekitClient.RoomEvent.TrackSubscribed, (track) => {
                if (track.kind === 'audio') {
                    console.log('[UI] Audio track attached');
                    track.attach();
                }
            });

            try {
                await room.registerTextStreamHandler("lk.transcription", async (reader, info) => {
                    for await (const message of reader) {
                        const text = message.text;
                        const sender = info.identity === room.localParticipant.identity ? 'user' : 'agent';
                        console.log(`[UI] ${sender}: ${text}`);
                        addMessage(text, sender);
                        if (sender === 'agent') updateStatus('Agent speaking', 'speaking');
                    }
                });
            } catch (streamErr) {
                console.error('[UI] Transcription Stream Error:', streamErr);
            }

            await room.connect(url, token);

            try {
                await room.localParticipant.setMicrophoneEnabled(true);
                await room.startAudio();
            } catch (micErr) {
                console.error('[UI] Mic Error:', micErr);
                updateStatus('Mic Error: ' + micErr.message, 'idle');
                throw micErr;
            }

            console.log('[UI] Room connected');
            updateStatus('Listening', 'listening');
            btn.style.background = '#ef4444'; // Red when active
        } catch (err) {
            console.error('[UI] Connection Error:', err);
            updateStatus('Error: ' + err.message, 'idle');
        }
    };

    window.leaveRoom = async () => {
        if (room) {
            await room.disconnect();
            room = null;
            updateStatus('Ready', 'idle');
            btn.style.background = '#4f46e5';
        }
    };

    btn.onclick = async () => {
        console.log('[UI] Mic button clicked');
        if (room) {
            await window.leaveRoom();
        } else {
            const gradioBtn = document.querySelector('button[data-component="button"][id*="start-btn"]');
            if (gradioBtn) {
                console.log('[UI] Triggering Gradio token fetch');
                gradioBtn.click();
            } else {
                console.error('[UI] Start button not found in DOM');
                updateStatus('UI Error: Start button missing', 'idle');
            }
        }
    };
}
