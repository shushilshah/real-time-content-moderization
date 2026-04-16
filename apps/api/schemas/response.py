# Auto-generated file
from pydantic import BaseModel

class ModerationResponse(BaseModel):
    toxicity: float
    label: str
    action: str
    