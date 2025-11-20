"""Simple chat mode for testing."""

import sys
import time
import threading
from auryx_agent.core.config import load_config
from auryx_agent.core.yellowfire_client import YellowFireClient
from auryx_agent.core.formatter import Formatter


def simple_chat():
    """Run a simple chat session."""
    fmt = Formatter()
    
    # Show logo
    print(fmt.logo())
    
    # Load configuration
    print(fmt.info("Loading configuration..."))
    config = load_config()
    
    if not config.yellowfire_api_key:
        print("\n" + fmt.error("YellowFire API key not configured!"))
        print(fmt.info("Please add your API key to ~/.config/auryx-agent/config.toml"))
        print(fmt.info("Get your free key: https://t.me/YellowFireBot -> /get_api"))
        return 1
    
    # Initialize client
    print(fmt.info(f"Initializing AI client..."))
    client = YellowFireClient(
        api_key=config.yellowfire_api_key,
        default_model=config.default_model
    )
    
    print("\n" + fmt.success("Ready!"))
    print(fmt.key_value("Model", fmt.model_badge(client.current_model, True)))
    print(fmt.key_value("Assistant", config.assistant_name))
    if config.system_prompt:
        print(fmt.key_value("Custom prompt", config.system_prompt[:50] + "..."))
    print(fmt.key_value("Temperature", str(config.temperature)))
    
    print(fmt.section("Commands", "💡"))
    print(fmt.command("/model <name>", "Switch model"))
    print(fmt.command("/models", "List available models"))
    print(fmt.command("/info", "Show current model info"))
    print(fmt.command("/clear", "Clear chat history"))
    print(fmt.command("/tools", "Enable/disable tool mode"))
    print(fmt.command("/save <file>", "Save conversation to file"))
    print(fmt.command("/load <file>", "Load conversation from file"))
    print(fmt.command("/exec <cmd>", "Execute shell command"))
    print(fmt.command("/help", "Show this help"))
    print(fmt.command("/quit or /exit", "Exit chat"))
    
    print(fmt.section("Capabilities", "🛠️"))
    print("  • Execute shell commands")
    print("  • Read/write files")
    print("  • Network diagnostics")
    print("  • System information")
    
    print("\n" + fmt.divider())
    
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
                    print("\n" + fmt.info("Goodbye! 👋"))
                    break
                
                elif cmd == "/clear":
                    client.clear_history()
                    print(fmt.success("Chat history cleared"))
                    continue
                
                elif cmd == "/models":
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
                        print(fmt.warning("Usage: /model <model_name>"))
                        continue
                    
                    new_model = cmd_parts[1]
                    if client.set_model(new_model):
                        print(fmt.success(f"Switched to {fmt.model_badge(client.current_model, True)}"))
                    else:
                        print(fmt.error(f"Model '{new_model}' not available"))
                        print(fmt.info("Use /models to see available models"))
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
                    
                    import json
                    filename = cmd_parts[1]
                    try:
                        history_data = [{"role": msg.role, "content": msg.content} for msg in client.chat_history]
                        with open(filename, 'w') as f:
                            json.dump(history_data, f, indent=2)
                        print(fmt.success(f"Conversation saved to {filename}"))
                    except Exception as e:
                        print(fmt.error(f"Failed to save: {e}"))
                    continue
                
                elif cmd == "/load":
                    if len(cmd_parts) < 2:
                        print(fmt.warning("Usage: /load <filename>"))
                        continue
                    
                    import json
                    from auryx_agent.core.yellowfire_client import ChatMessage
                    filename = cmd_parts[1]
                    try:
                        with open(filename, 'r') as f:
                            history_data = json.load(f)
                        client.chat_history = [ChatMessage(role=msg["role"], content=msg["content"]) for msg in history_data]
                        print(fmt.success(f"Conversation loaded from {filename}"))
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
                    print(fmt.key_value("Assistant Name", config.assistant_name))
                    print(fmt.key_value("Temperature", str(config.temperature)))
                    continue
                
                elif cmd == "/help":
                    print(fmt.section("Available Commands", "💡"))
                    print(fmt.command("/model <name>", "Switch AI model"))
                    print(fmt.command("/models", "List available models"))
                    print(fmt.command("/info", "Show current model info"))
                    print(fmt.command("/clear", "Clear chat history"))
                    print(fmt.command("/tools", "Toggle tool mode"))
                    print(fmt.command("/save <file>", "Save conversation"))
                    print(fmt.command("/load <file>", "Load conversation"))
                    print(fmt.command("/exec <cmd>", "Execute shell command"))
                    print(fmt.command("/help", "Show this help"))
                    print(fmt.command("/quit", "Exit chat"))
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
                print(response)
            except Exception as e:
                loading = False
                spinner_thread.join(timeout=0.2)
                print(fmt.error(str(e)))
        
        except KeyboardInterrupt:
            print("\n\n" + fmt.info("Goodbye! 👋"))
            break
        except EOFError:
            print("\n\n" + fmt.info("Goodbye! 👋"))
            break
    
    return 0


if __name__ == "__main__":
    exit(simple_chat())
