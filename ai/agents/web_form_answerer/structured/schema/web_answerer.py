from typing import List

from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Optional


class FromAnswers(BaseModel):
    """Final response to the question being asked"""
    application_answers: dict[str, str]  = Field(
        description=
            """
            Map with keys and values where the keys are the tag IDs and the values are the answers for each tag ID.
            """)

