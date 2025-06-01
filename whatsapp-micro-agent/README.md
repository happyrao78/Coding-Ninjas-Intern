# WhatsApp Automation Agent

A micro agent built using Python, FastAPI, Selenium, and Google Sheets integration to automate WhatsApp messaging for outreach and engagement workflows.

This agent is designed and deployed as part of Sankalpiq’s automation suite, allowing consistent and personalized communication with organizations listed in a Google Sheet. It eliminates repetitive manual effort by sending tailored WhatsApp messages at scheduled intervals, while tracking delivery status in real-time.

---

## Purpose

NGOs and similar organizations often face challenges in scaling outreach while maintaining personalization. This agent solves that problem by:

* Automating personalized WhatsApp messages to contacts stored in a structured Google Sheet.
* Reducing manual effort and improving operational efficiency.
* Enabling consistent and scalable communication without third-party platforms.

---

## Key Features

* CLI-based execution with FastAPI backend for optional HTTP-based control
* Uses Selenium for WhatsApp Web automation and persistent sessions
* Reads contact and status data from Google Sheets
* Message templates with dynamic placeholders like `{ngo_name}`
* Tracks and writes delivery status back to the sheet
* Supports both manual and scheduled bulk message sending
* Custom message override supported per contact

---

## Technologies Used

* **Python>=3.8.x** – Core development language
* **FastAPI** – Lightweight and async-compatible API framework
* **Selenium** – Automates WhatsApp Web for browser-based messaging
* **gspread** – Google Sheets API wrapper for reading/writing data
* **oauth2client** – Handles Google service authentication
* **asyncio** – For scheduling periodic task execution

---

## Getting Started

### 1. Install the dependencies

```bash
pip install -r requirements.txt
```

### 2. Create a `.env` file

Use the following sample format and update values as needed:

```env
GOOGLE_SHEETS_CREDENTIALS_FILE=credentials/config.json
GOOGLE_SHEET_ID=your_sheet_id
WORKSHEET_NAME=Sheet1

MESSAGE_TEMPLATE=Your message template with {ngo_name}
CUSTOM_MESSAGE=Optional default fallback message with {ngo_name}

PROCESSING_INTERVAL=300
CHROME_USER_DATA_DIR=data/chrome_user_data
```

### 3. Run the service

```bash
uvicorn app.main:app --reload
```

The API will start at `http://localhost:8000`

---

## API Overview

| Method | Endpoint   | Description                        |
| ------ | ---------- | ---------------------------------- |
| GET    | `/status`  | Check if the agent is running      |
| POST   | `/send`    | Send a message to a single contact |
| POST   | `/process` | Trigger bulk message processing    |

---

## Sheet Format Requirements

The connected Google Sheet must contain the following columns:

* `Client Name` – The name of the organization
* `Phone` – The WhatsApp-compatible phone number
* `Status` – The status field will be updated automatically (`Pending`, `Sent`, `Failed`, etc.)

---

## Future Scope

The current implementation offers a focused CLI-first solution. Future enhancements are planned to improve scalability, observability, and intelligent processing:

### Langflow or Agent Orchestration

Integrate Langflow or similar agent design frameworks to allow visually designed workflows for conditional messaging and escalation logic.

### Modular Agent Extension

Enable plug-and-play functionality for adding new contact sources (e.g., Airtable, Notion) or messaging platforms (e.g., Telegram, Email).

### Deployment on MCP/Cloud Servers

Package the agent into a containerized service and deploy on a cloud infrastructure (e.g., MCP servers) to enable multi-tenant use and monitoring.

