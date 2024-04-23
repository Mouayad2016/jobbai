from typing import List

from langchain_core.pydantic_v1 import BaseModel, Field


class JobPostAnlyzerResponse(BaseModel):
    """Final response to the question being asked"""
    reference: str = Field(
        description=
            """
            This should include any relevant information for the e-mail like specific case, reference, title or text to state or to mention. If empty this should be None
            """)
    last_date: str = Field(description="Last date for the applicaiton in this format dd/mm/yyyy")
    e_mail: str = Field(
        description="the email account"
    )