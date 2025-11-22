"""Simple chat mode for testing.

Author: sqrilizz
GitHub: https://github.com/Sqrilizz/auryx-agent
"""

import sys
import time
import threading
import json
import os
from pathlib import Path
from auryx_agent.core.config import load_config
from auryx_agent.core.yellowfire_client import YellowFireClient, ChatMessage
from auryx_agent.core.formatter import Formatter
from auryx_agent.core.providers.factory import ProviderFactory
from auryx_agent.core.providers.base import BaseProvider


def get_history_file() -> Path:
    """Get path to chat history file."""
    config_dir = Path.home() / ".config" / "auryx-agent"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / "chat_history.json"


def load_chat_history(client) -> int:
    """Load chat history from file.
    
    Returns:
        Number of messages loaded
    """
    history_file = get_history_file()
    
    if not history_file.exists():
        return 0
    
    try:
        with open(history_file, 'r', encoding='utf-8') as f:
            history_data = json.load(f)
        
        # Load messages
        client.chat_history = [
            ChatMessage(role=msg["role"], content=msg["content"]) 
            for msg in history_data
        ]
        
        return len(client.chat_history)
    except Exception as e:
        print(f"Warning: Failed to load chat history: {e}")
        return 0


def save_chat_history(client) -> bool:
    """Save chat history to file.
    
    Returns:
        True if saved successfully
    """
    history_file = get_history_file()
    
    try:
        history_data = [
            {"role": msg.role, "content": msg.content} 
            for msg in client.chat_history
        ]
        
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history_data, f, indent=2, ensure_ascii=False)
        
        return True
    except Exception as e:
        print(f"Warning: Failed to save chat history: {e}")
        return False


def simple_chat(model_spec=None):
    """Run a simple chat session.
    
    Args:
        model_spec: Optional ModelSpec with provider and model info
    """
    fmt = Formatter()
    
    # Show compact logo
    print(fmt.logo())
    
    # Load configuration
    config = load_config()
    
    # Determine which provider to use
    if model_spec and model_spec.provider:
        # Explicit provider specified
        provider_name = model_spec.provider
        model_name = model_spec.model
        
        # Check if API key is configured
        api_key_map = {
            "yellowfire": config.yellowfire_api_key,
            "google": config.google_api_key,
            "groq": config.groq_api_key,
        }
        
        api_key = api_key_map.get(provider_name)
        if not api_key:
            print(fmt.error(f"{provider_name.upper()} API key not configured!"))
            print(fmt.info(f"Add your key to ~/.config/auryx-agent/config.toml"))
            return 1
        
        # Create provider using factory
        try:
            client = ProviderFactory.create(
                provider_name=provider_name,
                api_key=api_key,
                model=model_name
            )
        except Exception as e:
            print(fmt.error(f"Failed to initialize {provider_name.upper()} provider: {e}"))
            return 1
    else:
        # Default: YellowFire
        if not config.yellowfire_api_key:
            print(fmt.error("YellowFire API key not configured!"))
            print(fmt.info("Add your key to ~/.config/auryx-agent/config.toml"))
            print(fmt.info("Get free key: https://t.me/YellowFireBot -> /get_api"))
            return 1
        
        model_name = model_spec.model if model_spec else config.default_model
        try:
            client = ProviderFactory.create(
                provider_name="yellowfire",
                api_key=config.yellowfire_api_key,
                model=model_name
            )
        except Exception as e:
            print(fmt.error(f"Failed to initialize YellowFire provider: {e}"))
            return 1
    
    # Load previous chat history
    loaded_messages = load_chat_history(client)
    if loaded_messages > 0:
        print(fmt.success(f"📜 Loaded {loaded_messages} messages from previous session"))
    
    # Compact info box
    print(fmt.box(
        f"💻 Code  🌐 Web  🧠 Memory  🖥️ System  📡 Network\n"
        f"/help commands  •  /models list  •  /memory stats\n"
        f"{fmt.colors.DIM}by sqrilizz{fmt.colors.RESET}",
        width=58,
        title=""
    ))
    
    print(fmt.divider(60))
    print(f"{fmt.colors.BRIGHT_MAGENTA}🤖 Chatting with {fmt.model_badge(client.current_model, True)}{fmt.colors.RESET}")
    print(fmt.divider(60))
    
    # Initialize agent
    from auryx_agent.core.agent import Agent
    agent = Agent(client)
    use_tools = True
    
    # Chat loop
    while True:
        try:
            user_input = input(f"\n{fmt.colors.BRIGHT_GREEN}{fmt.colors.BOLD}You:{fmt.colors.RESET} ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.startswith("/"):
                cmd_parts = user_input.split(maxsplit=1)
                cmd = cmd_parts[0].lower()
                
                if cmd in ["/quit", "/exit"]:
                    save_chat_history(client)
                    print("\n" + fmt.info("Goodbye! 👋"))
                    break
                
                elif cmd == "/clear":
                    client.clear_history()
                    save_chat_history(client)
                    print(fmt.success("Chat history cleared"))
                    continue
                
                elif cmd == "/models":
                    if len(cmd_parts) > 1:
                        # /models <provider>
                        provider_arg = cmd_parts[1].lower()
                        from auryx_agent.core.model_parser import get_provider_models, validate_provider
                        
                        if not validate_provider(provider_arg):
                            print(fmt.error(f"Unknown provider: {provider_arg}"))
                            print(fmt.info("Available: yellowfire, google, groq"))
                            continue
                        
                        models = get_provider_models(provider_arg)
                        print(fmt.section(f"{provider_arg.upper()} models ({len(models)})", "📋"))
                        for model in models[:20]:
                            print(f"  • {model}")
                        if len(models) > 20:
                            print(fmt.info(f"... and {len(models) - 20} more"))
                    else:
                        # /models (current provider)
                        models = client.list_models()
                        print(fmt.section(f"Available models ({len(models)})", "📋"))
                        for model in models[:10]:
                            if model == client.current_model:
                                print(f"  → {fmt.model_badge(model, True)}")
                            else:
                                print(f"    {fmt.model_badge(model)}")
                        if len(models) > 10:
                            print(fmt.info(f"... and {len(models) - 10} more. Use 'auryx-agent models list' to see all"))
                    continue
                
                elif cmd == "/model":
                    if len(cmd_parts) < 2:
                        print(fmt.warning("Usage: /model <model_name> or /model <provider:model_name>"))
                        print(fmt.info("Examples:"))
                        print("  /model gpt-4o-mini                → YellowFire (default)")
                        print("  /model google:gemini-1.5-pro      → Google AI API")
                        print("  /model groq:llama-3.3-70b         → Groq API")
                        continue
                    
                    from auryx_agent.core.model_parser import parse_model_spec
                    
                    model_input = cmd_parts[1]
                    
                    try:
                        model_spec = parse_model_spec(model_input)
                        
                        if model_spec.provider is not None:
                            # Explicit provider specified - need to recreate client
                            provider_name = model_spec.provider
                            model_name = model_spec.model
                            
                            # Get API key for provider
                            api_key_map = {
                                "yellowfire": config.yellowfire_api_key,
                                "google": config.google_api_key,
                                "groq": config.groq_api_key,
                            }
                            
                            api_key = api_key_map.get(provider_name)
                            if not api_key:
                                print(fmt.error(f"{provider_name.upper()} API key not configured!"))
                                print(fmt.info(f"Add your key to ~/.config/auryx-agent/config.toml"))
                                continue
                            
                            # Save current history
                            save_chat_history(client)
                            
                            # Create new client with different provider
                            try:
                                print(fmt.info(f"Switching to {provider_name.upper()} provider..."))
                                client = ProviderFactory.create(
                                    provider_name=provider_name,
                                    api_key=api_key,
                                    model=model_name
                                )
                                # Reload history
                                load_chat_history(client)
                                # Recreate agent with new client
                                agent = Agent(client)
                                print(fmt.success(f"Switched to {fmt.model_badge(client.current_model, True)} ({provider_name.upper()})"))
                            except Exception as e:
                                print(fmt.error(f"Failed to switch provider: {e}"))
                            continue
                        
                        # YellowFire model (no provider prefix)
                        if client.set_model(model_spec.model):
                            print(fmt.success(f"Switched to {fmt.model_badge(client.current_model, True)}"))
                        else:
                            print(fmt.error(f"Model '{model_spec.model}' not available"))
                            print(fmt.info("Use /models to see available models"))
                    except ValueError as e:
                        print(fmt.error(str(e)))
                    continue
                
                elif cmd == "/tools":
                    use_tools = not use_tools
                    status = "enabled" if use_tools else "disabled"
                    print(fmt.success(f"Tool mode {status}"))
                    continue
                
                elif cmd == "/save":
                    if len(cmd_parts) < 2:
                        print(fmt.warning("Usage: /save <filename>"))
                        continue
                    
                    filename = cmd_parts[1]
                    try:
                        history_data = [{"role": msg.role, "content": msg.content} for msg in client.chat_history]
                        with open(filename, 'w', encoding='utf-8') as f:
                            json.dump(history_data, f, indent=2, ensure_ascii=False)
                        print(fmt.success(f"Conversation saved to {filename}"))
                    except Exception as e:
                        print(fmt.error(f"Failed to save: {e}"))
                    continue
                
                elif cmd == "/load":
                    if len(cmd_parts) < 2:
                        print(fmt.warning("Usage: /load <filename>"))
                        continue
                    
                    filename = cmd_parts[1]
                    try:
                        with open(filename, 'r', encoding='utf-8') as f:
                            history_data = json.load(f)
                        client.chat_history = [ChatMessage(role=msg["role"], content=msg["content"]) for msg in history_data]
                        save_chat_history(client)
                        print(fmt.success(f"Conversation loaded from {filename} ({len(client.chat_history)} messages)"))
                    except Exception as e:
                        print(fmt.error(f"Failed to load: {e}"))
                    continue
                
                elif cmd == "/exec":
                    if len(cmd_parts) < 2:
                        print(fmt.warning("Usage: /exec <command>"))
                        continue
                    
                    import subprocess
                    command = user_input[6:].strip()  # Remove "/exec "
                    try:
                        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
                        if result.stdout:
                            print(result.stdout)
                        if result.stderr:
                            print(fmt.warning(result.stderr))
                    except Exception as e:
                        print(fmt.error(f"Command failed: {e}"))
                    continue
                
                elif cmd == "/info":
                    print(fmt.section("Current Session Info", "ℹ️"))
                    print(fmt.key_value("Current Model", fmt.model_badge(client.current_model, True)))
                    print(fmt.key_value("Tool Mode", "Enabled" if use_tools else "Disabled"))
                    print(fmt.key_value("History Length", str(len(client.chat_history))))
                    print(fmt.key_value("History File", str(get_history_file())))
                    print(fmt.key_value("Assistant Name", config.assistant_name))
                    print(fmt.key_value("Temperature", str(config.temperature)))
                    continue
                
                elif cmd == "/memory":
                    if agent.memory:
                        stats = agent.memory.stats()
                        print(fmt.section("Memory Statistics", "🧠"))
                        print(fmt.key_value("Total memories", str(stats['total'])))
                        print(fmt.key_value("Average importance", str(stats['avg_importance'])))
                        if stats['by_category']:
                            print("\nBy category:")
                            for cat, count in stats['by_category'].items():
                                print(f"  • {cat}: {count}")
                        if stats.get('most_accessed'):
                            print(f"\nMost accessed: {stats['most_accessed'][:60]}...")
                    else:
                        print(fmt.warning("Memory system is disabled"))
                    continue
                
                elif cmd == "/remember":
                    if len(cmd_parts) < 2:
                        print(fmt.warning("Usage: /remember <text>"))
                        continue
                    
                    if agent.memory:
                        text = user_input[10:].strip()  # Remove "/remember "
                        
                        # Check for duplicates
                        existing = agent.memory.search(text, limit=1)
                        if existing and existing[0].content.lower() == text.lower():
                            print(fmt.warning("This memory already exists"))
                            continue
                        
                        memory_id = agent.memory.add(text, category="user_note", importance=7)
                        print(fmt.success(f"Remembered: {text[:60]}..."))
                    else:
                        print(fmt.warning("Memory system is disabled"))
                    continue
                
                elif cmd == "/recall":
                    if len(cmd_parts) < 2:
                        print(fmt.warning("Usage: /recall <query>"))
                        continue
                    
                    if agent.memory:
                        query = cmd_parts[1]
                        results = agent.memory.search(query, limit=5)
                        if results:
                            print(fmt.section(f"Found {len(results)} memories", "🔍"))
                            for mem in results:
                                print(f"  [{mem.category}] {mem.content}")
                        else:
                            print(fmt.info("No memories found"))
                    else:
                        print(fmt.warning("Memory system is disabled"))
                    continue
                
                elif cmd == "/forget":
                    if agent.memory:
                        agent.memory.clear()
                        print(fmt.success("All memories cleared"))
                    else:
                        print(fmt.warning("Memory system is disabled"))
                    continue
                
                elif cmd == "/help":
                    print(fmt.section("Available Commands", "💡"))
                    print(fmt.command("/model <name>", "Switch AI model"))
                    print(fmt.command("/models [provider]", "List models (optional: yellowfire/google/groq)"))
                    print(fmt.command("/info", "Show session info & history"))
                    print(fmt.command("/clear", "Clear chat history"))
                    print(fmt.command("/tools", "Toggle tool mode"))
                    print(fmt.command("/memory", "Show memory stats"))
                    print(fmt.command("/remember <text>", "Add to memory"))
                    print(fmt.command("/recall <query>", "Search memory"))
                    print(fmt.command("/forget", "Clear all memories"))
                    print(fmt.command("/save <file>", "Export conversation"))
                    print(fmt.command("/load <file>", "Import conversation"))
                    print(fmt.command("/exec <cmd>", "Execute shell command"))
                    print(fmt.command("/help", "Show this help"))
                    print(fmt.command("/quit", "Save & exit chat"))
                    print(fmt.info("\n💡 History auto-saves between sessions"))
                    continue
                
                else:
                    print(fmt.warning(f"Unknown command: {cmd}. Type /help for available commands"))
                    continue
            
            # Generate response with loading animation
            loading = True
            spinner_chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
            spinner_idx = [0]
            
            def show_spinner():
                while loading:
                    sys.stdout.write(f"\r{fmt.colors.BRIGHT_MAGENTA}{spinner_chars[spinner_idx[0] % len(spinner_chars)]} Thinking...{fmt.colors.RESET}")
                    sys.stdout.flush()
                    spinner_idx[0] += 1
                    time.sleep(0.1)
                sys.stdout.write("\r" + " " * 20 + "\r")
                sys.stdout.flush()
            
            spinner_thread = threading.Thread(target=show_spinner, daemon=True)
            spinner_thread.start()
            
            try:
                if use_tools:
                    response = agent.process(user_input)
                else:
                    response = client.generate(user_input, use_history=True, timeout=60)
                
                loading = False
                spinner_thread.join(timeout=0.2)
                
                # Render markdown formatting
                formatted_response = fmt.render_markdown(response)
                print(formatted_response)
                
                # Auto-save history after each exchange
                save_chat_history(client)
            except Exception as e:
                loading = False
                spinner_thread.join(timeout=0.2)
                print(fmt.error(str(e)))
        
        except KeyboardInterrupt:
            save_chat_history(client)
            print("\n\n" + fmt.info("Goodbye! 👋"))
            break
        except EOFError:
            save_chat_history(client)
            print("\n\n" + fmt.info("Goodbye! 👋"))
            break
    
    # Final save on exit
    save_chat_history(client)
    return 0


if __name__ == "__main__":
    exit(simple_chat())
