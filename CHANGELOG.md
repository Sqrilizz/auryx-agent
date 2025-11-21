# Changelog

All notable changes to Auryx Agent will be documented in this file.

## [0.2.0] - 2024-11-21

### 🎉 Major Features Added

#### 💻 Code Tools
- **Code Generation**: Generate code from natural language descriptions
- **Code Review**: Analyze code for bugs, improvements, and best practices
- **Refactoring**: Automated code refactoring suggestions
- **Bug Detection**: Find potential bugs in code files
- **Documentation Generation**: Auto-generate documentation from code
- **Git Integration**: View git status and diffs
- **Project Templates**: Quick scaffolding for Python, Flask, FastAPI, CLI tools

#### 🌐 Web Access
- **Web Search**: Search the internet using DuckDuckGo (no API key needed)
- **Page Fetching**: Download and analyze web pages
- **File Downloads**: Download files from URLs
- **Website Checking**: Check if websites are accessible
- **Weather Information**: Get weather for any location via wttr.in
- **Link Extraction**: Extract all links from web pages
- **WHOIS Lookup**: Domain information lookup

#### 🧠 Long-term Memory System
- **Persistent Memory**: Agent remembers information across sessions
- **User Preferences**: Automatically learns and remembers your preferences
- **Context Retention**: Maintains context about projects and conversations
- **Memory Search**: Search through stored memories
- **Categories**: Organize memories by type (preference, fact, context, skill)
- **Importance Ranking**: Prioritize important memories
- **Memory Commands**: `/memory`, `/remember`, `/recall`, `/forget`

#### 🖥️ Advanced System Control
- **Process Management**: List, monitor, and terminate processes
- **Resource Monitoring**: Track CPU, RAM, disk usage in real-time
- **Network Connections**: View active network connections
- **Battery Information**: Check battery status (if available)
- **File Search**: Find files by pattern recursively
- **Archive Operations**: Create and extract zip, tar, tar.gz archives
- **System Monitoring**: Monitor system resources over time

### 🎨 UI Improvements
- **Compact Startup**: Cleaner, more minimal startup screen
- **New Logo**: Redesigned ASCII art logo
- **Tool Badges**: Visual indicators for different tool types
- **Progress Bars**: Visual feedback for long operations
- **Boxes**: Beautiful bordered boxes for important info
- **Better Colors**: Enhanced color scheme with more visual hierarchy

### 📚 Documentation
- **FEATURES_v0.2.md**: Comprehensive guide to new features
- **README.ru.md**: Russian version of README
- **CHANGELOG.md**: This file
- **Updated README.md**: Added v0.2.0 features and examples

### 🔧 Technical Changes
- Added `psutil` dependency for system monitoring
- New modules:
  - `auryx_agent/tools/code_tools.py`
  - `auryx_agent/tools/web_tools.py`
  - `auryx_agent/tools/advanced_computer_tools.py`
  - `auryx_agent/core/memory.py`
- Enhanced `Agent` class with 31+ tools
- Improved `Formatter` class with new visual elements
- Updated CLI with memory commands

### 📊 Statistics
- **31+ Tools** available (up from 9)
- **4 New Tool Categories**: Code, Web, Advanced System, Memory
- **8 New Commands**: Memory-related commands
- **3 New Modules**: Major feature additions

## [0.1.0] - 2024-11-20

### Initial Release
- Multi-model AI chat (50+ models)
- Interactive chat with context
- System tools integration
- Network diagnostics (ping, DNS, ports, traceroute)
- Session management (save/load)
- Command execution
- Basic file operations

---

## Roadmap

See [ROADMAP.md](ROADMAP.md) for planned features:
- v0.3.0: Image & music generation
- v0.4.0: Automation & workflows
- v0.5.0: Analytics & monitoring
- v1.0.0: Production ready

---

**Author: sqrilizz**  
**Note**: This project follows [Semantic Versioning](https://semver.org/).
