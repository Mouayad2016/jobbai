from langchain_openai import ChatOpenAI
from ...tool import get_word_length
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv
import os
from .schema.post_anlyzer import JobPostAnlyzerResponse

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2, api_key= api_key) # type: ignore

tools = [JobPostAnlyzerResponse]

llm_with_tools = llm.bind_functions(tools)
system_input_1 = "You are an analyzer tasked with analyzing text to extract relevant information for job applications. Sometimes, the text specifies that a reference is required, and other times it does not. Your role is to identify the necessary information from the provided text and include it in your response."
system_input_2 = "You are an analyzer and will help me extract information from a given HTML code. You should extract the email and check if there is a reference to be sent with the given email and extract both."

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_input_1),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)


