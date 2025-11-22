"""Groq API provider."""

from typing import List
from auryx_agent.core.providers.base import BaseProvider, ChatMessage


class GroqProvider(BaseProvider):
    """Provider for Groq API."""
    
    AVAILABLE_MODELS = [
        "llama-3.3-70b-versatile",
        "llama-4-scout",
        "kimi-k2",
        "gpt-oss-120b",
        "gpt-oss-20b",
        "llama-3.1-70b-versatile",
        "llama-3.1-8b-instant",
        "mixtral-8x7b-32768",
        "gemma2-9b-it",
    ]
    
    def __init__(self, api_key: str, default_model: str = "llama-3.3-70b-versatile"):
        """Initialize Groq provider."""
        super().__init__(api_key, default_model)
        
        try:
            from groq import Groq
            self.client = Groq(api_key=api_key)
        except ImportError:
            raise ImportError("Groq library not installed. Install with: pip install groq")
    
    def list_models(self) -> List[str]:
        """List all available models."""
        return self.AVAILABLE_MODELS
    
    def generate(self, prompt: str, use_history: bool = True, timeout: int = 30) -> str:
        """Generate response from current model."""
        messages = []
        
        if use_history and self.chat_history:
            for msg in self.chat_history:
                messages.append({"role": msg.role, "content": msg.content})
        
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = self.client.chat.completions.create(
                model=self.current_model,
                messages=messages,
                timeout=timeout
            )
            
            generated_text = response.choices[0].message.content
            
            if use_history:
                self.chat_history.append(ChatMessage(role="user", content=prompt))
                self.chat_history.append(ChatMessage(role="assistant", content=generated_text))
                self.trim_history(max_messages=20)
            
            return generated_text
            
        except Exception as e:
            raise Exception(f"Groq API error: {str(e)}")
