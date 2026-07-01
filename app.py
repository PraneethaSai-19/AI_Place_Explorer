from flask import Flask, render_template, request, jsonify
import ollama
import json
import os

app = Flask(__name__)

current_place = {}
FAVORITES_FILE = "favorites.json"
def load_favorites():
    if not os.path.exists(FAVORITES_FILE):
        return []
    with open(FAVORITES_FILE, "r") as f:
        return json.load(f)

def save_favorites(data):
    with open(FAVORITES_FILE, "w") as f:
        json.dump(data, f, indent=4)
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/chat", methods=["POST"])
def chat():
    global current_place
    user_input = request.json["message"]
    save_commands = [
        "save this place",
        "save this",
        "save it",
        "bookmark this place",
        "bookmark it",
        "favorite this place",
        "add this to favorites",
        "add to favorites"
    ]
    if user_input.lower() in save_commands:
        if current_place == {}:
            return jsonify({
                "response":"There is no place to save."
            })
        print(current_place)
        favorites = load_favorites()
        already_exists = any(
            place["name"].lower() == current_place["name"].lower()
            for place in favorites
        )
        if already_exists:
            return jsonify({
                "response":"⭐ This place is already in your favorites."
            })
        favorites.append(current_place)
        save_favorites(favorites)
        return jsonify({
            "response":f"✅ {current_place['name']} has been added to Favorites."
        })
    prompt = f"""
You are a Perfect Place Explorer AI.

The user has already asked a question.

Answer the question directly.

Rules:

- Never ask follow-up questions.
- Never introduce yourself or greet user when user asks any question.
- Never ask "What would you like to know?"
- Never ask for clarification.
- Never greet unless the user ONLY says:
  hi
  hello
  hey
  good morning
  good evening

If the user greets Reply ONLY:
"Hi! 👋 I'm Place Explorer AI. How can I help you today?"

Otherwise answer directly.
Mention only REAL places.
For every place provide:

Place Name
State/Country
Short History
Why Famous
Story
Exact Location

Never invent facts.

Never mention you are an AI.
Rule :
- Don't add unnecessary details when you greet user back just say "Hi! 👋 I'm Place Explorer AI. How can I help you today?"
- add relevant emojis .
- Don't hallucinate .
- Provide correct details and location.
User:
{user_input}
"""
    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]
    )

    ai_response = response.message.content.strip()
    print(ai_response)

    current_place = {
        "name": "Unknown",
        "location": "Unknown",
        "history": ai_response
    }

    lines = [line.strip() for line in ai_response.split("\n") if line.strip()]
    if len(lines) > 0:
        current_place["name"] = lines[0].replace("📍", "").strip()
    for line in lines:
        if "Exact Location" in line:
            if ":" in line:
                current_place["location"] = line.split(":", 1)[1].strip()
            break
    print(current_place)
    return jsonify({
        "response": ai_response
    })

@app.route("/favorites", methods=["GET"])
def favorites():
    return jsonify(load_favorites())

if __name__=="__main__":
    app.run(debug=True)