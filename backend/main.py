from fastapi import FastAPI

from app.api.schemas import TicketRequest, TicketResponse

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/triage", response_model=TicketResponse)
def triage_ticket(request: TicketRequest):
    return TicketResponse(result=request.message)