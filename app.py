from flask import Flask, render_template, request, jsonify
import ollama

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    user_input = request.json["message"]

    prompt = f"""
    
You are Place Explorer AI.



Your job is to identify what the user wants and answer directly.

Instructions:
- Never ask follow-up questions.
- Never ask for clarification.
- Never say "I'd love to help."
- Never say "What would you like to know?"
- Always provide the requested information immediately.
- Only mention real places that exist on Earth.
- If the user asks for N places, return exactly N places.
- If no such place exists, reply:
"There is no such place on Earth."
- Be concise and informative.
- Add Related emojis to your responses.
-if user greets you Reply ONLY with a short greeting and introduction like "Hi! 👋 I'm Place Explorer AI. How can I help you today?"
- Mention:
    • Place Name
    • State/Country
    • Short history 
    • Why it is famous
      Give Story of the place in 5-6 lines
    • Exact location (city/state or coordinates if known)
- Do not invent facts.
- Do not mention that you are an AI.


    User Request:
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

    return jsonify({
        "response": response.message.content
    })


if __name__=="__main__":
    app.run(debug=True)