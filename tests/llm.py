
from typing import List

from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from typing import Optional

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
llm = ChatOpenAI(model="gpt-4", temperature=0.2, api_key= api_key) # type: ignore

class Joke(BaseModel):
    is_pre_step: bool = Field(
        description=
            """
            If the form is an email or login form and not directly a job application form.
            """)
    is_application_form: bool = Field(
        description=
            """
            If the information provided is an job application form. 
            """)
    application_link: Optional[str] = Field(
            default='',
            description=
                """
                The link for the applicaiton to apply for the job. 
                """)

    # You can add custom validation logic easily with Pydantic.
    # @validator("setup")
    # def question_ends_with_question_mark(cls, field):
    #     if field[-1] != "?":
    #         raise ValueError("Badly formed question!")
    #     return field

html_tag="""<h1>Jobb hemifrån - Deltid</h1>
<h4>Bara Telecom AB</h4>

<a
	href="https://my.careerhub.se/?adid=129897&amp;worplaceid=&amp;companyid=&amp;source=AMS"
	role="button"
>
	Klicka här för att Ansöka
</a>

<h1>Jobb hemifrån - Deltid</h1>
<p><strong>5 platser</strong></p>
<h3>ANSÖKAN</h3>
Ansök snabbt genom att fylla i din e-post nedan och välj fortsätt.<a></a>

<h4><a href="#aemail"> Ange din e-postadress </a></h4>

<input aria-label="..." placeholder="E-postadress" type="text" />

<button type="submit">Fortsätt</button>

<strong
	>Klicka på länken som har mailats till dig från avsändaren My.Careerhub. Har
	du inte fått någon länk kontrollera att du har angivit rätt e-postadress
	alternativt se om mailet landat i din skräpkorg. Engångskoden på 6 siffror är
	skickad till din e-post
</strong>

<input placeholder="Skriv in din 6-siffriga kod" type="text" />

<button type="submit">Logga in</button>

<button aria-label="Close" type="button">×</button>
"""
# And a query intented to prompt a language model to populate the data structure.
joke_query = f'''
        This is an HTML tag {html_tag} from a website. 
        Analyze it and determine whether this website is one of the following:
        (A) - Job application form where users submit their CVs and information seeking employment.
        (B) - A preliminary step in the job application process where users are asked to submit an email, or to login or create an account.
        (C) - A website with information about the job, including a link to direct users to the application website.
        
        Respond as follows based on your conclusions. You can only have one conclusion; choose the one that best suits this case. 
        
        If (A) set is_application_form to true. Set is_pre_step to false. Set application_link to None
        If (B) set is_application_form to false. Set is_pre_step to true. Set application_link to None.
        If (C) set is_application_form to false. Set is_pre_step to false. Set the application_link.
        If none of (A) or (B) or (C) Set is_application_form to false. Set is_pre_step to false. Set the application_link to None.
        
        '''

# Set up a parser + inject instructions into the prompt template.
parser = PydanticOutputParser(pydantic_object=Joke)

prompt = PromptTemplate(
    template="Answer the user query.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

chain = prompt | llm | parser

a = chain.invoke({"query": joke_query})
print(a)