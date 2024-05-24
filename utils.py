

# Formatting function for message and history
def format_message(message: str, history: list, memory_limit: int = 3) -> str:
   
     

    SYSTEM_PROMPT = """<s>[INST] <<SYS>>
    You are a Admission Q/A Chatbot. Your answers should be clear and concise.
    <</SYS>>
    """
    
   
    # always keep len(history) <= memory_limit
    if len(history) > memory_limit:
        history = history[-memory_limit:]

    if len(history) == 0:
        return SYSTEM_PROMPT + f"{message} [/INST]"

    formatted_message = SYSTEM_PROMPT + f"{history[0][0]} [/INST] {history[0][1]} </s>"

    # Handle conversation history
    for user_msg, model_answer in history[1:]:
        formatted_message += f"<s>[INST] {user_msg} [/INST] {model_answer} </s>"

    # Handle the current message
    formatted_message += f"<s>[INST] {message} [/INST]"

    return formatted_message