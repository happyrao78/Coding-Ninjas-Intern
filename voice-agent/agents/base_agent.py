from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.agents.output_parsers import ReActSingleInputOutputParser
from langchain.schema import AgentAction, AgentFinish
from langchain.tools.render import render_text_description
from langchain_core.prompts import PromptTemplate
from langchain_core.language_models.base import BaseLanguageModel
from langchain_core.memory import BaseMemory
from langchain_core.callbacks import CallbackManagerForChainRun
from langchain_community.llms import GooglePalm
from langchain.memory import ConversationBufferWindowMemory
from typing import List, Dict, Any, Optional, Tuple
import google.generativeai as genai
from config.settings import settings
import asyncio
from datetime import datetime
import uuid

class CustomGeminiLLM(BaseLanguageModel):
    """Custom LLM wrapper for Google Gemini"""
    
    def __init__(self, api_key: str, model_name: str = "gemini-1.5-flash"):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        self.model_name = model_name
    
    def _call(self, prompt: str, stop: Optional[List[str]] = None, **kwargs) -> str:
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error in Gemini LLM call: {e}")
            return "मुझे इस सवाल का जवाब नहीं मिला। कृपया बाद में पुनः प्रयास करें।"
    
    async def _acall(self, prompt: str, stop: Optional[List[str]] = None, **kwargs) -> str:
        return self._call(prompt, stop, **kwargs)
    
    @property
    def _llm_type(self) -> str:
        return "gemini"

class BaseVoiceAgent:
    """Base class for voice agents with LangChain integration"""
    
    def __init__(self, name: str = "BaseAgent"):
        self.name = name
        self.conversation_id = str(uuid.uuid4())
        self.llm = CustomGeminiLLM(api_key=settings.gemini_api_key)
        self.memory = ConversationBufferWindowMemory(
            k=10,  # Remember last 10 exchanges
            return_messages=True,
            memory_key="chat_history"
        )
        self.tools = []
        self.agent_executor = None
        self.conversation_state = {}
        
    def add_tool(self, tool):
        """Add a tool to the agent"""
        self.tools.append(tool)
        
    def get_conversation_prompt(self) -> PromptTemplate:
        """Get the conversation prompt template"""
        template = """
        You are a helpful AI assistant for a voice-based conversation system.
        You are speaking with users in Hindi and English (Hinglish).
        Keep responses concise and natural for voice interaction.
        
        Current conversation state: {conversation_state}
        Chat History: {chat_history}
        
        Human: {input}
        
        Respond in Hindi/Hinglish in a conversational manner.
        """
        
        return PromptTemplate(
            input_variables=["conversation_state", "chat_history", "input"],
            template=template
        )
    
    def initialize_agent(self):
        """Initialize the agent executor"""
        if self.tools:
            # Create agent with tools
            prompt = self.get_conversation_prompt()
            
            # For now, we'll use a simple approach without ReAct
            # since we're focusing on voice conversation
            pass
    
    async def process_input(self, user_input: str, step: str = "general") -> str:
        """Process user input and return response"""
        try:
            # Update conversation state
            self.conversation_state.update({
                "current_step": step,
                "timestamp": datetime.now().isoformat(),
                "conversation_id": self.conversation_id
            })
            
            # Get response from LLM
            prompt = self.create_step_prompt(user_input, step)
            response = await self.llm._acall(prompt)
            
            # Store in memory
            self.memory.chat_memory.add_user_message(user_input)
            self.memory.chat_memory.add_ai_message(response)
            
            return response
            
        except Exception as e:
            print(f"Error processing input: {e}")
            return "माफ कीजिए, कुछ तकनीकी समस्या है। कृपया बाद में पुनः प्रयास करें।"
    
    def create_step_prompt(self, user_input: str, step: str) -> str:
        """Create prompt based on conversation step"""
        base_prompt = f"""
        You are a helpful AI assistant for voice conversations in Hindi/Hinglish.
        Current step: {step}
        Conversation ID: {self.conversation_id}
        
        Keep responses:
        - Concise (1-3 sentences)
        - Natural and conversational
        - In Hindi/Hinglish
        - Appropriate for voice interaction
        
        User said: {user_input}
        
        Respond appropriately:
        """
        
        return base_prompt
    
    def get_conversation_history(self) -> List[Dict]:
        """Get conversation history"""
        try:
            messages = self.memory.chat_memory.messages
            history = []
            for msg in messages:
                history.append({
                    "type": msg.type,
                    "content": msg.content,
                    "timestamp": datetime.now().isoformat()
                })
            return history
        except:
            return []
    
    def clear_memory(self):
        """Clear conversation memory"""
        self.memory.clear()
        self.conversation_id = str(uuid.uuid4())
        self.conversation_state = {}
    
    def get_state(self) -> Dict[str, Any]:
        """Get current agent state"""
        return {
            "name": self.name,
            "conversation_id": self.conversation_id,
            "state": self.conversation_state,
            "history_length": len(self.memory.chat_memory.messages) if self.memory else 0
        }