from core.email_imap import fetch_imap_emails
from core.email_sender import send_email, send_draft_to_gmail
from core.supervisor import supervisor_langgraph
from core.state import EmailState

from config import (
    IMAP_USERNAME,
    IMAP_PASSWORD,
    IMAP_SERVER
)

from utils.logger import get_logger

logger = get_logger(__name__)


def process_email_action(email, your_name):

    action = input(
        "\nSend email or save draft? (s/d): "
    ).strip().lower()

    if action == "s":

        if send_email(email, your_name):
            print("\nEmail sent successfully.")
        else:
            print("\nFailed to send email.")

    elif action == "d":

        gmail_address = input(
            "Enter Gmail address for draft: "
        )

        if send_draft_to_gmail(
            email,
            your_name,
            gmail_address
        ):
            print("\nDraft sent successfully.")
        else:
            print("\nFailed to create draft.")


def choose_tone():

    print("\nReply Style")
    print("1. Professional")
    print("2. Friendly")
    print("3. Brief")

    choice = input("\nChoose style: ")

    styles = {
        "1": "Professional",
        "2": "Friendly",
        "3": "Brief"
    }

    return styles.get(choice, "Professional")


def main():

    logger.info("\n\nStarting InboxFlow\n")

    your_name = input(
        "Your name: "
    )

    recipient_name = input(
        "Recipient name: "
    )

    tone = choose_tone()

    emails = fetch_imap_emails(
        IMAP_USERNAME,
        IMAP_PASSWORD,
        IMAP_SERVER
    )

    if not emails:

        print("\nNo emails found.")
        return

    latest_emails = emails[-5:]

    print("\nRecent Emails")

    for index, email in enumerate(
        latest_emails,
        start=1
    ):
        print(
            f"{index}. {email['subject']}"
        )

    choice = int(
        input(
            "\nChoose email number: "
        )
    ) - 1

    if (
        choice < 0
        or choice >= len(latest_emails)
    ):
        print("Invalid selection.")
        return

    selected_email = latest_emails[choice]

    state = EmailState()

    state.emails = [selected_email]
    state.current_email = selected_email

    state = supervisor_langgraph(
        selected_email,
        state,
        your_name,
        recipient_name,
        tone
    )

    print("\n" + "=" * 50)
    print("EMAIL INSIGHTS")
    print("=" * 50)

    print(
        f"Category: "
        f"{selected_email.get('classification')}"
    )

    print(
        f"Priority: "
        f"{selected_email.get('priority')}/10"
    )

    print(
        f"Sentiment: "
        f"{selected_email.get('sentiment')}"
    )

    print(
        f"\nSummary:\n"
        f"{selected_email.get('summary')}"
    )

    print("\nAction Items:")

    for item in selected_email.get(
        "action_items",
        []
    ):
        print(f"- {item}")

    print("\n" + "=" * 50)
    print("GENERATED RESPONSE")
    print("=" * 50)

    print(
        selected_email.get(
            "response",
            "No response generated."
        )
    )

    process_email_action(
        selected_email,
        your_name
    )

    logger.info(
        "Email processing completed."
    )


if __name__ == "__main__":
    main()