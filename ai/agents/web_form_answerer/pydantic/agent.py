from langchain.output_parsers import PydanticOutputParser
from .schema.web_answerer import FromAnswers
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os


first_name = "Mouayad"
last_name = "Mouayad"
phone_number= "+46 733 524 957"
address = "Visättravägen 12 lgh 1401, 141 50 Huddinge"
studies = "Computer Science at Dalarna University"
date_of_birth = "19980103"
e_mail = "mouayad1998@hotmail.com"
cv=('/Users/mouayadmouayad/Desktop/jobbAI/ai/agents/web_form_answerer/pydantic/Arbetsgivarintyg.pdf')
cover_letter=('/Users/mouayadmouayad/Desktop/jobbAI/ai/agents/web_form_answerer/pydantic/Arbetsgivarintyg.pdf')


applicant_information= f"""
First name: {first_name}
Last name: {last_name}
Date of birth: {date_of_birth}
Phone number: {phone_number}
Address: {address}
Studies: {studies}
e-mail:{e_mail}
coverletter: {cover_letter}
cv:{cv}""" 

parser = PydanticOutputParser(pydantic_object=FromAnswers)

def web_form_answerer(html_tag):
	prompt = PromptTemplate(
		template="Answer the user query.\n{format_instructions}\n{query}\n",
		input_variables=["query"],
		partial_variables={"format_instructions": parser.get_format_instructions()},
	)

	load_dotenv()
	api_key = os.getenv('OPENAI_API_KEY')

	llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2, api_key= api_key) # type: ignore

	chain = prompt | llm | parser

	print("web_form_answerer agent strated ---")
	result = chain.invoke({"query": f'''
		
		This is an HTML tag {html_tag} from a website. 
		Do the following:
		
		Determine the answers for each question necessary to complete the application. Base your answers on this information info_A:{applicant_information}. 
  		Respond with a map of each tag's ID and its corresponding answer like this example: {{"ID":"Answer"}}.
		
  		- If you don't know the answer, provide a generate a response based on info_A. Set the tag ID or name as the key and set the generated answer as the value.
        - If the input has a type attribute 'file'. Set the tag ID or name as the key, and set the file path as the value.
        
        - If the tag is a form submition tag. Set the tag ID or name as the key. Set 'submit' as the value.
        
        - If the input has a type 'checkbox' Set the ID to the input's ID or name if the ID is not specified and set value to 'checkbox'.

		'''})
 
	print("web_form_answerer agent finito ---")
	return result;
 
