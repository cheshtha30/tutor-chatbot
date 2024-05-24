import gradio as gr
from vdb import PineConeRetriver
from embedders import AllMiniLML6V2
from llm import ReplicateLLM
from rag import Prag
system_prompt = """
You are a Admission Q/A Chatbot. Your job is to anwer questions only from the context.
 If there is no context, Tell you are not sure about the information you are telling else
 generate accurate responses.
"""

emb = AllMiniLML6V2()
ret = PineConeRetriver(emb)
llm  = ReplicateLLM("meta/llama-2-13b-chat",system_prompt )

rag = Prag(llm,ret,emb)
def gradio_run():
    with gr.Blocks() as demo:
        chatbot = gr.components. Chatbot (label='Admission Q/A Chatbot', height=600)
        msg = gr.components. Textbox (label='User query')
        clear = gr.components. ClearButton()
        msg.submit(set_user_response, [msg, chatbot], [msg, chatbot], queue=False).then( bot_response, chatbot,chatbot)
        clear.click(lambda: None, None, chatbot, queue=False)
    demo.queue()

    demo.launch(server_name="0.0.0.0")

    
def bot_response(chat_bot):
    user_msg=chat_bot[-1][0]
    chat_bot[-1][1]=""
    res=rag.respond(user_msg)
    
    for event in res:
        chat_bot[-1][1]+=event
        yield chat_bot

def set_user_response(msg,chat_bot):
    chat_bot+=[[msg,None]]
    return '',chat_bot