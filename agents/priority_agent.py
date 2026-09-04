from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from config import GEMINI_API_KEY


def calculate_priority(email: dict) -> int:

    prompt = PromptTemplate(
        input_variables=["subject", "content"],
        template="""
Rate the urgency of this email from 1 to 10.

1 = not important
10 = extremely urgent

Subject:
{subject}

Content:
{content}

Return ONLY a number.
"""
    )

    formatted = prompt.format(
        subject=email.get("subject", ""),
        content=email.get("body", "")
    )

    model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0.2
)

    response = model.invoke(formatted)

    text = (
        response.content
        if hasattr(response, "content")
        else str(response)
    )

    try:
        return int(text.strip())
    except:
        return 5
