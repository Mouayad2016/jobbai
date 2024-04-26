from typing import List

from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Optional


class DetermineFileUpload(BaseModel):
    """Final response to the question being asked"""
    js_file_upload: bool = Field(
        description=
            """
            Value if the file upploads is using JS insted of regular input type 'file' html tag
            
            """)

