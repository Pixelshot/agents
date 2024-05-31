# Tool class can only accept one argument
# StructuredTool class can accept multiple arguments
# In our case, we want to accept two arguments: filename and html 
from langchain.tools import StructuredTool
from pydantic.v1 import BaseModel

def write_report(filename, html):
    with open(filename, 'w') as f:
        f.write(html)
        
# A class that describes the different arguments the function above expects to receive
class WriteReportArgsSchema(BaseModel):
    filename: str
    html: str
    
write_report_tool = StructuredTool.from_function(
    name="write_report",
    description="Write an HTML file to disk. Use this tool whenever someone asks for a report.", 
    func=write_report,
    args_schema=WriteReportArgsSchema
)