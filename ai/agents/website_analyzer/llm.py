from langchain_openai import ChatOpenAI
from ...tool import get_word_length
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv
import os
from .schema.web_anlyzer import JobPostAnlyzerResponse

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

llm = ChatOpenAI(model="gpt-4-turbo", temperature=0.2, api_key= api_key) # type: ignore

tools = [JobPostAnlyzerResponse]

llm_with_tools = llm.bind_functions(tools)
system_input_1 = """ 
                You are a helpful assistant that works to analyze the information provided from a given HTML code. 
                """

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_input_1),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)


