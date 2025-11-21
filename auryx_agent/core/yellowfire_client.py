"""YellowFire API client using official network_tools library."""

from dataclasses import dataclass
from typing import List, Optional
from network_tools import NetworkToolsAPI, GptModels


@dataclass
class ChatMessage:
    """Represents a chat message in the conversation history."""
    role: str  # 'user' or 'assistant'
    content: str


class YellowFireClient:
    """Client for interacting with YellowFire API using network_tools."""
    
    # Available models from YellowFire API (tested and working)
    AVAILABLE_MODELS = [
        "gpt-5-1-high",
        "gpt-5-1",
        "gpt-5-high",
        "gpt-5",
        "gpt-5-mini",
        # "gpt-5-nano",  # Error: Unknown error in process GPT
        # "gpt-5-chat-latest",  # Error: Unsupported model
        "gpt-oss",
        "gpt-4-5",
        "gpt-4-1",
        "gpt-4-1-mini",
        "gpt-4-1-nano",
        "gpt-4o",
        "chatgpt-4o",
        "gpt-4o-mini",
        # "gpt-3-5",  # Error: Unknown error in process GPT
        "o4-mini",
        "o3-high",
        "o3-mini",
        "o1",
        "claude-4-5-sonnet",
        "claude-4-5-sonnet-thinking",
        "claude-4-1-opus",
        "claude-4-opus",
        "claude-4-sonnet",
        "claude-4-1-opus-thinking",
        "claude-4-opus-thinking",
        "claude-4-sonnet-thinking",
        "claude-3-7-sonnet-thinking",
        "claude-3-5-sonnet",
        "claude-3-opus",
        "claude-3-sonnet",
        "claude-3-haiku",
        "command-r-plus",
        "command-a",
        "command-a-vision",
        "c4ai-aya-vision-32b",
        "deepseek-r1",
        "deepseek-v3",
        # "deepseek-r1-0528-qwen3-8b",  # Error: Unknown error in process GPT
        "deepseek-v3.2",
        "deepseek-v3.2-thinking",
        "grok-4",
        "grok-3",
        "gemini-3-0-pro",
        "gemini-2-5-pro",
        "gemini-2.5-flash",
        # "gemini-2.5-flash-lite",  # Error: Unknown error in process GPT
        "gemini-2.0-flash-lite",
        # "minimax-01",  # Error: Unknown error in process GPT
        "minimax-02",
        "glm-4.6",
        "kimi-k2-thinking",
    ]
    
    def __init__(self, api_key: str, default_model: str = "command-a"):
        """Initialize the YellowFire client."""
        if not api_key:
            raise ValueError("YellowFire API key cannot be empty")
        
        self.api_key = api_key
        self.current_model = default_model
        self.client = NetworkToolsAPI(api_key)
        self.chat_history: List[ChatMessage] = []
    
    def list_models(self) -> List[str]:
        """List all available models."""
        return self.AVAILABLE_MODELS
    
    def set_model(self, model_name: str) -> bool:
        """Set the active model."""
        if model_name in self.AVAILABLE_MODELS:
            self.current_model = model_name
            return True
        return False
    
    def generate(self, prompt: str, use_history: bool = True, timeout: int = 30) -> str:
        """Generate response from current model."""
        # Build chat history in network_tools format
        chat_history_list = []
        
        if use_history:
            for msg in self.chat_history:
                chat_history_list.append({
                    "role": msg.role,
                    "content": msg.content
                })
        
        try:
            # Use network_tools API
            response = self.client.chatgpt_api(
                prompt=prompt,
                model=self.current_model,
                chat_history=chat_history_list,
                file_path=None
            )
            
            generated_text = response.response.text
            
            # Update chat history
            if use_history:
                self.chat_history.append(ChatMessage(role="user", content=prompt))
                self.chat_history.append(ChatMessage(role="assistant", content=generated_text))
                
                # Auto-trim history to prevent context overflow
                self.trim_history(max_messages=20)
            
            return generated_text
            
        except Exception as e:
            raise Exception(f"YellowFire API error: {str(e)}")
    
    def clear_history(self) -> None:
        """Clear chat history."""
        self.chat_history.clear()
    
    def trim_history(self, max_messages: int = 20) -> None:
        """Trim chat history to keep only recent messages.
        
        Args:
            max_messages: Maximum number of messages to keep (excluding system prompt)
        """
        if not self.chat_history:
            return
        
        # Keep system prompt if it exists
        system_prompt = None
        messages = self.chat_history
        
        if messages and messages[0].role == "system":
            system_prompt = messages[0]
            messages = messages[1:]
        
        # Keep only last N messages
        if len(messages) > max_messages:
            messages = messages[-max_messages:]
        
        # Rebuild history
        self.chat_history.clear()
        if system_prompt:
            self.chat_history.append(system_prompt)
        self.chat_history.extend(messages)
    
    def get_balance(self, timeout: int = 10) -> float:
        """Get current account balance."""
        try:
            user_usage = self.client.get_usage()
            return float(user_usage.response.balance)
        except Exception as e:
            raise Exception(f"Failed to get balance: {str(e)}")
    
    def get_usage(self, limit: int = 10, timeout: int = 10) -> List[dict]:
        """Get usage history."""
        try:
            user_usage = self.client.get_usage()
            entries = []
            
            for request in user_usage.response.usage[:limit]:
                entries.append({
                    "timestamp": request.timestamp,
                    "comment": request.comment,
                    "balance_change": float(request.balance_change)
                })
            
            return entries
        except Exception as e:
            raise Exception(f"Failed to get usage: {str(e)}")
