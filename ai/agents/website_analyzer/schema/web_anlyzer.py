from typing import List

from langchain_core.pydantic_v1 import BaseModel, Field


class JobPostAnlyzerResponse(BaseModel):
    """Final response to the question being asked"""
    is_application_form: bool = Field(
        description=
            """
            If the information provided is an job application form or not, this can only be true or false
            """)
    application_link: str = Field(
            description=
                """
                The link for the applicaiton to apply for the job this can be None if is_application_form = true
                """)