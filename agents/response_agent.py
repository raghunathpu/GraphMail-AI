from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from config import GEMINI_API_KEY
from utils.formatter import format_email


def generate_response(
    email: dict,
    summary_data: dict,
    recipient_name: str,
    your_name: str,
    tone: str = "Professional"
):

    summary = summary_data.get("summary", "")
    sentiment = summary_data.get("sentiment", "Neutral")

    prompt_template = PromptTemplate(
        input_variables=[
            "subject",
            "content",
            "summary",
            "sentiment",
            "tone"
        ],
        template="""
You are an email assistant.

Subject:
{subject}

Content:
{content}

Summary:
{summary}

Sender Sentiment:
{sentiment}

Write a {tone} email reply.

Do not include greeting.
Do not include signature.
"""
    )

    prompt = prompt_template.format(
        subject=email.get("subject", ""),
        content=email.get("body", ""),
        summary=summary,
        sentiment=sentiment,
        tone=tone
    )

    model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0.5
    )

    response = model.invoke(prompt)

    response_text = (
        response.content
        if hasattr(response, "content")
        else str(response)
    )

    return format_email(
        email.get("subject", ""),
        recipient_name,
        response_text,
        your_name
    )
