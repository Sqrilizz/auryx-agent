"""Simple chat mode for testing.

Author: sqrilizz
GitHub: https://github.com/Sqrilizz/auryx-agent
"""

import sys
import time
import threading
from auryx_agent.core.config import load_config
from auryx_agent.core.yellowfire_client import YellowFireClient
from auryx_agent.core.formatter import Formatter


def simple_chat():
    """Run a simple chat session."""
    fmt = Formatter()
    
    # Show compact logo
    print(fmt.logo())
    
    # Load configuration
    config = load_config()
    
    if not config.yellowfire_api_key:
        print(fmt.error("YellowFire API key not configured!"))
        print(fmt.info("Add your key to ~/.config/auryx-agent/config.toml"))
        print(fmt.info("Get free key: https://t.me/YellowFireBot -> /get_api"))
        return 1
    
    # Initialize client
    client = YellowFireClient(
        api_key=config.yellowfire_api_key,
        default_model=config.default_model
    )
    
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
                    print(fmt.command("/models", "List available models"))
                    print(fmt.command("/info", "Show current model info"))
                    print(fmt.command("/clear", "Clear chat history"))
                    print(fmt.command("/tools", "Toggle tool mode"))
                    print(fmt.command("/memory", "Show memory stats"))
                    print(fmt.command("/remember <text>", "Add to memory"))
                    print(fmt.command("/recall <query>", "Search memory"))
                    print(fmt.command("/forget", "Clear all memories"))
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
