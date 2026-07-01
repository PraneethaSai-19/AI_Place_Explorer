const chatBox = document.getElementById("chatBox");

async function sendMessage() {
  const input = document.getElementById("userInput");

  const text = input.value.trim();

  if (text === "") return;

  addMessage(text, "user");

  input.value = "";
  const loading = document.createElement("div");
  loading.className = "message bot";
  loading.id = "loading";

  loading.innerHTML = "<span>Typing...</span>";

  chatBox.appendChild(loading);

  chatBox.scrollTop = chatBox.scrollHeight;

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

  document.getElementById("loading").remove();

  addMessage(data.response, "bot");

  chatBox.scrollTop = chatBox.scrollHeight;

  loadFavorites();
}

function addMessage(message, type) {
  const div = document.createElement("div");

  div.className = `message ${type}`;

  div.innerHTML = `<span>${message}</span>`;

  chatBox.appendChild(div);
}

function showChat() {
  document.getElementById("chatSection").style.display = "flex";
  document.getElementById("favoritesSection").style.display = "none";

  const chatBox = document.getElementById("chatBox");
  chatBox.scrollTop = chatBox.scrollHeight;
}
async function showFavorites() {
  document.getElementById("chatSection").style.display = "none";
  document.getElementById("favoritesSection").style.display = "block";

  await loadFavorites();

  document.getElementById("favoritesSection").scrollTop = 0;
}
async function loadFavorites() {
  const response = await fetch("/favorites");

  const favorites = await response.json();

  const container = document.getElementById("favoritesList");

  container.innerHTML = "";

  if (favorites.length === 0) {
    container.innerHTML = `
            <p>No favorite places yet ❤️</p>
        `;

    return;
  }

  favorites.forEach((place) => {
    container.innerHTML += `

        <div class="favorite-card">

            <h3>📍 ${place.name}</h3>

            <p><strong>Location:</strong><br>${place.location}</p>

            <button onclick="viewPlace(\`${place.history}\`)">
                View Details
            </button>

        </div>

        `;
  });
}

function viewPlace(history) {
  showChat();

  addMessage(history, "bot");
}

document.getElementById("userInput").addEventListener("keypress", function (e) {
  if (e.key === "Enter") {
    sendMessage();
  }
});

loadFavorites();
