# Sankalpiq Foundation - AI Automation Suite

## Problem Statement

In India there are 3.3 million(approx) registered Non-governmental organizations (NGOs) and many of them face significant operational challenges that hinder their ability to maximize impact with limited resources. These challenges include:

- **Repetitive Communication Tasks**: Manual handling of donor and volunteer inquiries consuming substantial human resources
- **Knowledge Fragmentation**: Critical organizational information scattered across multiple sources without centralized access
- **Scaling Limitations**: Inability to handle increasing volumes of stakeholder interactions without proportional resource increase
- **Manual Process Dependencies**: Heavy reliance on human intervention for routine communication, data collection, and outreach activities, planning campaigns
- **Limited Outreach Capabilities**: Difficulty in maintaining consistent and personalized communication across multiple channels
- **Data Collection Inefficiencies**: Time-intensive manual processes for gathering beneficiary information and feedback

## Solution Overview

The Sankalpiq Foundation AI Automation Suite is a comprehensive microservices-based Multiagent designed to automate critical NGO operations through intelligent micro agents. The solution addresses operational bottlenecks by implementing specialized micro-agents that handle specific organizational functions while maintaining seamless integration capabilities and working independently.

### Core Components

1. **CLI-Based Micro Agent**: Intelligent assistant for email automation and knowledge management
2. **Voice Micro-Agent**: Automated voice interaction system for data collection and FAQ handling
3. **WhatsApp Automation Agent**: Automated messaging system for scalable outreach campaigns, leads generation
4. **Streamlit Dashboard**: Web-based user interface for agent overview and solution architecture visualization

## Architecture Overview

### Streamlit UI
![Streamlit UI](https://happyrao78-coding-ninjas-intern-clientclient-iypjzf.streamlit.app)

### High-Level Design (HLD)
![High-Level Design](https://www.mermaidchart.com/raw/a8191288-3abc-4075-a659-d0cf9e7ab95c?theme=light&version=v0.1&format=svg)

### Low-Level Design (LLD)
![Low-Level Design](https://www.mermaidchart.com/raw/72b460cc-72d5-4e1d-98cb-5349690efbfa?theme=light&version=v0.1&format=svg)

## Performance Metrics

- **Response Accuracy**: Percentage of queries answered correctly by the knowledge base
- **Query Latency**: Average response time per query
- **Email Delivery Rate**: Percentage of successfully delivered emails
- **Knowledge Base Coverage**: Percentage of responses using stored organizational knowledge

## Technology Stack

### Large Language Models (LLMs)

#### Primary LLM Selection
**Google Gemini 1.5 Flash** serves as the primary language model for this implementation, chosen for the following reasons:

- **Cost Efficiency**: Optimal balance between performance and operational costs for NGO budgets
- **Response Speed**: Fast inference times suitable for real-time interactions
- **Multilingual Support**: Enhanced capability for regional language processing
- **Integration Ease**: Seamless API integration with existing Google Cloud services
- **Context Understanding**: Superior performance in understanding organizational context and domain-specific queries

#### Free-Tier Alternative
**Hugging Face Transformers (all-MiniLM-L6-v2)** is utilized for embedding generation and semantic search capabilities:

- **Open Source**: No licensing costs, suitable for resource-constrained environments
- **Offline Capability**: Can operate without continuous internet connectivity
- **Customization**: Ability to fine-tune on organization-specific data
- **Privacy**: Local processing ensures sensitive organizational data remains secure

### Core Technologies

| Layer | Technology | Purpose |
|-------|------------|---------|
| **LLM Framework** | Google Gemini 1.5 Flash | Natural language understanding and generation |
| **Vector Database** | Pinecone | Scalable semantic search and knowledge retrieval |
| **Backend Framework** | FastAPI | High-performance API orchestration |
| **Frontend Interface** | Streamlit | Interactive web dashboard for agent management |
| **Workflow Management** | LangChain | LLM pipeline orchestration and tool integration |
| **Voice Processing** | Twilio Voice (Polly) | Automated telephonic interactions |
| **Web Automation** | Selenium WebDriver | Browser-based WhatsApp automation |
| **Email Service** | SMTP Protocol | Automated email delivery |
| **Data Storage** | Google Sheets API | Cloud-based data management |
| **Containerization** | Docker | Environment consistency and deployment |
| **Development Tunnel** | Ngrok | Local development and webhook testing |
| **Code Quality** | Husky | Flake8 and Black for auto indentation, clean code for better debugging and optimization  |

### Programming Languages and Libraries

- **Python 3.8+**: Primary development language
- **FastAPI**: Asynchronous web framework
- **Streamlit**: Interactive web application framework for dashboard creation
- **LangChain**: LLM application development framework
- **gspread**: Google Sheets API integration
- **Selenium**: Web browser automation
- **asyncio**: Asynchronous programming support
- **python-dotenv**: Environment configuration management
- **Oauth2client**: Handles Google service authentication via Cloud

## Agent Specifications

Each agent operates with its own independent architecture and deployment configuration. For detailed setup instructions, refer to the individual README files in each micro agent's directory.

### CLI-Based Micro Agent (`/cli-assistant`)
- **Function**: Email automation and knowledge base management with semantic search using vector DB and LLM Embeddings
- **Interface**: Command-line interface for resource-constrained environments
- **Setup**: See `/cli-assistant/README.md` for detailed overview,installation and configuration

### Voice Micro-Agent (`/voice-micro-agent`)
- **Function**: Automated voice interactions and data collection via Call
- **Sub-Agents**: 1. FAQ Agent for query resolution, 2. Info Agent for structured data collection
- **Setup**: See `/voice-micro-agent/README.md` for overview, configuration and deployment

### WhatsApp Automation Agent (`/whatsapp-micro-agent`)
- **Function**: Scalable messaging and outreach automation
- **Capabilities**: Bulk message sending, delivery tracking, template-based personalization
- **Setup**: See `/whatsapp-micro-agent/README.md` for Google Sheets integration, setup, and Overview

### Streamlit Dashboard (`/client`)
- **Function**: Web-based interface for agent information and solution architecture visualization
- **Features**: Overall solution overview, architecture diagrams, and agent infrastrucutre
- **Setup**: See `/client/README.md` for dashboard configuration and deployment

## Video Demonstrations

### Agent Functionality Demos
- **CLI Micro Agent Demo**: [Link to be provided]
- **Voice Agent Interaction Demo**: [Link to be provided]
- **WhatsApp Automation Demo**: [Link to be provided]
- **End-to-End Workflow Demo**: [Link to be provided]

## Setup and Deployment

### Prerequisites
- Python 3.8 or higher
- Docker and Docker Compose
- Google Cloud Platform account with API access
- Twilio account with verified phone number
- Gmail account with App Password enabled


### Root Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Future Scope and Scalability

### Planned Enhancements

#### Infrastructure Scaling
- **Apache Kafka Integration**: Implementation of event-driven architecture for real-time data streaming and service decoupling
- **Model Context Protocol (MCP) Servers**: Deployment on high-performance infrastructure for concurrent task processing
- **Cloud-Native Architecture**: Migration to containerized deployments on AWS ECS, Google Cloud Run, or Azure Container Instances

#### Advanced AI Capabilities
- **Langflow Integration**: Visual workflow orchestration for complex agent behavior design
- **Enhanced Language Support**: Regional Indian language processing including Bengali, Tamil, and Marathi
- **Advanced Analytics**: Real-time dashboard for performance monitoring and operational insights

#### Platform Extensions
- **Multi-Channel Integration**: Support for Telegram, and other messaging platforms
- **Advanced Speech Recognition**: Implementation of specialized STT systems or sarvam-ai for improved regional language accuracy
- **Intelligent Routing and Connection**: AI-powered query classification and routing to appropriate specialized agents

### Monitoring and Observability
- **Real-Time Alerts**: Automated failure detection and notification systems
- **Performance Analytics**: Comprehensive tracking of agent performance and user engagement metrics
- **Audit Logging**: Complete interaction logging for compliance and performance optimization

## Code Quality and Industry Based Development Standards

This project maintains high code quality through automated tooling and standardized practices:

- **Husky**: Pre-commit hooks for code quality enforcement
- **Linting**: Automated code style checking and formatting
- **Version Control**: Git-based workflow with branch protection
- **Modular Architecture**: Each agent maintains independent codebase and deployment configuration
- **Documentation Standards**: Comprehensive README files for each component
- **Detailed Technical Documentation**: Detailed technical documentation as per Industry Standards.
- **System Design**: High Level Architecture and Low Level Architecture made using Mermaid.

---
