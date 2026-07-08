from fastapi import FastAPI

from app.api.schemas import TicketRequest, TicketResponse, TriageResult

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/triage", response_model=TicketResponse)
def triage_ticket(request: TicketRequest):
    result = TriageResult(
        category="Billing",
        priority="High",
        risk="Payment dispute",
        assigned_team="Finance Support",
        customer_reply="I'm sorry to hear about the payment issue. Our finance support team will review this urgently.",
        internal_note=f"Customer reported: {request.message}"
    )

    return TicketResponse(result=result)