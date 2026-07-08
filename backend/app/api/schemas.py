from pydantic import BaseModel


class TicketRequest(BaseModel):
    message: str


class TriageResult(BaseModel):
    category: str
    priority: str
    risk: str
    assigned_team: str
    customer_reply: str
    internal_note: str


class TicketResponse(BaseModel):
    result: TriageResult