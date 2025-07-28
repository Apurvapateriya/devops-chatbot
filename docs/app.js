async function sendMessage() {
  const inputElem = document.getElementById('user-input');
  const responseElem = document.getElementById('response');
  const userInput = inputElem.value.trim();

  if (!userInput) {
    responseElem.textContent = "Go on, don't be shy .. Ask Something!";
    return;
  }

  try {
    const response = await fetch('https://devops-chatbot-zstm.onrender.com/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': 'mysecret123'
      },
      body: JSON.stringify({ message: userInput })
    });

    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }

    const data = await response.json();
    responseElem.textContent = data.response;
  } catch (error) {
    responseElem.textContent = 'Oops! Something went wrong';
    console.error(error);
  }
}
