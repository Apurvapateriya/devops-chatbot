async function sendMessage() {
  const inputElem = document.getElementById('user-input');
  const chatWindow = document.getElementById('chat-window');
  const userInput = inputElem.value.trim();

  if (!userInput) {
    alert("Go on, don't be shy .. Ask Something!");
    return;
  }

  const userMsgDiv = document.createElement('div');
  userMsgDiv.className = 'chat-message user-message';
  userMsgDiv.textContent = userInput;
  chatWindow.appendChild(userMsgDiv);

  inputElem.value = '';
  chatWindow.scrollTop = chatWindow.scrollHeight;

  try {
    const response = await fetch('https://devops-chatbot-zstm.onrender.com/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ message: userInput })
    });

    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }

    const data = await response.json();

    const botMsgDiv = document.createElement('div');
    botMsgDiv.className = 'chat-message bot-message';
    botMsgDiv.textContent = data.response;
    chatWindow.appendChild(botMsgDiv);

    chatWindow.scrollTop = chatWindow.scrollHeight;

  } catch (error) {
    const errorMsgDiv = document.createElement('div');
    errorMsgDiv.className = 'chat-message bot-message error';
    errorMsgDiv.textContent = 'Oops! Something went wrong.';
    chatWindow.appendChild(errorMsgDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight;

    console.error(error);
  }
}
