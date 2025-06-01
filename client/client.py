import streamlit as st
import pandas as pd
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="Sankalpiq Foundation - Multi-Agent AI Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced CSS with animations and modern design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 4rem 2rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 3rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 100%;
        height: 100%;
        background: rgba(255,255,255,0.1);
        transform: rotate(45deg);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%) rotate(45deg); }
        100% { transform: translateX(100%) rotate(45deg); }
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 1rem;
        background: linear-gradient(45deg, #fff, #f0f0f0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: fadeInUp 1s ease-out;
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        opacity: 0.9;
        font-weight: 300;
        animation: fadeInUp 1s ease-out 0.2s both;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    }
    
    .metric-number {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        color: #718096;
        font-size: 0.9rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .agent-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
        gap: 2rem;
        margin: 2rem 0;
    }
    
    .agent-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
        border: 1px solid #e2e8f0;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        border-top: 4px solid;
        border-image: linear-gradient(135deg, #4299e1, #3182ce) 1;
    }
    
    .agent-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
    }
    
    .tech-stack {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin: 1rem 0;
    }
    
    .tech-badge {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .tech-badge:hover {
        transform: scale(1.1);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    .highlight-box {
        background: linear-gradient(135deg, #e6fffa 0%, #f0fff4 100%);
        border-left: 4px solid #38b2ac;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1.5rem 0;
    }
    
    .warning-box {
        background: linear-gradient(135deg, #fef5e7 0%, #fff8dc 100%);
        border-left: 4px solid #ed8936;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1.5rem 0;
    }
    
    .future-box {
        background: linear-gradient(135deg, #ebf8ff 0%, #f0f9ff 100%);
        border-left: 4px solid #4299e1;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1.5rem 0;
    }
    
    .footer-section {
        text-align: center;
        padding: 3rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        margin-top: 3rem;
        color: white;
    }
    
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2rem;
        }
        
        .hero-subtitle {
            font-size: 1.1rem;
        }
        
        .agent-grid {
            grid-template-columns: 1fr;
        }
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-section">
    <h1 class="hero-title">🤖 Sankalpiq Foundation Multi-Agent AI Platform</h1>
    <p class="hero-subtitle">Enterprise-Grade Intelligent Automation for NGO Operations</p>
</div>
""", unsafe_allow_html=True)

# Assignment Overview Metrics
st.markdown("""
<div class="metric-grid">
    <div class="metric-card">
        <div class="metric-number">4</div>
        <div class="metric-label">Specialized Agents</div>
    </div>
    <div class="metric-card">
        <div class="metric-number">12+</div>
        <div class="metric-label">Technologies Used</div>
    </div>
    <div class="metric-card">
        <div class="metric-number">3</div>
        <div class="metric-label">Communication Channels</div>
    </div>
    <div class="metric-card">
        <div class="metric-number">100%</div>
        <div class="metric-label">Process Automation</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Problem Statement Section
st.header("🎯 Problem Statement")

st.markdown("""
<div class="highlight-box">
<h4>Primary Challenge</h4>
<p>NGOs face significant operational inefficiencies in managing multi-channel communications, volunteer coordination, 
and stakeholder engagement. Manual processes lead to delayed responses, inconsistent information delivery, 
and resource wastage.</p>
</div>
""", unsafe_allow_html=True)

st.subheader("Why Multi-Agent AI is the Solution:")
st.write("""
- **Specialized Task Distribution:** Each agent handles specific communication channels and processes
- **Scalability:** Agents can process thousands of interactions simultaneously
- **24/7 Availability:** Continuous operation without human intervention
- **Intelligent Collaboration:** Agents share context and knowledge base for consistent responses
- **Cost Efficiency:** Reduces need for large customer service teams
""")

st.markdown("""
<div class="warning-box">
<strong>Unique Value of Multi-Agent Approach:</strong> Unlike single-agent systems, our multi-agent architecture 
allows for specialized expertise in each communication channel while maintaining unified organizational knowledge 
and seamless handoffs between agents.
</div>
""", unsafe_allow_html=True)

# Project Description Section
st.header("🚀 Project Description")

st.write("""
The Sankalpiq Foundation Multi-Agent Platform is a comprehensive ecosystem of four specialized micro-agents 
that automate and optimize NGO operations through intelligent process orchestration.
""")

st.subheader("Agent Interaction & Collaboration:")
st.write("""
- **Shared Knowledge Base:** All agents access centralized Pinecone vector database
- **Context Passing:** Information collected by one agent is available to others
- **Unified Communication:** Consistent messaging across all channels
- **Intelligent Routing:** Complex queries are routed to appropriate specialized agents
- **Real-time Synchronization:** Data updates are immediately available across all agents
""")

# Agent Architecture
st.header("🏗️ Multi-Agent Architecture")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="agent-card">
        <h3>🖥️ CLI Assistant Agent</h3>
        <p><strong>Purpose:</strong> Command-line orchestration and knowledge management</p>
        <p><strong>Key Functions:</strong></p>
        <ul>
            <li>Semantic search through organizational knowledge</li>
            <li>Email automation workflows</li>
            <li>System health monitoring</li>
            <li>Inter-agent communication hub</li>
        </ul>
        <div class="tech-stack">
            <span class="tech-badge">Gemini 1.5</span>
            <span class="tech-badge">Pinecone</span>
            <span class="tech-badge">FastAPI</span>
            <span class="tech-badge">LangChain</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="agent-card">
        <h3>💬 WhatsApp Automation Agent</h3>
        <p><strong>Purpose:</strong> Mass messaging and campaign management</p>
        <p><strong>Key Functions:</strong></p>
        <ul>
            <li>Bulk WhatsApp message campaigns</li>
            <li>Personalized message templating</li>
            <li>Delivery status tracking</li>
            <li>Campaign analytics and reporting</li>
        </ul>
        <div class="tech-stack">
            <span class="tech-badge">Selenium</span>
            <span class="tech-badge">Google Sheets</span>
            <span class="tech-badge">FastAPI</span>
            <span class="tech-badge">Asyncio</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="agent-card">
        <h3>📞 Voice Interaction Agent</h3>
        <p><strong>Purpose:</strong> Telephonic communication automation</p>
        <p><strong>Key Functions:</strong></p>
        <ul>
            <li>Automated data collection via phone calls</li>
            <li>FAQ resolution through voice interface</li>
            <li>Real-time information processing</li>
            <li>Multilingual support capability</li>
        </ul>
        <div class="tech-stack">
            <span class="tech-badge">Twilio API</span>
            <span class="tech-badge">Gemini AI</span>
            <span class="tech-badge">Google Sheets</span>
            <span class="tech-badge">Docker</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="agent-card">
        <h3>🔗 Integration Layer</h3>
        <p><strong>Purpose:</strong> Agent coordination and data synchronization</p>
        <p><strong>Key Functions:</strong></p>
        <ul>
            <li>Unified API gateway</li>
            <li>Authentication and security</li>
            <li>Data consistency management</li>
            <li>Performance monitoring</li>
        </ul>
        <div class="tech-stack">
            <span class="tech-badge">OAuth2</span>
            <span class="tech-badge">Ngrok</span>
            <span class="tech-badge">Redis</span>
            <span class="tech-badge">Uvicorn</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Tools and Frameworks Section
st.header("🛠️ Tools, Libraries & Frameworks")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.subheader("🤖 AI & ML Frameworks")
    st.write("""
    - **LangChain:** Agent orchestration and prompt management
    - **HuggingFace Transformers:** Model integration and processing
    - **Pinecone:** Vector database for semantic search
    - **Google Gemini:** Primary LLM for intelligent responses
    """)

with col2:
    st.subheader("🌐 Communication Protocols")
    st.write("""
    - **Twilio API:** Voice call automation
    - **SMTP Protocol:** Email automation
    - **WhatsApp Web API:** Messaging automation
    - **Google Sheets API:** Data management
    """)

with col3:
    st.subheader("⚙️ Backend & Infrastructure")
    st.write("""
    - **FastAPI:** High-performance web framework
    - **Docker:** Containerization and deployment
    - **Uvicorn:** ASGI web server
    - **Ngrok:** Secure tunneling service
    """)

with col4:
    st.subheader("🔄 Agent Orchestration")
    st.write("""
    - **Asyncio:** Asynchronous processing
    - **Python-dotenv:** Configuration management
    - **OAuth2:** Authentication framework
    - **Selenium:** Web automation
    """)

# LLM Selection Section
st.header("🧠 LLM Selection & Justification")

# Create comparison table data
comparison_data = {
    "Model Type": ["Primary LLM", "Secondary LLM", "Free Tier", "Open Source"],
    "Model": ["Google Gemini 1.5 Pro", "OpenAI GPT-4o", "Gemini 1.5 Flash", "Llama 3.1 70B"],
    "Use Case": [
        "Complex reasoning, multi-modal processing",
        "Critical decision making, complex analysis",
        "High-volume, quick responses",
        "On-premises deployment, data privacy"
    ],
    "Justification": [
        "Superior context window (1M tokens), excellent reasoning, cost-effective",
        "Best-in-class reasoning for complex scenarios",
        "Fast processing, sufficient for routine tasks",
        "No API costs, complete data control"
    ],
    "Cost": ["Moderate", "High", "Free/Low", "Infrastructure"]
}

df_comparison = pd.DataFrame(comparison_data)
st.dataframe(df_comparison, use_container_width=True)

st.markdown("""
<div class="highlight-box">
<h4>Selection Rationale:</h4>
<p><strong>Gemini 1.5 Pro</strong> was chosen as the primary LLM because:</p>
<ul>
    <li><strong>Long Context Window:</strong> Essential for processing large knowledge bases</li>
    <li><strong>Multi-modal Capabilities:</strong> Can process text, voice, and potentially images</li>
    <li><strong>Cost Efficiency:</strong> Better price-to-performance ratio than GPT-4</li>
    <li><strong>Google Integration:</strong> Seamless integration with Google Workspace APIs</li>
    <li><strong>Reasoning Quality:</strong> Excellent performance on complex NGO scenarios</li>
</ul>
</div>
""", unsafe_allow_html=True)

# Future Scope Section
st.header("🔮 Future Scope & Roadmap")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="future-box">
        <h4>🎯 Phase 1: Enhanced Intelligence (Q2-Q3 2025)</h4>
        <ul>
            <li><strong>Multi-language Support:</strong> Bengali, Hindi, Tamil, Marathi</li>
            <li><strong>Advanced Analytics:</strong> Real-time performance dashboards</li>
            <li><strong>Apache Kafka:</strong> Event-driven architecture</li>
            <li><strong>Langflow Integration:</strong> Visual workflow designer</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="future-box">
        <h4>🚀 Phase 2: Enterprise Scaling (Q4 2025)</h4>
        <ul>
            <li><strong>MCP Server:</strong> Multi-tenant architecture</li>
            <li><strong>Cloud-Native:</strong> AWS/GCP deployment</li>
            <li><strong>AI Orchestration:</strong> CrewAI integration</li>
            <li><strong>Enterprise Security:</strong> SOC 2 compliance</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="future-box">
        <h4>🌐 Phase 3: Platform Extension (2026)</h4>
        <ul>
            <li><strong>SaaS Platform:</strong> Multi-NGO support</li>
            <li><strong>Marketplace:</strong> Agent marketplace</li>
            <li><strong>Mobile Apps:</strong> iOS/Android applications</li>
            <li><strong>API Economy:</strong> Third-party integrations</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Technical Innovation Section
st.header("⚡ Technical Innovations")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="highlight-box">
        <h4>🔄 Agent Orchestration</h4>
        <p>Dynamic load balancing and intelligent task routing between specialized agents</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="highlight-box">
        <h4>🧠 Shared Intelligence</h4>
        <p>Centralized knowledge base with real-time context sharing across all agents</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="highlight-box">
        <h4>📊 Real-time Analytics</h4>
        <p>Live performance monitoring with predictive insights and automated optimization</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="highlight-box">
        <h4>🔒 Enterprise Security</h4>
        <p>OAuth2 authentication, encrypted communications, and audit trail logging</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer-section">
    <h3 style="margin-bottom: 1rem; font-weight: 600;">🚀 Transforming NGO Operations Through AI</h3>
    <p style="font-size: 1.1rem; opacity: 0.9;">Sankalpiq Foundation Multi-Agent Platform</p>
    <p style="font-size: 0.9rem; margin-top: 1.5rem; opacity: 0.8;">
        Built with ❤️ for Social Impact | Enterprise-Grade | Open Source Foundation
    </p>
</div>
""", unsafe_allow_html=True)