const inputField = document.querySelector('.input-field');
const sendIcon = document.querySelector('.send-icon');
const chatArea = document.querySelector('.chat-area');

sendIcon.addEventListener('click', sendMessage);

inputField.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});

async function sendMessage() {

    const userMsg = inputField.value.trim();
    if (!userMsg) return;

    addUserMessage(userMsg);
    inputField.value = "";

    showTyping();

    const botReply = await getAIReply(userMsg);

    removeTyping();
    addBotMessage(botReply);
}

/******** UI ********/
function addUserMessage(text) {
    const div = document.createElement("div");
    div.className = "message-bubble user";
    div.innerText = text;
    chatArea.appendChild(div);
    scrollDown();
}

function addBotMessage(text) {
    const div = document.createElement("div");
    div.className = "message-bubble bot";
    div.innerText = text;
    chatArea.appendChild(div);
    scrollDown();
}

function showTyping() {
    removeTyping();
    const div = document.createElement("div");
    div.className = "message-bubble bot typing";
    div.innerText = "Typing...";
    chatArea.appendChild(div);
    scrollDown();
}

function removeTyping() {
    const t = document.querySelector(".typing");
    if (t) t.remove();
}

function scrollDown() {
    chatArea.scrollTop = chatArea.scrollHeight;
}

/******** BACKEND CALL ********/
async function getAIReply(message) {

    try {
        const res = await fetch(
            "http://127.0.0.1:8000/chat",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ message })
            }
        );

        const data = await res.json();
        return data.reply;

    } catch (err) {
        return "I'm here for you 💙 Can you tell me more?";
    }
}
