from openai import OpenAI
from dotenv import load_dotenv

from app.api.schemas import TriageResult
from app.prompts.triage_prompt import TRIAGE_SYSTEM_PROMPT

load_dotenv()

client = OpenAI()


def analyze_ticket(message: str) -> TriageResult:
    completion = client.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": TRIAGE_SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": message
            }
        ],
        response_format=TriageResult,
    )

    return completion.choices[0].message.parsed