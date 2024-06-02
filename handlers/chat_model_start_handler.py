from langchain.callbacks.base import BaseCallbackHandler
from pyboxen import boxen # This package creates a nice display box in the terminal.

def boxen_print(*args, **kwargs):
    print(boxen(*args, **kwargs))

# boxen_print("Test message", title="Title", color="green")

# It's not always apparent with what's going on with our program even if with verbose=True. Another way of gaining more information is by creating a custom Class to inspect what's happening inside of our program.
# See # 63/64 for explanation on creating custom Class.
class ChatModelStartHandler(BaseCallbackHandler):
    # These arguments(methods) are names are specific.
    # Click cmd click on BaseCallbackHandler to see the methods that are available to use.
    # Most of the time we don't have to worry about serialized.
    def on_chat_model_start(self, serialized, messages, **kwargs):
        # print("\n\n\n\n========= Sending Messages =========\n\n\n\n")
        boxen_print("========= Sending Messages =========", title="Info", color="red")
        
        for message in messages[0]:
            # print(message.type)
            if message.type == "system":
                boxen_print(message.content, title=message.type, color="yellow")
                
            elif message.type == "human":
                boxen_print(message.content, title=message.type, color="green")
            
            #ChatGPT has two probabilities, the result that it produces or a function that it wants to run. # 65    
            elif message.type == "ai" and "function_call" in message.additional_kwargs:
                call = message.additional_kwargs["function_call"]
                boxen_print(f"Running too {call['name']} with args {call['arguments']}"),
                title=message.type,
                color="cyan"
                
                
            elif message.type == "ai":
                boxen_print(message.content, title=message.type, color="blue")
                
            elif message.type == "function":
                boxen_print(message.content, title=message.type, color="purple")
                
            else:
                boxen_print(message.content, title=message.type)