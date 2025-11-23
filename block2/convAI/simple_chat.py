# Simple Chat with ChainLit

# Use Chainlit + Ollama 
# The Ollama REST API will be available at http://localhost:11434.
# Run the Chainlit app:
#   chainlit run app.py
# run chainlit (opens http://localhost:8000)

import os
import chainlit as cl
from ollama import Client

# Configuration (can be overridden with env vars)
BASE_URL = os.getenv("BASE_URL", "http://localhost:11434")
MODEL = os.getenv("MODEL", "llama3.2")

client = Client(host=BASE_URL)


# Hilfsfunktion: History aus Session holen
def get_history():
    return cl.user_session.get("history", [])

# Hilfsfunktion: History speichern
def add_to_history(role, content):
    history = cl.user_session.get("history", [])
    history.append({"role": role, "content": content})
    cl.user_session.set("history", history)


def generate(prompt: str, model: str):
    history = get_history()
    full_prompt = ""
    for h in history:
        full_prompt += f"{h['role']}: {h['content']}\n"
    full_prompt += f"user: {prompt}\nassistant:"

    try:
        for chunk in client.generate(model=model, prompt=full_prompt, stream=True):
            # each chunk is a dict with a 'response' token
            yield chunk.get("response", "")
    except Exception as e:
        yield f"Error calling Ollama: {e}"

@cl.on_chat_start
async def on_chat_start():
    """Send a welcome message when the user opens a new chat session."""
    #cl.user_session.set("history", []) 
    await cl.Message(content=(
        "Hi — I'm a Chainlit app using Ollama as the LLM backend."
        f"I use the following model {MODEL}."
    )).send()

@cl.on_message
async def on_message(message: cl.Message):
    prompt = message.content
    # User-Eingabe zur History hinzufügen
    add_to_history("user", prompt)

    # message that will receive streamed tokens
    msg = cl.Message(content="")
    await msg.send()

    # stream tokens into the Chainlit message
    final_answer = ""
    for token in generate(prompt, MODEL):
        final_answer += token
        await msg.stream_token(token)

    # finalize message (optional but clean)
    await msg.update()

    add_to_history("assistant", final_answer)


if __name__ == "__main__":
    # Running via `python app.py` is not the standard Chainlit workflow, but we keep
    # this guard to allow running lints or tests on the file.
    print("This file is a Chainlit app. Run with: chainlit run app.py")

