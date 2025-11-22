# Multi-Provider Support

Auryx Agent now supports multiple AI providers! Use models from different companies.

## Supported Providers

1. **YellowFire** (default) - 50+ models, 2x cheaper, free $1
2. **OpenAI** - GPT-4o, GPT-4o-mini, o1
3. **Anthropic** - Claude 3.5 Sonnet, Claude 3 Opus
4. **Google** - Gemini 2.0 Flash, Gemini 1.5 Pro
5. **Groq** - Llama 3.3, Mixtral (fastest inference)
6. **Vercel** - Unified interface for multiple models

## Quick Start

### 1. Install provider libraries (optional)

```bash
# Install all providers
pip install openai anthropic google-generativeai groq

# Or install specific ones
pip install openai  # for OpenAI/Vercel
pip install anthropic  # for Anthropic
pip install google-generativeai  # for Google
pip install groq  # for Groq
```

### 2. Configure

Edit `~/.config/auryx-agent/config.toml`:

```toml
# Choose provider
provider = "yellowfire"  # or: openai, anthropic, google, groq, vercel

# Default model
default_model = "command-a"

# API Keys
[api_keys]
yellowfire = "your_key"  # Get: https://t.me/GPT4_Unlimit_bot?start=api
openai = ""              # Get: https://platform.openai.com/api-keys
anthropic = ""           # Get: https://console.anthropic.com/
google = ""              # Get: https://makersuite.google.com/app/apikey
groq = ""                # Get: https://console.groq.com/keys
vercel = ""              # Get: https://sdk.vercel.ai/
```

### 3. Run

```bash
auryx-agent chat
```

## Provider Comparison

| Provider | Price | Speed | Quality | Free Tier |
|----------|-------|-------|---------|-----------|
| YellowFire | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | $1 |
| OpenAI | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | No |
| Anthropic | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | No |
| Google | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | Yes |
| Groq | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Yes |
| Vercel | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Varies |

## Recommendations

- **Getting started**: YellowFire (free $1, 50+ models)
- **Production**: OpenAI or Anthropic (stability)
- **Experiments**: Google or Groq (free)
- **Speed**: Groq (fastest)
- **Coding**: Anthropic Claude (best for code)

See [PROVIDERS.md](PROVIDERS.md) for detailed documentation (Russian).
