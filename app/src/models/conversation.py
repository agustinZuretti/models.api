from pydantic import BaseModel

class Conversation(BaseModel):
    role: str
    content: str