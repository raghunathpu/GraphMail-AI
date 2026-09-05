# GraphMail AI

A multi-agent email assistant built with Python, LangGraph, Google Gemini, Gmail IMAP, and SMTP.

GraphMail AI automatically reads emails, classifies them, generates summaries, drafts context-aware replies, and allows human approval before sending responses.

---

## Features

### Smart Email Reading

* Connects directly to Gmail using IMAP
* Fetches recent emails automatically
* Supports real inbox processing

### AI Email Classification

Categorizes emails into:

* Personal
* Business
* Spam
* Important
* Informational

### AI Email Summarization

* Generates concise summaries
* Extracts key information
* Identifies sentiment and intent

### AI Reply Generation

* Creates context-aware responses
* Supports multiple reply styles:

  * Professional
  * Friendly
  * Brief

### Human-in-the-Loop Review

* Review generated responses before sending
* Edit responses manually
* Approve or reject drafts

### Automated Email Sending

* Sends approved emails through Gmail SMTP
* Secure authentication using Gmail App Passwords

### LangGraph Multi-Agent Workflow

The system uses a supervisor-based workflow:

Email → Filtering Agent → Summarization Agent → Response Agent → Human Review → Send Email

---

## Tech Stack

### AI & Agents

* Google Gemini 2.5 Flash
* LangChain
* LangGraph

### Email Services

* Gmail IMAP
* Gmail SMTP

### Backend

* Python 3.10+
* dotenv
* logging

---

## Project Architecture

```text
GraphMail AI

├── Filtering Agent
│   └── Classifies email category

├── Summarization Agent
│   └── Creates concise summaries

├── Response Agent
│   └── Generates contextual replies

├── Human Review Agent
│   └── Allows approval/editing

└── Supervisor
    └── Controls workflow using LangGraph
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/manikoushik001/GraphMail-AI.git
cd GraphMail-AI
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate environment:

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file:

```env
# Gemini API
GEMINI_API_KEY=your_gemini_api_key

# Gmail SMTP
EMAIL_SERVER=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_gmail_app_password

# Gmail IMAP
IMAP_SERVER=imap.gmail.com
IMAP_PORT=993
IMAP_USERNAME=your_email@gmail.com
IMAP_PASSWORD=your_gmail_app_password
```

---

## Running the Application

```bash
python main.py
```

The application will:

1. Connect to Gmail
2. Fetch recent emails
3. Classify the selected email
4. Generate a summary
5. Create a response draft
6. Allow human approval
7. Send the email through SMTP

---

## Example Workflow

```text
Recent Emails

1. Meeting Request
2. Project Update
3. Personal Message

Choose email number: 2

Category: Business
Priority: High

Summary:
Project status update with action items.

Generated Reply:
...

Approve? (y/n)
```

---

## Folder Structure

```text
GraphMail-AI
│
├── agents/
│   ├── filtering_agent.py
│   ├── summarization_agent.py
│   ├── response_agent.py
│   └── human_review_agent.py
│
├── core/
│   ├── email_imap.py
│   ├── email_sender.py
│   ├── supervisor.py
│   └── state.py
│
├── utils/
│   ├── logger.py
│   └── formatter.py
│
├── drafts/
│
├── main.py
├── config.py
├── requirements.txt
└── README.md
```

---

## Future Improvements

* Gmail OAuth Authentication
* Multi-account inbox management
* Priority-based email sorting
* Automatic follow-up suggestions
---

