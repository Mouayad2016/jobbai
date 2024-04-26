from langchain.output_parsers import PydanticOutputParser
from .schema.file_upload import DetermineFileUpload
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

parser = PydanticOutputParser(pydantic_object=DetermineFileUpload)

def determin_file_upload(html_tag):
	prompt = PromptTemplate(
		template="Answer the user query.\n{format_instructions}\n{query}\n",
		input_variables=["query"],
		partial_variables={"format_instructions": parser.get_format_instructions()},
	)

	load_dotenv()
	api_key = os.getenv('OPENAI_API_KEY')

	llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2, api_key= api_key) # type: ignore

	chain = prompt | llm | parser


	result = chain.invoke({"query": f'''
		
	This is an HTML tag {html_tag} from a website. Determine the method used to upload documents and choose one of the following options in your answer:

	(A): Input tags have an attribute type as 'file'.
	(B): A button has JavaScript functions that handle file uploads and the input tag does not have a 'file' type.
	
 	If (A), set js_file_upload to false.
	If (B), set js_file_upload to true.
  
		'''})
 
	print(result)






