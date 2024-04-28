from langchain.output_parsers import PydanticOutputParser
from .schema.web_anlyzer import Response
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os


parser = PydanticOutputParser(pydantic_object=Response)

def web_analize(html_tag):
	prompt = PromptTemplate(
		template="Answer the user query.\n{format_instructions}\n{query}\n",
		input_variables=["query"],
		partial_variables={"format_instructions": parser.get_format_instructions()},
	)

	load_dotenv()
	api_key = os.getenv('OPENAI_API_KEY')

	llm = ChatOpenAI(model="gpt-4-turbo", temperature=0, api_key= api_key) # type: ignore

	chain = prompt | llm | parser

	print("web_form_answerer agent strated ---")
	result = chain.invoke({"query": f'''
        This is an HTML tag {html_tag} from a website. 
        Analyze it and determine whether this website is one of the following:
        (A) - Job application form where users submit their CVs and information seeking employment.
        (B) - A preliminary step in the job application process where users are asked to submit an email, or to login or create an account.
        (C) - A website with information about the job, including a link to direct users to the application website.
        (D) - Not (A). Not (B). Not (C). Has a button to apply
        
        Respond as follows based on your conclusions. You can only have one conclusion; choose the one that best suits this case: 
        
        If (A) set is_application_form to 'true'. Set is_auth to 'false'. Set application_link to 'null'. Set application_button_tag_id to 'null'
        If (B) set is_application_form to 'false'. Set is_auth to 'true'. Set application_link to 'null'. Set application_button_tag_id to 'null'
        If (C) set is_application_form to 'false'. Set is_pre_step to 'false'. Set the application_link.
        If none of (A) or (B) or (C) Set is_application_form to 'false'. Set is_auth to 'false'. Set the application_link to 'null'. Set application_button_tag_id to apply button tag identifier this includes (id, name, value)
        
        Always follow the predeiged analysis steps and never break them
        '''
        })
 
	print("web_form_answerer agent finito ---")
	return result;
 
# - If the tag is a form submition tag. Set the identifier as the key. Set 'submit' as the value.
#- If the input has a type attribute 'date'. Set the tag identifier as a key. Answer is this format yyyy-mm-dd. Set the answer as the value.
