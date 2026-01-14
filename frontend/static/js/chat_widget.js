document.addEventListener('DOMContentLoaded', function () {
    // Inject CSS
    const style = document.createElement('style');
    style.innerHTML = `
        #placement-ai-widget {
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 10000;
            font-family: 'Inter', sans-serif;
        }
        #ai-chat-btn {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            color: white;
            border: none;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
            transition: transform 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
        }
        #ai-chat-btn:hover {
            transform: scale(1.1);
        }
        #ai-chat-window {
            display: none;
            width: 350px;
            height: 500px;
            background: #1e1e2d;
            border-radius: 15px;
            box-shadow: 0 5px 25px rgba(0,0,0,0.3);
            flex-direction: column;
            overflow: hidden;
            position: absolute;
            bottom: 80px;
            right: 0;
            border: 1px solid rgba(255,255,255,0.1);
        }
        .chat-header {
            background: linear-gradient(to right, rgba(99, 102, 241, 0.2), rgba(139, 92, 246, 0.2));
            padding: 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        .chat-body {
            flex: 1;
            padding: 15px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 10px;
            background: #151521;
        }
        .chat-footer {
            padding: 15px;
            background: rgba(255,255,255,0.02);
            display: flex;
            gap: 10px;
            border-top: 1px solid rgba(255,255,255,0.05);
            align-items: center;
        }
        .chat-input {
            flex: 1;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 20px;
            padding: 10px 15px;
            color: white;
            outline: none;
            font-size: 0.9rem;
        }
        .chat-action-btn {
            background: #6366f1;
            border: none;
            color: white;
            border-radius: 50%;
            width: 38px;
            height: 38px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: background 0.2s;
            flex-shrink: 0;
        }
        .chat-action-btn:hover {
            background: #4f46e5;
        }
        .chat-action-btn.listening {
            background: #ef4444;
            animation: pulse 1.5s infinite;
        }
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }
            70% { box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); }
            100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
        }
        .message {
            max-width: 85%;
            padding: 10px 14px;
            border-radius: 12px;
            font-size: 0.9rem;
            line-height: 1.5;
            word-wrap: break-word;
        }
        .message.user {
            align-self: flex-end;
            background: #6366f1;
            color: white;
            border-bottom-right-radius: 2px;
        }
        .message.ai {
            align-self: flex-start;
            background: rgba(255,255,255,0.1);
            color: #e2e8f0;
            border-bottom-left-radius: 2px;
        }
        .typing-indicator {
            align-self: flex-start;
            font-size: 0.75rem;
            color: rgba(255,255,255,0.5);
            margin-left: 10px;
            margin-bottom: 5px;
            display: none;
            font-style: italic;
        }
        /* Markdown styles */
        .message.ai li { margin-left: 20px; }
        .message.ai strong { color: #fff; }
    `;
    document.head.appendChild(style);

    // Initial HTML
    const widget = document.createElement('div');
    widget.id = 'placement-ai-widget';
    widget.innerHTML = `
        <div id="ai-chat-window">
            <div class="chat-header">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <i class="fas fa-robot" style="color: #6366f1; font-size: 1.2rem;"></i>
                    <div style="display: flex; flex-direction: column;">
                        <span style="font-weight: 600; color: white; font-size: 0.9rem;">PLACEMENT-AI</span>
                        <select id="chat-lang-select" style="background: rgba(0,0,0,0.2); border: none; color: white; font-size: 0.7rem; padding: 2px; border-radius: 4px; cursor: pointer; outline: none;">
                            <option value="en-US">English</option>
                            <option value="hi-IN">Hindi</option>
                            <option value="kn-IN">Kannada</option>
                            <option value="ta-IN">Tamil</option>
                            <option value="te-IN">Telugu</option>
                            <option value="ml-IN">Malayalam</option>
                        </select>
                    </div>
                </div>
                <button id="close-chat" style="background: none; border: none; color: rgba(255,255,255,0.6); cursor: pointer;"><i class="fas fa-chevron-down"></i></button>
            </div>
            <div class="chat-body" id="chat-messages">
                <div class="message ai">Hello! I am PLACEMENT-AI. I can speak 6 languages. How can I help?</div>
            </div>
            <div class="typing-indicator" id="typing-indicator">AI is writing...</div>
            <div class="chat-footer">
                <input type="text" class="chat-input" id="chat-input" placeholder="Type or speak..." autocomplete="off">
                <button class="chat-action-btn" id="mic-btn" title="Speak"><i class="fas fa-microphone"></i></button>
                <button class="chat-action-btn" id="send-btn" title="Send"><i class="fas fa-paper-plane"></i></button>
            </div>
        </div>
        <button id="ai-chat-btn"><i class="fas fa-comment-dots"></i></button>
    `;
    document.body.appendChild(widget);

    // Logic
    const btn = document.getElementById('ai-chat-btn');
    const windowEl = document.getElementById('ai-chat-window'); // RENAMED to windowEl to avoid conflict with global window
    const closeBtn = document.getElementById('close-chat');
    const input = document.getElementById('chat-input');
    const sendBtn = document.getElementById('send-btn');
    const micBtn = document.getElementById('mic-btn');
    const langSelect = document.getElementById('chat-lang-select');
    const messagesContainer = document.getElementById('chat-messages');
    const typingIndicator = document.getElementById('typing-indicator');

    let history = [];
    let isSpeaking = false;

    // Speech Recognition Setup
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    let recognition = null;
    let isListening = false;

    if (SpeechRecognition) {
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;

        recognition.onstart = function () {
            isListening = true;
            micBtn.classList.add('listening');
            input.placeholder = "Listening...";
        };

        recognition.onend = function () {
            isListening = false;
            micBtn.classList.remove('listening');
            input.placeholder = "Type or speak...";
        };

        recognition.onresult = function (event) {
            const transcript = event.results[0][0].transcript;
            input.value = transcript;
            setTimeout(() => {
                sendMessage(); // Auto-send on voice input
            }, 500);
        };

        recognition.onerror = function (event) {
            console.error('Speech recognition error', event.error);
            isListening = false;
            micBtn.classList.remove('listening');
            input.placeholder = "Type or speak...";
            if (event.error === 'not-allowed') {
                alert("Microphone access denied.");
            }
        };
    } else {
        micBtn.style.display = 'none'; // Hide if not supported
    }

    micBtn.addEventListener('click', () => {
        if (!recognition) return;
        if (isListening) {
            recognition.stop();
        } else {
            recognition.lang = langSelect.value;
            recognition.start();
        }
    });

    // Speech Synthesis Setup
    // Speech Synthesis Setup
    function speak(text) {
        if (!window.speechSynthesis) return;

        // Stop any current speech
        window.speechSynthesis.cancel();

        const utterance = new SpeechSynthesisUtterance(text);
        const targetLang = langSelect.value;
        utterance.lang = targetLang;

        // Load voices
        let voices = window.speechSynthesis.getVoices();

        // Function to select best voice
        const selectVoice = () => {
            // 1. Precise Match (e.g., 'hi-IN' === 'hi-IN')
            let bestVoice = voices.find(v => v.lang === targetLang);

            // 2. Google Cloud Voice Match (Usually higher quality)
            if (!bestVoice) {
                bestVoice = voices.find(v => v.name.includes("Google") && v.lang.startsWith(targetLang.split('-')[0]));
            }

            // 3. Fuzzy Language Code Match (e.g., 'hi' matches 'hi-IN')
            if (!bestVoice) {
                const shortLang = targetLang.split('-')[0];
                bestVoice = voices.find(v => v.lang.startsWith(shortLang));
            }

            // 4. Fallback (English, if critical failure to find Indian voice but user needs to hear SOMETHING)
            // But usually better to let the OS handle the fallback if we don't set .voice explicitly

            if (bestVoice) {
                console.log(`[TTS] Selected Voice: ${bestVoice.name} (${bestVoice.lang}) for target: ${targetLang}`);
                utterance.voice = bestVoice;
            } else {
                console.warn(`[TTS] No specific voice found for ${targetLang}. Relying on OS default.`);
            }

            window.speechSynthesis.speak(utterance);
        };

        // If voices are not ready, wait a bit (Chrome quirk)
        if (voices.length === 0) {
            window.speechSynthesis.onvoiceschanged = () => {
                voices = window.speechSynthesis.getVoices();
                selectVoice();
            };
        } else {
            selectVoice();
        }
    }

    function toggleChat() {
        if (windowEl.style.display === 'flex') {
            windowEl.style.display = 'none';
            btn.style.display = 'flex';
            window.speechSynthesis.cancel(); // Stop speaking when closed
        } else {
            windowEl.style.display = 'flex';
            btn.style.display = 'none';
            input.focus();
        }
    }

    btn.addEventListener('click', toggleChat);
    closeBtn.addEventListener('click', toggleChat);

    function formatMessage(text) {
        return text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/- (.*?)(\n|$)/g, '<li>$1</li>')
            .replace(/\n/g, '<br>');
    }

    function addMessage(text, sender) {
        const div = document.createElement('div');
        div.className = `message ${sender}`;
        div.innerHTML = formatMessage(text);
        messagesContainer.appendChild(div);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    async function sendMessage() {
        const text = input.value.trim();
        if (!text) return;

        // Stop any previous speech
        window.speechSynthesis.cancel();

        addMessage(text, 'user');
        input.value = '';
        typingIndicator.style.display = 'block';

        const selectedLanguage = langSelect.value; // Get selected language

        // Add context for language if needed, but Gemini usually detects it.
        // We can append a system instruction implicitly if we really wanted to enforce language,
        // but for now relying on natural conversation is better.

        try {
            const response = await fetch('/api/general_chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text, history: history, language: selectedLanguage })
            });

            const data = await response.json();
            typingIndicator.style.display = 'none';

            if (data.response) {
                addMessage(data.response, 'ai');
                history.push({ role: 'user', message: text });
                history.push({ role: 'model', message: data.response });
                // Limit client history
                if (history.length > 20) history = history.slice(-20);

                // Speak the response
                speak(data.response);

            } else {
                addMessage("Sorry, I couldn't get a response.", 'ai');
            }
        } catch (e) {
            typingIndicator.style.display = 'none';
            addMessage("Connection error. Please try again.", 'ai');
        }
    }

    sendBtn.addEventListener('click', sendMessage);
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
});
