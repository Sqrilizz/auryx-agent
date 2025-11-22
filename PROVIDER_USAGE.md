# Использование провайдеров в Auryx Agent

## Обзор

Auryx Agent поддерживает несколько AI провайдеров:

- **YellowFire** (по умолчанию) - доступ ко всем моделям через единый API
- **OpenAI** - прямое использование OpenAI API
- **Anthropic** - прямое использование Anthropic API
- **Google AI** - прямое использование Google AI API
- **Groq** - прямое использование Groq API
- **Vercel AI** - использование Vercel AI SDK

## Форматы указания моделей

### YellowFire (по умолчанию)

Модели YellowFire уже прописаны в коде и доступны напрямую:

```bash
# Просто указываете имя модели
auryx-agent --model gpt-4o-mini
auryx-agent --model claude-3-5-sonnet
auryx-agent --model gemini-2-5-pro
auryx-agent --model deepseek-v3
```

**Преимущества YellowFire:**
- ✅ Доступ ко всем моделям через один API ключ
- ✅ Дешевле официальных API (в 2 раза)
- ✅ Бесплатный $1 баланс для старта
- ✅ 50+ моделей от разных провайдеров

### Другие провайдеры

Для использования других провайдеров используйте формат `provider:model`:

```bash
# OpenAI API напрямую
auryx-agent --model openai:gpt-4o
auryx-agent --model openai:gpt-4o-mini

# Anthropic API напрямую
auryx-agent --model anthropic:claude-3-5-sonnet-20241022
auryx-agent --model anthropic:claude-3-opus-20240229

# Google AI API напрямую
auryx-agent --model google:gemini-1.5-pro
auryx-agent --model google:gemini-2.0-flash-exp

# Groq API напрямую
auryx-agent --model groq:llama-3.3-70b-versatile
auryx-agent --model groq:mixtral-8x7b-32768
```

## Конфигурация API ключей

Добавьте API ключи в `~/.config/auryx-agent/config.toml`:

```toml
[api_keys]
# YellowFire - получить: https://t.me/GPT4_Unlimit_bot?start=api
yellowfire = "your_yellowfire_key"

# OpenAI - получить: https://platform.openai.com/api-keys
openai = "sk-..."

# Anthropic - получить: https://console.anthropic.com/
anthropic = "sk-ant-..."

# Google AI - получить: https://makersuite.google.com/app/apikey
google = "AIza..."

# Groq - получить: https://console.groq.com/keys
groq = "gsk_..."
```

## Примеры использования

### В командной строке

```bash
# YellowFire (по умолчанию)
auryx-agent --model gpt-4o-mini

# OpenAI напрямую
auryx-agent --model openai:gpt-4o

# Anthropic напрямую
auryx-agent --model anthropic:claude-3-5-sonnet-20241022
```

### В чате

```bash
# Запустить чат
auryx-agent chat

# Переключить модель (YellowFire)
/model gpt-4o-mini
/model claude-3-5-sonnet

# Переключить на другой провайдер (пока не реализовано в чате)
/model openai:gpt-4o
# ⚠️  Provider switching not yet implemented in chat mode
```

## Список доступных моделей

### YellowFire модели

Посмотреть все доступные модели:

```bash
auryx-agent models list
```

Поиск моделей:

```bash
auryx-agent models search gpt
auryx-agent models search claude
auryx-agent models search gemini
```

### Модели других провайдеров

#### OpenAI
- gpt-4o, gpt-4o-mini
- gpt-4-turbo, gpt-4
- gpt-3.5-turbo
- o1, o1-mini, o1-preview

#### Anthropic
- claude-3-5-sonnet-20241022
- claude-3-opus-20240229
- claude-3-sonnet-20240229
- claude-3-haiku-20240307

#### Google AI
- gemini-2.0-flash-exp
- gemini-1.5-pro
- gemini-1.5-flash
- gemini-1.0-pro

#### Groq
- llama-3.3-70b-versatile
- llama-3.1-70b-versatile
- mixtral-8x7b-32768
- gemma2-9b-it

## Когда использовать какой провайдер?

### Используйте YellowFire если:
- ✅ Хотите доступ ко всем моделям через один API
- ✅ Нужна экономия (в 2 раза дешевле)
- ✅ Тестируете разные модели
- ✅ Не хотите настраивать много API ключей

### Используйте прямые API если:
- ✅ Нужны самые новые модели (могут быть недоступны в YellowFire)
- ✅ Требуется максимальная надежность
- ✅ Используете корпоративные аккаунты
- ✅ Нужны специфичные фичи провайдера

## Стоимость

### YellowFire (за 1M токенов)
- GPT-5: $0.625 / $5.00
- GPT-4o: $1.25 / $5.00
- Claude 3.5 Sonnet: $1.50 / $7.50
- Gemini 2.5 Pro: $0.625 / $5.00
- DeepSeek V3: $0.135 / $0.55

### Официальные API
Обычно в 2 раза дороже YellowFire.

## Проверка баланса

```bash
# YellowFire баланс
auryx-agent balance

# История использования
auryx-agent usage
```

## Поддержка

- 🐛 [Сообщить о проблеме](https://github.com/Sqrilizz/auryx-agent/issues)
- 💬 [Telegram бот YellowFire](https://t.me/GPT4_Unlimit_bot)
- 📖 [Документация](https://github.com/Sqrilizz/auryx-agent)
