# 🔥 Auryx Agent

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.2.0-orange.svg)](ROADMAP.md)
[![GitHub stars](https://img.shields.io/github/stars/Sqrilizz/auryx-agent.svg)](https://github.com/Sqrilizz/auryx-agent/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/Sqrilizz/auryx-agent.svg)](https://github.com/Sqrilizz/auryx-agent/issues)

> 🚀 Advanced AI agent with memory, web access, and code generation capabilities

Auryx Agent is a powerful command-line AI assistant that brings advanced capabilities directly to your terminal. Chat with 50+ AI models, generate and review code, search the web, manage your system, and let it remember your preferences - all from one place.

## 🎉 What's New in v0.2.0

- 💻 **Code Generation & Review** - Create, analyze, and refactor code
- 🌐 **Web Access** - Search the internet, download files, check weather
- 🧠 **Long-term Memory** - Agent remembers your preferences and context
- 🖥️ **Advanced System Control** - Process management, resource monitoring
- 🎨 **Enhanced UI** - Beautiful output with colors and icons

[📖 Read Full v0.2.0 Features](FEATURES_v0.2.md) | [🇷🇺 Русская версия](README.ru.md)

## ✨ Features

### 🤖 Multi-Model AI Chat
- **50+ AI Models**: GPT-5, Claude 4, Gemini 3.0, DeepSeek, Grok, and more
- **Interactive Chat**: Natural conversation with context preservation
- **Tool Mode**: AI can execute commands and interact with your system
- **Session Management**: Save and load conversations

### 💻 Code Capabilities (NEW!)
- **Code Generation**: Create code in any language from descriptions
- **Code Review**: Analyze code for bugs and improvements
- **Refactoring**: Automated code refactoring
- **Project Templates**: Quick scaffolding for Flask, FastAPI, CLI tools
- **Git Integration**: Status, diff, and version control

### 🌐 Web Access (NEW!)
- **Web Search**: Search the internet using DuckDuckGo
- **Page Fetching**: Download and analyze web pages
- **File Downloads**: Download files from URLs
- **Weather Info**: Get weather for any location
- **Link Extraction**: Extract all links from web pages

### 🧠 Long-term Memory (NEW!)
- **Remembers Preferences**: Learns your coding style and preferences
- **Context Retention**: Maintains context across sessions
- **Smart Recall**: Search through stored memories
- **Auto-learning**: Automatically remembers important information

### 🖥️ Advanced System Control (NEW!)
- **Process Management**: List, monitor, and kill processes
- **Resource Monitoring**: CPU, RAM, disk usage tracking
- **Network Connections**: View active connections
- **File Operations**: Search, compress, extract archives
- **System Monitoring**: Real-time resource monitoring

### 🛠️ Network Tools
- **Diagnostics**: Ping, DNS lookup, port scanning, traceroute
- **System Information**: Detailed system info
- **Command Execution**: Run shell commands directly

### 💰 Cost-Effective
- **2x Cheaper** than official APIs for text models
- **Free $1 Balance** to get started
- **31+ Tools** available for automation

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
/memory                   # Show memory stats (NEW!)
/remember <text>          # Add to memory (NEW!)
/recall <query>           # Search memory (NEW!)
/forget                   # Clear memory (NEW!)
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
- Command R+,
- Minimax-01/02, Kimi K2


## 💡 Examples

### Code Generation

```bash
You: Create a FastAPI app with user endpoints

Auryx: 💻 Creating FastAPI application...
✓ Created main.py
✓ Created requirements.txt
✓ Added endpoints: GET /users, POST /users
```

### Web Search

```bash
You: Search for Python 3.12 new features

Auryx: 🌐 Searching the web...
Found 5 results:
1. Python 3.12 Release Notes - New features include...
2. What's New in Python 3.12 - Performance improvements...
```

### Memory System

```bash
You: Remember that I prefer Python and FastAPI

Auryx: ✓ Remembered your preferences

[Later...]

You: Create an API for a blog

Auryx: Creating FastAPI application (as you prefer)...
```

### System Monitoring

```bash
You: Show system resources

Auryx: 
🖥️ System Resources:
  CPU: 45% (8 cores)
  RAM: 8.2 GB / 16 GB (51%)
  Disk: 120 GB / 500 GB (24%)
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

**Author: sqrilizz**  
Made with ❤️ for developers
