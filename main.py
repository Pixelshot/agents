from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder
)
from langchain.schema import SystemMessage # This class allows us to create a plain simple system message that doesn't require input message or templating. See # 56
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from langchain.memory import ConversationBufferMemory # Maintains a buffer of recent messages to preserve conversation context and ensure coherent, contextually aware dialogues.
from dotenv import load_dotenv

from tools.sql import run_query_tool, list_tables, describe_tables_tool
from tools.report import write_report_tool
load_dotenv()

chat = ChatOpenAI()
tables = list_tables()
prompt = ChatPromptTemplate(
    messages=[
        # Persona
        SystemMessage(content=(
            "You are an AI that has access to a SQLite database.\n"
            f"The database has tables of: {tables}\n"
            "Do not make any assumptions about what tables exist or what columns exist. Intead use the 'describe_tables' function" # Ensures that GPT doesn't make any assumptions about the database
        )),
        MessagesPlaceholder(variable_name="chat_history"), # Dynamically inserts the conversation history from ConversationBufferMemory into the prompt, ensuring contextually aware and coherent responses.
        HumanMessagePromptTemplate.from_template(
            "{input}"),
        # The goal of MessagesPlaceholder is to take in input variable and expand into new list of messages 
        # agent_scratchpad is a special variable name that needs to be called in variable_name. Giving variable_name any other name will not work
        # agent_scratchpad is very similar to a memory 
        MessagesPlaceholder(variable_name="agent_scratchpad") 
    ]
)
# return_messages = Return the stored messages as a list of message objects rather than as a single concatenated string.
# This memory is used inside of agent_executor so that the agent can remember the conversation history.
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

tools = [run_query_tool, describe_tables_tool, write_report_tool]

agent = OpenAIFunctionsAgent(
    llm=chat,
    prompt=prompt,
    tools=tools
)

agent_executor = AgentExecutor(
    agent=agent,
    verbose=True, 
    tools=tools,
    memory=memory
)

agent_executor(
    "How many orders are there? Write the result to an html report."
)
agent_executor(
    "Repeat the exact same process for users."
)
# agent_executor("How many users are in the database?")
# agent_executor("How many users have provided a shipping address?")
# agent_executor("Summarize the top 5 most popular products. Write the results to a report file.")