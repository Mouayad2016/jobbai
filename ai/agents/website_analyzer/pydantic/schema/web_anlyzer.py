from typing import List

from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Optional


class Response(BaseModel):
    """Final response to the question being asked"""
    is_auth: bool = Field(
        description=
            """
            If the form is an email or login form and not directly a job application form.
            """)
    is_application_form: bool = Field(
        description=
            """
            If the information provided is an job application form. 
            """)
    application_button_tag_id: Optional[str] = Field(
        default=None,  # Sets the default value to None if not provided
        description=
            """
            Application button tag identifier         
            
            """)
    application_link: Optional[str] = Field(
        default=None,  # Sets the default value to None if not provided
        description="The link for the application to apply for the job.")

