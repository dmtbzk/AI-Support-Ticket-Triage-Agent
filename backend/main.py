from fastapi import FastAPI

from app.api.schemas import TicketRequest, TicketResponse
from app.agent.triage import analyze_ticket

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/triage", response_model=TicketResponse)
def triage_ticket(request: TicketRequest):
    result = analyze_ticket(request.message)

    return TicketResponse(result=result)