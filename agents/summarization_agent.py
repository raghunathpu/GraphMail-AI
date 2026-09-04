from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from config import GEMINI_API_KEY
from utils.formatter import clean_text
import json


def summarize_email(email: dict) -> dict:

    prompt_template = PromptTemplate(
        input_variables=["content"],
        template="""
Analyze the following email.

Email:
{content}

Return JSON only in this format:

{{
    "summary": "short summary",
    "sentiment": "Positive | Neutral | Negative",
    "action_items": [
        "item1",
        "item2"
    ]
}}
"""
    )

    prompt = prompt_template.format(
        content=email.get("body", "")
    )

    model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0.3
    )

    response = model.invoke(prompt)

    result_text = (
        response.content
        if hasattr(response, "content")
        else str(response)
    )

    result_text = clean_text(result_text)

    try:
        return json.loads(result_text)

    except Exception:
        return {
            "summary": result_text,
            "sentiment": "Neutral",
            "action_items": []
        }
