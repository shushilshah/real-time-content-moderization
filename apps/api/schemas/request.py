# Auto-generated file
from pydantic import BaseModel, Field

class ModerationRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000, description="Input text to moderate")