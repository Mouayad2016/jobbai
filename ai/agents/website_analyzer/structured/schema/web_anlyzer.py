from typing import List

from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Optional


class JobPostAnlyzerResponse(BaseModel):
    """Final response to the question being asked"""
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
    application_link: str = Field(
        description=
            """
            The link for the applicaiton to apply for the job. 
            """)
    
