from langchain.callbacks.base import BaseCallbackHandler

# It's not always apparent with what's going on with our program even if with verbose=True. Another way of gaining more information is by creating a custom Class to inspect what's happening inside of our program.
# See # 63/64 for explanation on creating custom Class.
class ChatModelStartHandler(BaseCallbackHandler):
    # These arguments(methods) are names are specific.
    # Click cmd click on BaseCallbackHandler to see the methods that are available to use.
    # Most of the time we don't have to worry about serialized.
    def on_chat_model_start(self, serialized, messages, **kwargs):
        print(messages)