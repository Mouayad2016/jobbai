from typing import List

from langchain_core.pydantic_v1 import BaseModel, Field


class Response(BaseModel):
    """Final response to the question being asked"""

    title: str = Field(description="The email title")
    mail: str = Field(
        description="The email body text"
    )