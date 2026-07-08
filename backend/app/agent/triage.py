from openai import OpenAI
from dotenv import load_dotenv

from app.api.schemas import TicketClassification, ReplyResult, TriageResult
from app.agent.router import route_ticket
from app.prompts.triage_prompt import (
    CLASSIFIER_SYSTEM_PROMPT,
    REPLY_SYSTEM_PROMPT,
)
from app.knowledge.loader import load_knowledge

load_dotenv()

client = OpenAI()

def classify_ticket(message: str) -> TicketClassification:
    completion = client.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": CLASSIFIER_SYSTEM_PROMPT
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
    knowledge = load_knowledge(category)
    completion = client.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": REPLY_SYSTEM_PROMPT
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

            Company knowledge
            {knowledge}
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