from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from config import GEMINI_API_KEY
from utils.logger import get_logger
from utils.formatter import clean_text

logger = get_logger(__name__)


def filter_email(email: dict) -> str:

    prompt_template = PromptTemplate(
        input_variables=["subject", "content"],
        template="""
You are an email classification assistant.

Subject:
{subject}

Content:
{content}

Classify this email into ONE category only:

- spam
- meeting
- support
- sales
- marketing
- personal

Return ONLY the category name.
"""
    )

    prompt = prompt_template.format(
        subject=email.get("subject", ""),
        content=email.get("body", "")
    )

    model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0.2
    )

    result = model.invoke(prompt)

    classification = clean_text(str(result)).lower()

    logger.debug("Classification Result: %s", classification)

    if "spam" in classification:
        return "spam"

    if "meeting" in classification:
        return "meeting"

    if "support" in classification:
        return "support"

    if "sales" in classification:
        return "sales"

    if "marketing" in classification:
        return "marketing"

    return "personal"
