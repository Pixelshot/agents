from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder
)
from langchain.schema import SystemMessage # This class allows us to create a plain simple system message that doesn't require input message or templating. See # 56
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from dotenv import load_dotenv

from tools.sql import run_query_tool, list_tables, describe_tables_tool

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
        HumanMessagePromptTemplate.from_template(
            "{input}"),
        # The goal of MessagesPlaceholder is to take in input variable and expand into new list of messages 
        # agent_scratchpad is a special variable name that needs to be called in variable_name. Giving variable_name any other name will not work
        # agent_scratchpad is very similar to a memory 
        # The goal of agent_scratchpad is to store all "history" messages leading up to the output function that ChatGPT will return 
        MessagesPlaceholder(variable_name="agent_scratchpad") 
    ]
)

tools = [run_query_tool, describe_tables_tool]

agent = OpenAIFunctionsAgent(
    llm=chat,
    prompt=prompt,
    tools=tools
)

agent_executor = AgentExecutor(
    agent=agent,
    verbose=True, 
    tools=tools
)

# agent_executor("How many users are in the database?")
agent_executor("How many users have provided a shipping address?")