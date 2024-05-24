
from config import SECRETS,SETTINGS
import replicate
from replicate.stream import ServerSentEvent





class ReplicateLLM:
    def __init__(self,model_name,system_prompt,**kwargs) :
        
        self.messages = []
        self.system_prompt=system_prompt
        self.prompt = ""
        self.kwargs = kwargs
        self.model_name = model_name

    
    def add_message(self,msg):
       
        if len(self.messages)>9:
            self.messages=self.messages[2:]
        self.messages.append(msg)
        self.prompt=self.getPromptFromMessages()
        
        
    
    def getPromptFromMessages(self):
        prompt=""
        for msg in self.messages:
            if msg["isUser"]:
                prompt += f"[INST] {msg['message']} [ /INST ] \n"
            else:
                prompt += msg["message"] + "\n"
        return prompt


    def respond(self, query):
    

        self.add_message({"isUser":True, "message":query})
        


        input={
        "debug": self.kwargs.get("debug", False),
        "top_p": self.kwargs.get("top_p", 1),
        "prompt": self.prompt,
        "temperature": self.kwargs.get("temperature", 0.7),
        "system_prompt": self.system_prompt,
        "max_new_tokens": self.kwargs.get("max_new_tokens", 600),
        "min_new_tokens": self.kwargs.get("debug", -1),
        "prompt_template": "<<SYS>>\n{system_prompt}\n<</SYS>>\n\n{prompt} ",
        "repetition_penalty": self.kwargs.get("debug", 1)
    }
        stream=False
        if stream:
            gen = replicate.stream(self.model_name, input=input)

            model_response = ""
            for event in gen:
                if event.event == ServerSentEvent.EventType.DONE:
                    self.add_message({"isUser":False, "message":model_response})

                    yield "[DONE]"

                token = str(event)
                model_response += token
                yield token
        else:

            gen = replicate.run(self.model_name, input=input)

            model_response = ""
            for event in gen:
            

                token = str(event)
                model_response += token
                yield token
            yield "[DONE]"
      