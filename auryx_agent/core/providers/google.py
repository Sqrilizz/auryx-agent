"""Google Gemini API provider."""

from typing import List
from auryx_agent.core.providers.base import BaseProvider, ChatMessage


class GoogleProvider(BaseProvider):
    """Provider for Google Gemini API."""
    
    AVAILABLE_MODELS = [
        "gemini-2.5-flash",
        "gemini-2.5-pro",
        "gemini-2.0-flash-exp",
        "gemini-flash-latest",
        "gemini-pro-latest",
    ]
    
    def __init__(self, api_key: str, default_model: str = "gemini-2.5-flash"):
        """Initialize Google provider."""
        super().__init__(api_key, default_model)
        
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            self.genai = genai
        except ImportError:
            raise ImportError("Google Generative AI library not installed. Install with: pip install google-generativeai")
    
    def list_models(self) -> List[str]:
        """List all available models."""
        return self.AVAILABLE_MODELS
    
    def generate(self, prompt: str, use_history: bool = True, timeout: int = 30) -> str:
        """Generate response from current model."""
        try:
            model = self.genai.GenerativeModel(self.current_model)
            
            if use_history and self.chat_history:
                # Build chat history for Gemini
                chat = model.start_chat(history=[])
                
                # Add history (skip system messages as Gemini handles them differently)
                for msg in self.chat_history:
                    if msg.role != "system":
                        role = "user" if msg.role == "user" else "model"
                        chat.history.append({
                            "role": role,
                            "parts": [msg.content]
                        })
                
                response = chat.send_message(prompt)
            else:
                response = model.generate_content(prompt)
            
            generated_text = response.text
            
            if use_history:
                self.chat_history.append(ChatMessage(role="user", content=prompt))
                self.chat_history.append(ChatMessage(role="assistant", content=generated_text))
                self.trim_history(max_messages=20)
            
            return generated_text
            
        except Exception as e:
            raise Exception(f"Google API error: {str(e)}")
