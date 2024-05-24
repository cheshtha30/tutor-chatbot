import gradio as gr
from llm import get_llama_response



gr.ChatInterface(get_llama_response).queue().launch(share=True,debug=True)
