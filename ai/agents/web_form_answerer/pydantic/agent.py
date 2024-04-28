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
date_of_birth = "1998-01-03"
e_mail = "mouayad1998@hotmail.com"
cv=('/Users/mouayadmouayad/Desktop/CVs/cv/IT/General/Mouayad-Mouayad-Full-Stack-Developer.docx')
cover_letter=('/Users/mouayadmouayad/Desktop/CVs/cv/IT/General/Personlig brev Mouayad Mouayad .pdf')
desired_salary= '40 000 SEK'
year_experience= '3'
locations =['Stockholm', 'Gothenbug']
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
Desired salary: {desired_salary}
Locations: {locations}
Year of experience: {year_experience}
""" 

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
		(A): Base on this information info_A:{applicant_information} Determine the answers for each question necessary to complete the application.
		(B): Respond with a map of each tag's identifier this can include attributes as (id, name, value) use it as key and use its corresponding answer as a value.
		
	   
		Use the following roles as guide to how to fill the map:
  		- If you don't know the answer, provide a generate a response based on info_A. Set the tag identifier as a key and set the generated answer as the value.
        - If the input has a type attribute 'file'. Set the tag identifier as a key. Choose the correct file path from info_A and set it as value.
        - If the input has a type 'checkbox' Set the identifier as the key and set value to 'checkbox'.
        
        Dot not edit or manipulate and HTML tag identifier.
        Always include the correct HTML tag identifier as its specified in the HTML tag exactly as it's written in HTML tag. 
        Do not generate file Paths use it as it's written in info_A. 
        
        Never break this roles. 
		'''})
 
	print("web_form_answerer agent finito ---")
	return result;
 
# - If the tag is a form submition tag. Set the identifier as the key. Set 'submit' as the value.
#- If the input has a type attribute 'date'. Set the tag identifier as a key. Answer is this format yyyy-mm-dd. Set the answer as the value.
