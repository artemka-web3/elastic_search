from pydantic import BaseModel
from typing import List

class TextInput(BaseModel):
    text: str

class CreateDoc(BaseModel):
    text: str
    rubrics: List[str]