# 🔥 Auryx Agent

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/Sqrilizz/auryx-agent.svg)](https://github.com/Sqrilizz/auryx-agent/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/Sqrilizz/auryx-agent.svg)](https://github.com/Sqrilizz/auryx-agent/issues)

> AI-powered CLI agent with access to 50+ AI models through YellowFire API

Auryx Agent is a powerful command-line interface that brings AI capabilities directly to your terminal. Chat with GPT-5, Claude 4, Gemini, and many other models, execute system commands, perform network diagnostics, and automate your workflow - all from one place.

## ✨ Features

### 🤖 Multi-Model AI Chat
- **50+ AI Models**: GPT-5, Claude 4, Gemini 3.0, DeepSeek, Grok, and more
- **Interactive Chat**: Natural conversation with context preservation
- **Tool Mode**: AI can execute commands and interact with your system
- **Session Management**: Save and load conversations

### 🛠️ System Tools
- **Command Execution**: Run shell commands directly from chat
- **File Operations**: Read, write, and manage files
- **Network Diagnostics**: Ping, DNS lookup, port scanning, traceroute
- **System Information**: Get detailed system info

### 💰 Cost-Effective
- **2x Cheaper** than official APIs for text models
- **2x Cheaper** for image generation
- **Free $1 Balance** to get started

## 📦 Installation

### Quick Install

```bash
pip install git+https://github.com/Sqrilizz/auryx-agent.git
```

### From Source

```bash
git clone https://github.com/Sqrilizz/auryx-agent.git
cd auryx-agent
pip install -e .
```

## 🚀 Quick Start

### 1. Get Your API Key

Get a free API key with $1 balance:
1. Go to [@GPT4_Unlimit_bot](https://t.me/GPT4_Unlimit_bot?start=api)
2. Send `/get_api`
3. Copy your API key

### 2. Configure

Create config file at `~/.config/auryx-agent/config.toml`:

```toml
[yellowfire]
api_key = "your_api_key_here"

[agent]
default_model = "gpt-4o-mini"
assistant_name = "Auryx"
temperature = 0.7
```

### 3. Start Chatting

```bash
auryx-agent chat
```

## 📖 Usage

### Interactive Chat

```bash
# Start chat with default model
auryx-agent chat

# Chat commands:
/model gpt-5              # Switch to GPT-5
/models                   # List all available models
/info                     # Show current session info
/tools                    # Toggle tool mode
/save session.json        # Save conversation
/load session.json        # Load conversation
/exec ls -la             # Execute shell command
/help                     # Show all commands
/quit                     # Exit
```

### Direct Commands

```bash
# Check account balance
auryx-agent balance

# View usage history
auryx-agent usage

# Network diagnostics
auryx-agent ping google.com
auryx-agent dns github.com
auryx-agent ports localhost
auryx-agent traceroute 8.8.8.8

# List all models
auryx-agent models list

# Search for models
auryx-agent models search claude
```

## 🎯 Available Models

### Text Models (50+)

**OpenAI:**
- GPT-5 (1-high, 1, high, mini, nano)
- GPT-4.5, GPT-4.1, GPT-4o
- o4-mini, o3-mini, o1

**Anthropic:**
- Claude 4.5 Sonnet (+ Thinking)
- Claude 4 Opus (+ Thinking)
- Claude 3.7, 3.5 Sonnet, 3 Opus

**Google:**
- Gemini 3.0 Pro
- Gemini 2.5 Pro/Flash

**Others:**
- DeepSeek R1, V3, V3.2
- Grok 3, Grok 4
- Command R+, Reka Flash
- Minimax-01/02, Kimi K2

### Image Models
- DALL-E 3
- Stable Diffusion (Ultra, XL)
- Flux Pro
- Recraft V3
- Kandinsky

## 💡 Examples

### Chat with AI

```bash
$ auryx-agent chat
You: Explain quantum computing in simple terms

Auryx: Quantum computing uses quantum mechanics principles...
```

### Use Tools

```bash
You: /tools
✓ Tool mode enabled

You: Check if port 80 is open on localhost

Auryx: Let me scan that for you...
[Executes port scan]
Port 80 is open on localhost.
```

### Network Diagnostics

```bash
$ auryx-agent ping google.com
🏓 Ping google.com
PING google.com (142.250.185.46): 56 data bytes
64 bytes from 142.250.185.46: icmp_seq=0 ttl=117 time=12.3 ms
```

## 🔧 Configuration

### Config File Location

- Linux/Mac: `~/.config/auryx-agent/config.toml`
- Windows: `%APPDATA%\auryx-agent\config.toml`

### Available Options

```toml
[yellowfire]
api_key = "your_key"          # Required: YellowFire API key

[agent]
default_model = "gpt-4o-mini" # Default AI model
assistant_name = "Auryx"      # Assistant name
temperature = 0.7             # Response creativity (0.0-1.0)
system_prompt = ""            # Custom system prompt
```

## 💰 Pricing

All prices are in Credits (1 Credit = $1)

### Text Models (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| GPT-5 | $0.625 | $5.00 |
| GPT-5-mini | $0.125 | $1.00 |
| GPT-5-nano | $0.0025 | $0.20 |
| GPT-4o | $1.25 | $5.00 |
| GPT-4o-mini | $0.075 | $0.30 |
| Claude 4.5 Sonnet | $1.50 | $7.50 |
| Claude 3.5 Sonnet | $1.50 | $7.50 |
| Gemini 2.5 Pro | $0.625 | $5.00 |
| DeepSeek V3 | $0.135 | $0.55 |

[Full pricing table](https://github.com/Badim41/network_tools#pricing)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details

## 🙏 Credits

- Built on top of [network_tools](https://github.com/Badim41/network_tools) by Badim41
- Powered by [YellowFire API](https://yellowfire.ru)

## 📞 Support

- 🐛 [Report Issues](https://github.com/Sqrilizz/auryx-agent/issues)
- 💬 [Telegram Bot](https://t.me/GPT4_Unlimit_bot)

---

Made with ❤️ by sqrilizz
