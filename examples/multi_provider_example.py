#!/usr/bin/env python3
"""Example: Using multiple AI providers with Auryx Agent."""

from auryx_agent.core.providers import ProviderFactory

# Example 1: Using YellowFire (default)
print("=== Example 1: YellowFire ===")
try:
    yellowfire = ProviderFactory.create(
        provider_name="yellowfire",
        api_key="your_yellowfire_key_here",
        model="command-a"
    )
    
    response = yellowfire.generate("Hello! What's 2+2?", use_history=False)
    print(f"Response: {response}\n")
except Exception as e:
    print(f"Error: {e}\n")


# Example 2: Using OpenAI
print("=== Example 2: OpenAI ===")
try:
    openai = ProviderFactory.create(
        provider_name="openai",
        api_key="sk-...",  # Your OpenAI API key
        model="gpt-4o-mini"
    )
    
    response = openai.generate("What is Python?", use_history=False)
    print(f"Response: {response}\n")
except Exception as e:
    print(f"Error: {e}\n")


# Example 3: Using Anthropic Claude
print("=== Example 3: Anthropic ===")
try:
    anthropic = ProviderFactory.create(
        provider_name="anthropic",
        api_key="sk-ant-...",  # Your Anthropic API key
        model="claude-3-5-sonnet-20241022"
    )
    
    response = anthropic.generate("Write a Python function to reverse a string", use_history=False)
    print(f"Response: {response}\n")
except Exception as e:
    print(f"Error: {e}\n")


# Example 4: Using Google Gemini
print("=== Example 4: Google Gemini ===")
try:
    google = ProviderFactory.create(
        provider_name="google",
        api_key="AIza...",  # Your Google API key
        model="gemini-1.5-flash"
    )
    
    response = google.generate("Explain quantum computing in simple terms", use_history=False)
    print(f"Response: {response}\n")
except Exception as e:
    print(f"Error: {e}\n")


# Example 5: Using Groq (fastest)
print("=== Example 5: Groq ===")
try:
    groq = ProviderFactory.create(
        provider_name="groq",
        api_key="gsk_...",  # Your Groq API key
        model="llama-3.3-70b-versatile"
    )
    
    response = groq.generate("What is the capital of France?", use_history=False)
    print(f"Response: {response}\n")
except Exception as e:
    print(f"Error: {e}\n")


# Example 6: Chat with history
print("=== Example 6: Chat with History ===")
try:
    client = ProviderFactory.create(
        provider_name="yellowfire",
        api_key="your_key_here",
        model="command-a"
    )
    
    # First message
    response1 = client.generate("My name is Alice", use_history=True)
    print(f"Response 1: {response1}")
    
    # Second message (should remember name)
    response2 = client.generate("What's my name?", use_history=True)
    print(f"Response 2: {response2}\n")
except Exception as e:
    print(f"Error: {e}\n")


# Example 7: List available providers
print("=== Example 7: Available Providers ===")
providers = ProviderFactory.list_providers()
print(f"Available providers: {', '.join(providers)}")

for provider in providers:
    default_model = ProviderFactory.get_default_model(provider)
    print(f"  - {provider}: default model = {default_model}")
