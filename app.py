import os
from openai import OpenAI
from context import TWIN_SYSTEM_PROMPT
from tools import tools, handle_tool_calls
from styles import CSS, JS, THEME, HEADER, PLACEHOLDER, EXAMPLES
from dotenv import load_dotenv
import gradio as gr

load_dotenv(override=True)

# Groq speaks the OpenAI API, so the same client works with a different base_url + key
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
MODEL_NAME = "openai/gpt-oss-120b"

openai = OpenAI(base_url=GROQ_BASE_URL, api_key=os.getenv("GROQ_API_KEY"))

system = [{"role": "system", "content": TWIN_SYSTEM_PROMPT}]


def chat(message, history):
    # Gradio's history dicts carry extra keys (metadata, options). OpenAI ignores them,
    # Groq rejects them with a 400 — so keep only what the API expects.
    history = [{"role": m["role"], "content": m["content"]} for m in history]
    messages = system + history + [{"role": "user", "content": message}]
    response = openai.chat.completions.create(model=MODEL_NAME, messages=messages, tools=tools)
    while response.choices[0].finish_reason == "tool_calls":
        message = response.choices[0].message
        tool_calls = message.tool_calls
        results = handle_tool_calls(tool_calls)
        messages.append(message)
        messages.extend(results)
        response = openai.chat.completions.create(model=MODEL_NAME, messages=messages, tools=tools)
    return response.choices[0].message.content


if __name__ == "__main__":
    with gr.Blocks(title="Sameer Ahmed · AI twin", fill_height=True) as demo:
        gr.HTML(HEADER)
        gr.ChatInterface(
            chat,
            examples=EXAMPLES,
            fill_height=True,
            chatbot=gr.Chatbot(
                show_label=False,
                placeholder=PLACEHOLDER,
                elem_classes="twin-chat",
                scale=1,
            ),
            textbox=gr.Textbox(placeholder="Ask me anything…", submit_btn=True),
        )
    # Render (and most hosts) set PORT and route traffic in from outside, so listen on
    # all interfaces there. Locally PORT is unset and Gradio keeps 127.0.0.1:7860.
    port = os.getenv("PORT")
    demo.launch(
        css=CSS,
        js=JS,
        theme=THEME,
        server_name="0.0.0.0" if port else None,
        server_port=int(port) if port else None,
    )
