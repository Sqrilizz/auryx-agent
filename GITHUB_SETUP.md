# GitHub Setup Instructions

## 1. Create Repository on GitHub

1. Go to https://github.com/new
2. Repository name: `auryx-agent`
3. Description: `🔥 AI-powered CLI agent with 50+ models - GPT-5, Claude 4, Gemini & more`
4. Make it Public
5. **Don't** initialize with README (we already have one)
6. Click "Create repository"

## 2. Push to GitHub

```bash
# Add remote
git remote add origin https://github.com/YOUR_USERNAME/auryx-agent.git

# Push
git push -u origin main
```

## 3. Add Topics (Tags)

On GitHub repository page, click "⚙️ Settings" → "Topics" and add:
- `ai`
- `cli`
- `chatgpt`
- `gpt-5`
- `claude`
- `gemini`
- `python`
- `terminal`
- `yellowfire`
- `network-tools`

## 4. Create Release

1. Go to "Releases" → "Create a new release"
2. Tag: `v0.1.0`
3. Title: `🔥 Auryx Agent v0.1.0 - Initial Release`
4. Description:
```markdown
## 🎉 First Release!

Auryx Agent brings AI superpowers to your terminal!

### ✨ Features
- 🤖 50+ AI models (GPT-5, Claude 4, Gemini, DeepSeek, Grok)
- 💬 Interactive chat with context
- 🛠️ System tools integration
- 🌐 Network diagnostics
- 💾 Session management
- 💰 2x cheaper than official APIs

### 📦 Installation
\`\`\`bash
pip install git+https://github.com/YOUR_USERNAME/auryx-agent.git
\`\`\`

### 🚀 Quick Start
\`\`\`bash
auryx-agent chat
\`\`\`

Get your free API key: https://t.me/GPT4_Unlimit_bot?start=api
```

## 5. Add Screenshots

Create a `screenshots` folder and add:
- `chat.png` - Chat interface
- `models.png` - Model list
- `tools.png` - Tool mode in action
- `network.png` - Network diagnostics

Update README.md to include:
```markdown
## 📸 Screenshots

### Interactive Chat
![Chat Interface](screenshots/chat.png)

### Multiple Models
![Model Selection](screenshots/models.png)

### System Tools
![Tool Mode](screenshots/tools.png)
```

## 6. Enable GitHub Pages (Optional)

1. Settings → Pages
2. Source: Deploy from branch
3. Branch: main, folder: / (root)
4. Save

## 7. Add Badges to README

Add at the top of README.md:
```markdown
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/YOUR_USERNAME/auryx-agent.svg)](https://github.com/YOUR_USERNAME/auryx-agent/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/YOUR_USERNAME/auryx-agent.svg)](https://github.com/YOUR_USERNAME/auryx-agent/issues)
```

## 8. Update README Links

Replace `YOUR_USERNAME` with your actual GitHub username in:
- Installation command
- Issue links
- Repository links

## Done! 🎉

Your project is now ready for the world!
