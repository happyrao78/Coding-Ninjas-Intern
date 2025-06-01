# Voice Micro-Agent

The Voice Micro-Agent is a dedicated, containerized voice automation service developed for the Sankalpiq platform. It enables NGOs to automate interactions through voice calls, supporting both data collection and intelligent query resolution. This microservice operates independently and is designed to integrate seamlessly with broader outreach and communication efforts.

## Overview

Non-governmental organizations (NGOs) frequently face challenges such as limited manpower for communication, repetitive queries from beneficiaries, and a lack of scalable systems for data collection. The Voice Micro-Agent addresses these issues by automating voice calls, answering user queries via AI, and collecting structured data over telephonic interactions.

It includes two distinct operational sub-agents:

- **FAQ Agent**: Provides AI-driven answers to user queries.
- **Info Agent**: Collects structured data including name, email, and blood group.

This service is built with modular architecture, ensuring future extensibility and isolated deployment per use case.

## Sub-Agents

### FAQ Agent

This agent handles user questions by utilizing a predefined knowledge base in combination with a language model to deliver natural responses.

**Endpoints and Purpose:**

- `POST /voice-faq`: Initiates the FAQ workflow and prompts the user for their name.
- `POST /handle-name`: Processes the user’s name and advances to the next step.
- `POST /voice-ngo`: Introduces the NGO and prompts the user for their query.
- `POST /handle-faq`: Processes the query using Gemini AI and delivers a response.
- `POST /handle-more-faq`: Determines if the user has additional queries.
- `POST /thank-you`: Closes the interaction with a gratitude message.

### Info Agent

This agent is responsible for gathering structured personal data from users over a voice interaction.

**Endpoints and Purpose:**

- `POST /voice-info`: Begins the information collection flow by requesting the user’s name.
- `POST /handle-info-name`: Captures the name and moves to email collection.
- `POST /voice-email`: Requests the user’s email address.
- `POST /handle-email`: Validates and stores the email, then prompts for blood group.
- `POST /voice-blood`: Requests the user's blood group.
- `POST /handle-blood`: Stores the information in both CSV format and Google Sheets.

## Industry-Standard Stack

The Voice Micro-Agent is implemented using the following tools and technologies to ensure scalability, maintainability, and ease of deployment:

- **FastAPI**: High-performance asynchronous Python framework for API orchestration.
- **Twilio Voice API**: Manages automated voice call interactions and webhook integration.
- **Gemini AI API**: Provides dynamic, intelligent responses to user queries within the FAQ Agent.
- **CSV File Storage**: Local persistence of collected user data.
- **Google Sheets API**: Cloud-based storage for collected information accessible by NGOs.
- **Gmail SMTP**: Used for sending follow-up or confirmation emails to participants.
- **Docker**: Containerization for environment consistency across deployments.
- **Ngrok**: Local tunnel exposure for webhook testing in development environments.
- **Dotenv (`python-dotenv`)**: Secure handling of environment configurations.
- **Urllib / Requests**: HTTP handling for external service integration.

## Setup Instructions

### Prerequisites

- Docker and Docker Compose installed on your machine.
- Python 3.8 or higher (for development/debugging).
- A registered Twilio account with a verified phone number.
- Gmail account with App Password enabled (for email functionality).
- Google Sheets API credentials with access permissions.
- Gemini API Key.

### Environment Configuration

Create a `.env` file in the root directory with the following variables:

```

TWILIO\_ACCOUNT\_SID=your\_twilio\_account\_sid
TWILIO\_AUTH\_TOKEN=your\_twilio\_auth\_token
TWILIO\_PHONE\_NUMBER=your\_twilio\_phone\_number
TO\_NUMBER=recipient\_number

GEMINI\_API\_KEY=your\_gemini\_api\_key
GMAIL\_ADDRESS=your\_email
GMAIL\_APP\_PASSWORD=your\_gmail\_app\_password

WEBHOOK\_URL=[https://your-ngrok-url](https://your-ngrok-url)
PORT=8000
NGROK\_AUTHTOKEN=your\_ngrok\_auth\_token

```

### Docker-Based Execution

1. Build and start the services:

```

docker-compose up --build

```

2. Once the containers are running, retrieve the public Ngrok URL using:

```

curl [http://localhost:4040/api/tunnels](http://localhost:4040/api/tunnels)

```

3. Set the retrieved Ngrok URL as `WEBHOOK_URL` in your `.env` file for local testing with Twilio.

## Testing and Validation

For testing the APIs:

- **Tool**: [Thunder Client](https://www.thunderclient.com/) (VS Code Extension).
- Base URL during local development: `http://localhost:8000`.
- Use `application/x-www-form-urlencoded` content type to simulate Twilio webhook inputs.
- Ensure Twilio's webhook for incoming voice calls is set to your Ngrok public URL followed by the appropriate endpoint (e.g., `/voice-faq` or `/voice-info`).

## Future Scope

- **Langflow Integration**: To enable visual orchestration of workflows.
- **Expanded Language Support**: Support for regional Indian languages such as Bengali, Tamil, and Marathi.
- **Analytics and Reporting**: Integration of a dashboard to track call statistics, engagement rates, and data submissions.
- **Cloud-Native Deployment**: Deployment via AWS ECS, Google Cloud Run, or other platforms to support high-availability services.
- **Real-Time Monitoring**: Alerts and monitoring for failed interactions or incorrect submissions.
- **Enhanced Speech Recognition**: Use of advanced STT (speech-to-text) systems for improved Hindi accuracy.

---
