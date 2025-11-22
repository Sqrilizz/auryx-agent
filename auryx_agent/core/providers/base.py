"""Base provider interface for AI APIs."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ChatMessage:
    """Represents a chat message in the conversation history."""
    role: str  # 'user', 'assistant', or 'system'
    content: str


class BaseProvider(ABC):
    """Abstract base class for AI providers."""
    
    def __init__(self, api_key: str, default_model: str):
        """Initialize provider.
        
        Args:
            api_key: API key for the provider
            default_model: Default model to use
        """
        if not api_key:
            raise ValueError(f"{self.__class__.__name__} API key cannot be empty")
        
        self.api_key = api_key
        self.current_model = default_model
        self.chat_history: List[ChatMessage] = []
    
    @abstractmethod
    def list_models(self) -> List[str]:
        """List all available models for this provider."""
        pass
    
    @abstractmethod
    def generate(self, prompt: str, use_history: bool = True, timeout: int = 30) -> str:
        """Generate response from current model.
        
        Args:
            prompt: User prompt
            use_history: Whether to use chat history
            timeout: Request timeout in seconds
            
        Returns:
            Generated text response
        """
        pass
    
    def set_model(self, model_name: str) -> bool:
        """Set the active model.
        
        Args:
            model_name: Name of the model to use
            
        Returns:
            True if model was set successfully
        """
        if model_name in self.list_models():
            self.current_model = model_name
            return True
        return False
    
    def clear_history(self) -> None:
        """Clear chat history."""
        self.chat_history.clear()
    
    def trim_history(self, max_messages: int = 20) -> None:
        """Trim chat history to keep only recent messages.
        
        Args:
            max_messages: Maximum number of messages to keep
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
    
    def get_balance(self, timeout: int = 10) -> Optional[float]:
        """Get current account balance (if supported).
        
        Returns:
            Balance or None if not supported
        """
        return None
    
    def get_usage(self, limit: int = 10, timeout: int = 10) -> Optional[List[dict]]:
        """Get usage history (if supported).
        
        Returns:
            Usage history or None if not supported
        """
        return None
