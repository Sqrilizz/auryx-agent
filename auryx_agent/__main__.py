"""Main entry point for Auryx Agent CLI."""

import sys
import argparse
from typing import List, Optional

from auryx_agent.core.yellowfire_client import YellowFireClient


def get_model_suggestions(partial: str = "") -> List[str]:
    """Get model suggestions based on partial input.
    
    Args:
        partial: Partial model name to filter suggestions
        
    Returns:
        List of matching model names
    """
    all_models = YellowFireClient.AVAILABLE_MODELS
    
    if not partial:
        return all_models
    
    partial_lower = partial.lower()
    
    # Exact matches first
    exact_matches = [m for m in all_models if m.lower() == partial_lower]
    
    # Starts with matches
    starts_with = [m for m in all_models if m.lower().startswith(partial_lower) and m not in exact_matches]
    
    # Contains matches
    contains = [m for m in all_models if partial_lower in m.lower() and m not in exact_matches and m not in starts_with]
    
    return exact_matches + starts_with + contains


def print_model_suggestions(partial: str = "", max_suggestions: int = 10):
    """Print model suggestions to help user.
    
    Args:
        partial: Partial model name entered by user
        max_suggestions: Maximum number of suggestions to show
    """
    suggestions = get_model_suggestions(partial)
    
    if not suggestions:
        print(f"\n❌ Модель '{partial}' не найдена.")
        print("\n💡 Используйте 'auryx-agent models list' для просмотра всех доступных моделей")
        return
    
    if len(suggestions) == 1 and suggestions[0].lower() == partial.lower():
        # Exact match found
        return
    
    if partial:
        print(f"\n💡 Доступные модели (совпадения с '{partial}'):")
    else:
        print("\n💡 Доступные модели:")
    print("=" * 70)
    
    # Group by provider for better readability
    gpt_models = [m for m in suggestions if m.startswith(("gpt", "o1", "o3", "o4"))]
    claude_models = [m for m in suggestions if m.startswith("claude")]
    gemini_models = [m for m in suggestions if m.startswith("gemini")]
    deepseek_models = [m for m in suggestions if m.startswith("deepseek")]
    grok_models = [m for m in suggestions if m.startswith("grok")]
    other_models = [m for m in suggestions 
                   if not any(m.startswith(p) for p in ["gpt", "o1", "o3", "o4", "claude", "gemini", "deepseek", "grok"])]
    
    shown = 0
    
    if gpt_models and shown < max_suggestions:
        print("\n🤖 GPT/OpenAI:")
        for model in gpt_models[:max_suggestions - shown]:
            print(f"  • {model}")
            shown += 1
    
    if claude_models and shown < max_suggestions:
        print("\n🧠 Claude:")
        for model in claude_models[:max_suggestions - shown]:
            print(f"  • {model}")
            shown += 1
    
    if gemini_models and shown < max_suggestions:
        print("\n💎 Gemini:")
        for model in gemini_models[:max_suggestions - shown]:
            print(f"  • {model}")
            shown += 1
    
    if deepseek_models and shown < max_suggestions:
        print("\n🔍 DeepSeek:")
        for model in deepseek_models[:max_suggestions - shown]:
            print(f"  • {model}")
            shown += 1
    
    if grok_models and shown < max_suggestions:
        print("\n🚀 Grok:")
        for model in grok_models[:max_suggestions - shown]:
            print(f"  • {model}")
            shown += 1
    
    if other_models and shown < max_suggestions:
        print("\n🌟 Другие:")
        for model in other_models[:max_suggestions - shown]:
            print(f"  • {model}")
            shown += 1
    
    if len(suggestions) > max_suggestions:
        print(f"\n... и еще {len(suggestions) - max_suggestions} моделей")
    
    print("\n" + "=" * 70)
    print("💡 Используйте: auryx-agent --model <имя_модели>")
    print("💡 Полный список: auryx-agent models list")


def list_provider_models(provider_name: str):
    """List models available for a specific provider.
    
    Args:
        provider_name: Name of the provider (yellowfire, google, groq)
    """
    from auryx_agent.core.model_parser import get_provider_models, validate_provider
    
    provider_name = provider_name.lower()
    
    if not validate_provider(provider_name):
        print(f"\n❌ Неизвестный провайдер: {provider_name}")
        print("\n💡 Доступные провайдеры:")
        print("  • yellowfire - все модели (50+)")
        print("  • google     - Google AI модели")
        print("  • groq       - Groq модели")
        return
    
    models = get_provider_models(provider_name)
    
    print("\n" + "=" * 70)
    print(f"📋 Модели провайдера {provider_name.upper()} ({len(models)})")
    print("=" * 70)
    
    if provider_name == "yellowfire":
        print("\n💡 YellowFire предоставляет доступ ко всем моделям через единый API")
        print("   Используйте: auryx-agent --model <model_name>")
        print("\n" + "=" * 70)
        
        # Group by provider for YellowFire
        gpt_models = [m for m in models if m.startswith(("gpt", "o1", "o3", "o4"))]
        claude_models = [m for m in models if m.startswith("claude")]
        gemini_models = [m for m in models if m.startswith("gemini")]
        deepseek_models = [m for m in models if m.startswith("deepseek")]
        grok_models = [m for m in models if m.startswith("grok")]
        other_models = [m for m in models 
                       if not any(m.startswith(p) for p in ["gpt", "o1", "o3", "o4", "claude", "gemini", "deepseek", "grok"])]
        
        if gpt_models:
            print(f"\n🤖 GPT/OpenAI модели ({len(gpt_models)}):")
            for model in gpt_models:
                print(f"  • {model}")
        
        if claude_models:
            print(f"\n🧠 Claude модели ({len(claude_models)}):")
            for model in claude_models:
                print(f"  • {model}")
        
        if gemini_models:
            print(f"\n💎 Gemini модели ({len(gemini_models)}):")
            for model in gemini_models:
                print(f"  • {model}")
        
        if deepseek_models:
            print(f"\n🔍 DeepSeek модели ({len(deepseek_models)}):")
            for model in deepseek_models:
                print(f"  • {model}")
        
        if grok_models:
            print(f"\n🚀 Grok модели ({len(grok_models)}):")
            for model in grok_models:
                print(f"  • {model}")
        
        if other_models:
            print(f"\n🌟 Другие модели ({len(other_models)}):")
            for model in other_models:
                print(f"  • {model}")
    else:
        # For other providers, show direct API usage
        print(f"\n💡 Используйте: auryx-agent --model {provider_name}:<model_name>")
        print(f"   Пример: auryx-agent --model {provider_name}:{models[0] if models else 'model'}")
        print("\n" + "=" * 70)
        
        for model in models:
            print(f"  • {model}")
    
    print("\n" + "=" * 70)


def list_all_models():
    """List all available models grouped by provider."""
    all_models = YellowFireClient.AVAILABLE_MODELS
    
    print("\n" + "=" * 70)
    print(f"📋 Все модели YellowFire ({len(all_models)})")
    print("=" * 70)
    print("\n💡 YellowFire - доступ ко всем моделям через единый API")
    print("=" * 70)
    
    # Group by provider
    gpt_models = [m for m in all_models if m.startswith(("gpt", "o1", "o3", "o4"))]
    claude_models = [m for m in all_models if m.startswith("claude")]
    gemini_models = [m for m in all_models if m.startswith("gemini")]
    deepseek_models = [m for m in all_models if m.startswith("deepseek")]
    grok_models = [m for m in all_models if m.startswith("grok")]
    other_models = [m for m in all_models 
                   if not any(m.startswith(p) for p in ["gpt", "o1", "o3", "o4", "claude", "gemini", "deepseek", "grok"])]
    
    print(f"\n🤖 GPT/OpenAI модели ({len(gpt_models)}):")
    for model in gpt_models:
        print(f"  • {model}")
    
    print(f"\n🧠 Claude модели ({len(claude_models)}):")
    for model in claude_models:
        print(f"  • {model}")
    
    print(f"\n💎 Gemini модели ({len(gemini_models)}):")
    for model in gemini_models:
        print(f"  • {model}")
    
    print(f"\n🔍 DeepSeek модели ({len(deepseek_models)}):")
    for model in deepseek_models:
        print(f"  • {model}")
    
    print(f"\n🚀 Grok модели ({len(grok_models)}):")
    for model in grok_models:
        print(f"  • {model}")
    
    print(f"\n🌟 Другие модели ({len(other_models)}):")
    for model in other_models:
        print(f"  • {model}")
    
    print("\n" + "=" * 70)


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser for CLI.
    
    Returns:
        Configured argument parser
    """
    parser = argparse.ArgumentParser(
        prog="auryx-agent",
        description="Auryx CLI Agent - AI-powered network diagnostic tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  auryx-agent                                    # Start in chat mode (YellowFire)
  auryx-agent --model gpt-4o-mini                # Use model via YellowFire
  auryx-agent --model openai:gpt-4o              # Use OpenAI API directly
  auryx-agent --model anthropic:claude-3-5-sonnet # Use Anthropic API directly
  auryx-agent models list                        # List all available models
  auryx-agent models search gpt                  # Search for models
  auryx-agent ping google.com                    # Direct command mode
  auryx-agent balance                            # Check account balance
  
For more information, visit: https://github.com/Badim41/network_tools
        """
    )
    
    parser.add_argument(
        "--model",
        type=str,
        help="AI model to use. Format: 'model' (YellowFire) or 'provider:model' (direct API). "
             "Examples: gpt-4o-mini, openai:gpt-4o, anthropic:claude-3-5-sonnet"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )
    
    # Subcommands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Chat subcommand
    subparsers.add_parser("chat", help="Start interactive chat mode")
    
    # Models subcommand
    models_parser = subparsers.add_parser("models", help="Manage AI models")
    models_subparsers = models_parser.add_subparsers(dest="models_command", help="Model commands")
    
    # models list
    models_subparsers.add_parser("list", help="List all available models")
    
    # models search
    search_parser = models_subparsers.add_parser("search", help="Search for models")
    search_parser.add_argument("query", type=str, help="Search query (e.g., 'gpt', 'claude')")
    
    # models provider
    provider_parser = models_subparsers.add_parser("provider", help="List models for specific provider")
    provider_parser.add_argument("provider", type=str, help="Provider name (yellowfire, google, groq)")
    
    # models test
    test_parser = models_subparsers.add_parser("test", help="Test models from provider")
    test_parser.add_argument("provider", type=str, help="Provider name (yellowfire, google, groq)")
    test_parser.add_argument("--prompt", type=str, default="Что такое Python? Ответь кратко в 1-2 предложениях.", 
                           help="Test prompt")
    
    # Network commands
    ping_parser = subparsers.add_parser("ping", help="Ping a host")
    ping_parser.add_argument("host", type=str, help="Host to ping")
    
    dns_parser = subparsers.add_parser("dns", help="DNS lookup")
    dns_parser.add_argument("host", type=str, help="Host to lookup")
    
    ports_parser = subparsers.add_parser("ports", help="Port scan")
    ports_parser.add_argument("host", type=str, help="Host to scan")
    
    traceroute_parser = subparsers.add_parser("traceroute", help="Traceroute to host")
    traceroute_parser.add_argument("host", type=str, help="Host to trace")
    
    # Utility commands
    subparsers.add_parser("balance", help="Check account balance")
    subparsers.add_parser("usage", help="Show usage history")
    subparsers.add_parser("history", help="Show command history")
    subparsers.add_parser("report", help="Generate session report")
    
    return parser


def main():
    """Main entry point for CLI."""
    parser = create_parser()
    
    # Parse model specification if provided
    model_spec = None
    if "--model" in sys.argv:
        from auryx_agent.core.model_parser import parse_model_spec
        
        model_index = sys.argv.index("--model")
        
        # Check if there's a value after --model
        if model_index + 1 >= len(sys.argv) or sys.argv[model_index + 1].startswith("-"):
            print("\n❌ Ошибка: --model требует указания имени модели")
            print("\n💡 Форматы:")
            print("  • model_name         → YellowFire (все модели)")
            print("  • google:model_name  → Google AI API")
            print("  • groq:model_name    → Groq API")
            print_model_suggestions()
            sys.exit(1)
        
        model_value = sys.argv[model_index + 1]
        
        # Parse model specification
        try:
            model_spec = parse_model_spec(model_value)
            
            # No provider prefix = YellowFire (check if model exists)
            if model_spec.provider is None:
                if model_spec.model not in YellowFireClient.AVAILABLE_MODELS:
                    print(f"\n❌ Ошибка: Модель '{model_spec.model}' не найдена в YellowFire")
                    print_model_suggestions(model_spec.model)
                    sys.exit(1)
            else:
                # Explicit provider specified (openai:, anthropic:, etc.)
                print(f"\n✓ Будет использован {model_spec.provider.upper()} API для модели {model_spec.model}")
        except ValueError as e:
            print(f"\n❌ Ошибка: {e}")
            sys.exit(1)
    
    args = parser.parse_args()
    
    # Handle models subcommand
    if args.command == "models":
        if args.models_command == "list":
            list_all_models()
            sys.exit(0)
        elif args.models_command == "search":
            print_model_suggestions(args.query, max_suggestions=50)
            sys.exit(0)
        elif args.models_command == "provider":
            list_provider_models(args.provider)
            sys.exit(0)
        else:
            print("\n💡 Используйте:")
            print("  auryx-agent models list              # Показать все модели YellowFire")
            print("  auryx-agent models search <query>    # Поиск моделей")
            print("  auryx-agent models provider <name>   # Модели конкретного провайдера")
            sys.exit(0)
    
    # Handle chat subcommand
    if args.command == "chat":
        from auryx_agent.cli.simple_chat import simple_chat
        sys.exit(simple_chat(model_spec))
    
    # Handle balance command
    if args.command == "balance":
        from auryx_agent.core.config import load_config
        from auryx_agent.core.formatter import Formatter
        
        fmt = Formatter()
        config = load_config()
        
        if not config.yellowfire_api_key:
            print(fmt.error("YellowFire API key not configured!"))
            sys.exit(1)
        
        client = YellowFireClient(api_key=config.yellowfire_api_key)
        
        try:
            balance = client.get_balance()
            print(fmt.section("Account Balance", "💰"))
            print(fmt.key_value("Balance", f"{balance:.4f} credits"))
            sys.exit(0)
        except Exception as e:
            print(fmt.error(f"Failed to get balance: {e}"))
            sys.exit(1)
    
    # Handle usage command
    if args.command == "usage":
        from auryx_agent.core.config import load_config
        from auryx_agent.core.formatter import Formatter
        from datetime import datetime
        
        fmt = Formatter()
        config = load_config()
        
        if not config.yellowfire_api_key:
            print(fmt.error("YellowFire API key not configured!"))
            sys.exit(1)
        
        client = YellowFireClient(api_key=config.yellowfire_api_key)
        
        try:
            usage = client.get_usage(limit=20)
            print(fmt.section("Usage History", "📊"))
            
            for entry in usage:
                dt = datetime.fromtimestamp(entry.timestamp)
                date_str = dt.strftime("%Y-%m-%d %H:%M:%S")
                change = f"{entry.balance_change:+.4f}"
                color = fmt.colors.GREEN if entry.balance_change > 0 else fmt.colors.RED
                print(f"{date_str} | {color}{change}{fmt.colors.RESET} | {entry.comment}")
            
            sys.exit(0)
        except Exception as e:
            print(fmt.error(f"Failed to get usage: {e}"))
            sys.exit(1)
    
    # Handle network commands
    if args.command == "ping":
        from auryx_agent.tools.network_tools import NetworkTools
        from auryx_agent.core.formatter import Formatter
        
        fmt = Formatter()
        result = NetworkTools.ping(args.host)
        
        if result["success"]:
            print(fmt.section(f"Ping {args.host}", "🏓"))
            print(result["output"])
        else:
            print(fmt.error(f"Ping failed: {result['error']}"))
            sys.exit(1)
        sys.exit(0)
    
    if args.command == "dns":
        from auryx_agent.tools.network_tools import NetworkTools
        from auryx_agent.core.formatter import Formatter
        
        fmt = Formatter()
        result = NetworkTools.dns_lookup(args.host)
        
        if result["success"]:
            print(fmt.section(f"DNS Lookup: {args.host}", "🔍"))
            print(fmt.key_value("Hostname", result["hostname"]))
            if result["aliases"]:
                print(fmt.key_value("Aliases", ", ".join(result["aliases"])))
            print(fmt.key_value("IP Addresses", ", ".join(result["addresses"])))
        else:
            print(fmt.error(f"DNS lookup failed: {result['error']}"))
            sys.exit(1)
        sys.exit(0)
    
    if args.command == "ports":
        from auryx_agent.tools.network_tools import NetworkTools
        from auryx_agent.core.formatter import Formatter
        
        fmt = Formatter()
        print(fmt.info(f"Scanning ports on {args.host}..."))
        result = NetworkTools.scan_ports(args.host)
        
        print(fmt.section(f"Port Scan: {args.host}", "🔌"))
        print(fmt.key_value("Total scanned", str(result["total_scanned"])))
        
        if result["open_ports"]:
            print(fmt.key_value("Open ports", ", ".join(map(str, result["open_ports"]))))
        else:
            print(fmt.warning("No open ports found"))
        
        sys.exit(0)
    
    if args.command == "traceroute":
        from auryx_agent.tools.network_tools import NetworkTools
        from auryx_agent.core.formatter import Formatter
        
        fmt = Formatter()
        print(fmt.info(f"Tracing route to {args.host}..."))
        result = NetworkTools.traceroute(args.host)
        
        if result["success"]:
            print(fmt.section(f"Traceroute: {args.host}", "🗺️"))
            print(result["output"])
        else:
            print(fmt.error(f"Traceroute failed: {result['error']}"))
            sys.exit(1)
        sys.exit(0)
    
    if args.command == "history":
        print("📜 Command history feature coming soon!")
        sys.exit(0)
    
    if args.command == "report":
        print("📄 Session report feature coming soon!")
        sys.exit(0)
    
    # Default: start chat mode
    from auryx_agent.cli.simple_chat import simple_chat
    sys.exit(simple_chat(model_spec))


if __name__ == "__main__":
    main()
