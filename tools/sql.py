import sqlite3
# Pydantic is a library that allows us to annotate different classes inside of a python class and more clearly describe what kinds of data we expect that class to receive as attributes. See #59
from pydantic.v1 import BaseModel 
from typing import List
from langchain.tools import Tool

# See # 51
conn = sqlite3.connect('db.sqlite')

def list_tables():
    c = conn.cursor() 
    c.execute("SELECT name FROM sqlite_master WHERE type='table';") # Shows all the tables in the database
    rows = c.fetchall()
    return "\n".join([row[0] for row in rows if row[0] is not None]) # Formats the output to be more readable. Also affects how well GPT interprets the output

def run_sqlite_query(query):
    c = conn.cursor() # An object that allows us to gain access to the database. See # 55
    try:
        
        c.execute(query) # Access to the database
        return c.fetchall() # Fetches all the results of the query. The information received here is the one that will be transferred to GPT
    except sqlite3.OperationalError as err:
        return f"The following error occured: {str(err)}" # Stringify the error message

# This is creating a "record" inside of our program that says if you want to run this class, you must provide a query attribute that is a string
# This class is then used in run_query_tool
# Langchain will use this query: str to better describe the different arguments that ChatGPT should be providing to our tool
# See # 59
class RunQueryArgsSchema(BaseModel):
    query: str

run_query_tool = Tool.from_function(
    # name and description is mandatory
    name="run_sqlite_query",
    description="Run a query on the sqlite database",
    # The function that will be called ChatGPT runs the run_sqlite_query tool
    func=run_sqlite_query,
    args_schema=RunQueryArgsSchema
)

# As explained above in the RunQueryArgsSchema class, this class is used to guide ChatGPT into providing the correct arguments to the describe_tables() function
class DescribeTablesArgsSchema(BaseModel):
    table_names: List[str]

# This function formats the table names from the database that will be used in the ChatGPT prompt. It further formats the result from list_tables().
def describe_tables(table_names):
    c = conn.cursor()
    tables = ', '.join("'" + table + "'" for table in table_names)
    rows = c.execute(f"SELECT sql FROM sqlite_master WHERE type='table' and name IN ({tables});")
    return '\n'.join([row[0] for row in rows if row[0] is not None])

# Wrapping describe_tables() in a Tool object
describe_tables_tool = Tool.from_function(
    name="describe_tables",
    description="Given a list of table names, returns the schema of those tables",
    func=describe_tables,
    args_schema=DescribeTablesArgsSchema
)