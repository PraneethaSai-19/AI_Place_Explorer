import ollama
print("THE PLACE EXPLORER")
print()
print("Enter 'exit' or 'quit' to stop.")

while True:
    user_input = input("USER: ").lower()
    if user_input in ["exit" , "quit" , "bye"] :
        print("AGENT : GOODBYE , hope you travel the world ;) ")
        break
    if not user_input:
        print("Please Type Something!")
        
    prompt = f"""
You are Place Explorer AI.

User Request:
{user_input}

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
- Mention:
    • Place Name
    • State/Country
    • Short history 
    • Why it is famous
      Give Story of the place in 5-6 lines
    • Exact location (city/state or coordinates if known)
- Do not invent facts.
- Do not mention that you are an AI.
"""
    responses=ollama.chat(
        model="llama3.2",
        messages=[
            {"role":"user","content":prompt}
        ]
    )
    
    print("Agent: ",end="")
    print(responses.message.content)