from pydantic import BaseModel
class EmailAgentContext(BaseModel):
    sender: str | None = None
    receiver: str | None = None
    body: str | None = None
    subject: str | None = None