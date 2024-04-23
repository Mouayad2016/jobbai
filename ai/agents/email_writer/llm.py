from langchain_openai import ChatOpenAI
from ...tool import get_word_length
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv
import os
from .schema.mail import Response

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0,api_key= api_key) # type: ignore

tools = [Response]

llm_with_tools = llm.bind_functions(tools)

name = "Mouayad Mouayad"
phone = "+46 733 524 957"
address = "Stockholm"
studies = "Computer Science at Dalarna University"
years_of_experience = "5 years of experience as a Fullstack Developer"


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", f'You are a job seeker. Your name is {name}, and your contact number is {phone}. You live in {address} and have a background in {studies} with {years_of_experience}. You are looking for a job and are writing emails for job seeking. Dont be too formal; use casual, human language while always being respectful when writing emails. Never break your character'),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)


