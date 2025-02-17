from pydantic import BaseModel
from typing import List, Optional

# Define incoming data structure
class TemplateRequest(BaseModel):
    coverType: str
    coloringBook: bool = False
    quantity: int = 1
    quantityColoring: int = 1
