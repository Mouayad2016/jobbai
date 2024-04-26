from langchain_openai import ChatOpenAI
from ....tool import get_word_length
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv
import os
from .schema.web_answerer import FromAnswers

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2, api_key= api_key) # type: ignore

tools = [FromAnswers]

llm_with_tools = llm.bind_functions(tools)

first_name = "Mouayad"
last_name = "Mouayad"
phone_number= "+46 733 524 957"
address = "Visättravägen 12 lgh 1401, 141 50 Huddinge"
studies = "Computer Science at Dalarna University"
date_of_birth = "19980103"
e_mail = "mouayad1998@hotmail.com"
cv="./cv.pdf"
cover_letter="./cover_letter.pdf"

applicant_information= f"""
First name: {first_name}
Last name: {last_name}
Date of birth: {date_of_birth}
Phone number: {phone_number}
Address: {address}
Studies: {studies}
e-mail:{e_mail}
coverletter: {cover_letter}
cv:{cv}


""" 


system_input_1 = f""" 
                You are a helpful assistant that works to analyze the information provided from a given HTML code. 
                This is your information.{applicant_information}
                
                """

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_input_1),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)


