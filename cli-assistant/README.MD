# Sankalpiq Foundation Micro Agent

## Overview

The **Sankalpiq Foundation Micro Agent** is a **CLI-based intelligent assistant** built to empower NGOs by automating communication, managing knowledge, and optimizing operational workflows. Developed using state-of-the-art AI and backend technologies, this micro agent reduces manual workload, improves stakeholder engagement, and offers a scalable architecture for future growth.

---

## What Problems Does It Solve?

NGOs face several operational challenges due to limited resources and increasing complexity. This micro agent helps solve:

| Problem Area                 | Solution Provided                                                                        |
| ---------------------------- | ---------------------------------------------------------------------------------------- |
| **Repetitive Communication** | Automates replies to donor and volunteer emails using a knowledge-driven NLP system      |
| **Knowledge Fragmentation**  | Centralizes important info into a semantic vector-based knowledge base                   |
| **Scaling Limitations**      | Designed with scalable architecture using modern tools like Pinecone           |
| **Human Bottlenecks**        | Reduces dependency on manual processes for communication, tracking, and decision support |

---

## Automated Tasks Handled by the Agent

* Responding to common donor and volunteer queries
* Sending templated, personalized emails using SMTP
* Interacting with a pre-loaded knowledge base for contextual answers
* Logging and managing responses for performance evaluation
* CLI-based command management for low-resource environments

---

## Interface

* **Type**: Command Line Interface (CLI)
* **User Interaction**:

  * `help`: View all available commands
  * `send mail`: Trigger an email via SMTP
  * `config`: Update API keys or system parameters
  * `exit`: Stop the assistant

---

## Tech Stack

| Layer          | Technology                     | Purpose                                       |
| -------------- | ------------------------------ | --------------------------------------------- |
| **LLM**        | Gemini (1.5 Flash)             | Natural language understanding and generation |
| **Embeddings** | HuggingFace `all-MiniLM-L6-v2` | Create semantic vector representations        |
| **Vector DB**  | Pinecone                       | Fast and scalable semantic search             |
| **Backend**    | FastAPI + LangChain            | API orchestration and LLM workflows           |
| **Email**      | SMTP                           | Automated email delivery                      |
| **Interface**  | CLI                            | Lightweight terminal-based control            |
| **Server**     | Uvicorn                        | ASGI server for real-time interaction         |
| **Tunnel**     | Ngrok                          | Public access during local development        |

---

## Key Performance Metrics

* **Response Accuracy**: % of queries answered correctly
* **Query Latency**: Average response time per query
* **Email Delivery Rate**: % of successfully delivered emails
* **Knowledge Base Coverage**: % of responses using stored knowledge

---

## 🛠️ Local Development Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure `.env` File

Create a `.env` file with the following:

```
PINECONE_API_KEY=your_key
PINECONE_ENVIRONMENT=your_env
GEMINI_API_KEY=your_key
EMAIL_ADDRESS=your_email
EMAIL_PASSWORD=your_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

### 4. Prepare the Knowledge Base

Create or update `data/knowledge.txt` with organizational FAQs, processes, and campaign information.

### 5. Start the Application

```bash
python -m ngo-assisstant.main --knowledge-file data/knowledge.txt
```
Use --knowledge-file data/knowledge.txt only for the initial start to configure your knowledge as LLM Embeddings in Pinecone.

---

## Future Scope and Scalability

To ensure the agent can scale and serve growing NGO networks, the following technologies will be integrated:

### **1. Apache Kafka**

* **Why**: Kafka enables real-time data streaming and decoupled communication between microservices.
* **Use Cases**:

  * Queue incoming donor/volunteer queries for parallel processing
  * Stream event logs for audit and analytics
  * Integrate webhook listeners for social platforms and form submissions

### **2. MCP (Multi-Core Processing) Servers**

* **Why**: Leverage high-performance hardware for concurrency and parallel task handling.
* **Use Cases**:

  * Run multiple knowledge retrieval tasks simultaneously
  * Enable load balancing across different NLP services
  * Improve email batch processing speed

### **3. Langflow (for LLM Workflow Orchestration)**

* **Why**: Provides a visual, modular way to design and debug LLM pipelines.
* **Use Cases**:

  * Build advanced agent behavior with conditionals and tools
  * Visualize logic paths for transparency and audit
  * Quickly integrate new modules (e.g., speech-to-text, form validation)

---

## Example Use Case

**Volunteer Inquiry**:

* **User Input**: “How can I join the education outreach program?”
* **Response**: The agent semantically searches the knowledge base and replies:

  > "To join our education outreach program, please complete the volunteer form at [www.sankalpiq.co.in](http://www.sankalpiq.co.in). Our team will reach out shortly."

**Donor Email Automation**:

* Automatically responds to donation queries with:

  > "Thank you for your interest in supporting us. You can donate through [www.sankalpiq.co.in](http://www.sankalpiq.co.in). All contributions are tax-exempt under Section 80G."

---

## Why This Matters

NGOs need to maximize impact with minimal resources. The Bhartiya Foundation Micro Agent does just that by:

* Automating the most repetitive but essential tasks
* Providing instant, intelligent support to donors and volunteers
* Offering a scalable architecture ready for high-growth adoption

