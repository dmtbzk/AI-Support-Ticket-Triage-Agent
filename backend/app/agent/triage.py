from openai import OpenAI
from dotenv import load_dotenv

from app.api.schemas import TicketClassification, ReplyResult, TriageResult
from app.agent.router import route_ticket

load_dotenv()

client = OpenAI()

def classify_ticket(message: str) -> TicketClassification:
    completion = client.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """
            You are a support ticket classifier.

            Return only category, priority, and risk.

            category must be one of:
            Billing, Technical, Account, Product, Security, General

            priority must be one of:
            Low, Medium, High, Urgent
            """
            },
            {
                "role": "user",
                "content": message
            }
        ],
        response_format=TicketClassification,
    )

    return completion.choices[0].message.parsed



def generate_reply(
    message: str,
    category: str,
    priority: str,
    risk: str,
    assigned_team: str
) -> ReplyResult:
    completion = client.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """
            You are a customer support response assistant.

            Write:
            1. A polite reply from the support team to the customer.
            2. A short internal note for the assigned support team.

            Do not write as the customer.
            Keep the customer reply professional and concise.
            """
            },
            {
                "role": "user",
                "content": f"""
            Customer message:
            {message}

            Category:
            {category}

            Priority:
            {priority}

            Risk:
            {risk}

            Assigned team:
            {assigned_team}
            """
            }
        ],
        response_format=ReplyResult,
    )

    return completion.choices[0].message.parsed

def analyze_ticket(message: str) -> TriageResult:
    classification = classify_ticket(message)

    assigned_team = route_ticket(classification.category)

    reply = generate_reply(
        message=message,
        category=classification.category,
        priority=classification.priority,
        risk=classification.risk,
        assigned_team=assigned_team
    )

    return TriageResult(
        category=classification.category,
        priority=classification.priority,
        risk=classification.risk,
        assigned_team=assigned_team,
        customer_reply=reply.customer_reply,
        internal_note=reply.internal_note
    )