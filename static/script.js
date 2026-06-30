const chatBox = document.getElementById("chatBox");

async function sendMessage() {
  const input = document.getElementById("userInput");
  const text = input.value.trim();

  if (text === "") return;

  addMessage(text, "user");

  input.value = "";

  const response = await fetch("/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      message: text,
    }),
  });

  const data = await response.json();

  addMessage(data.response, "bot");
}

function addMessage(message, type) {
  const div = document.createElement("div");

  div.classList.add("message", type);

  div.innerHTML = `<span>${message}</span>`;

  chatBox.appendChild(div);

  chatBox.scrollTop = chatBox.scrollHeight;
}

document.getElementById("userInput").addEventListener("keypress", function (e) {
  if (e.key === "Enter") {
    sendMessage();
  }
});
