# Auto-generated file
from pydantic import BaseModel

class ModerationResponse(BaseModel):
    request_id: str
    toxicity: float
    label: str
    action: str
    