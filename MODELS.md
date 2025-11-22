# Доступные AI модели в Auryx Agent

## YellowFire (по умолчанию)

YellowFire предоставляет доступ ко всем моделям через единый API.

**Использование:** `auryx-agent --model <model_name>`

### GPT/OpenAI модели (16)
```bash
auryx-agent --model gpt-5-1-high
auryx-agent --model gpt-5-1
auryx-agent --model gpt-5-high
auryx-agent --model gpt-5
auryx-agent --model gpt-5-mini
auryx-agent --model gpt-oss
auryx-agent --model gpt-4-5
auryx-agent --model gpt-4-1
auryx-agent --model gpt-4-1-mini
auryx-agent --model gpt-4-1-nano
auryx-agent --model gpt-4o
auryx-agent --model chatgpt-4o
auryx-agent --model gpt-4o-mini
auryx-agent --model o4-mini
auryx-agent --model o3-high
auryx-agent --model o3-mini
auryx-agent --model o1
```

### Claude модели (13)
```bash
auryx-agent --model claude-4-5-sonnet
auryx-agent --model claude-4-5-sonnet-thinking
auryx-agent --model claude-4-1-opus
auryx-agent --model claude-4-opus
auryx-agent --model claude-4-sonnet
auryx-agent --model claude-4-1-opus-thinking
auryx-agent --model claude-4-opus-thinking
auryx-agent --model claude-4-sonnet-thinking
auryx-agent --model claude-3-7-sonnet-thinking
auryx-agent --model claude-3-5-sonnet
auryx-agent --model claude-3-opus
auryx-agent --model claude-3-sonnet
auryx-agent --model claude-3-haiku
```

### Gemini модели (4)
```bash
auryx-agent --model gemini-3-0-pro
auryx-agent --model gemini-2-5-pro
auryx-agent --model gemini-2.5-flash
auryx-agent --model gemini-2.0-flash-lite
```

### DeepSeek модели (4)
```bash
auryx-agent --model deepseek-r1
auryx-agent --model deepseek-v3
auryx-agent --model deepseek-v3.2
auryx-agent --model deepseek-v3.2-thinking
```

### Grok модели (2)
```bash
auryx-agent --model grok-4
auryx-agent --model grok-3
```

### Другие модели (8)
```bash
auryx-agent --model command-r-plus
auryx-agent --model command-a
auryx-agent --model command-a-vision
auryx-agent --model c4ai-aya-vision-32b
auryx-agent --model minimax-02
auryx-agent --model glm-4.6
auryx-agent --model kimi-k2-thinking
```

---

## Google AI (прямой API)

**Использование:** `auryx-agent --model google:<model_name>`

### Доступные модели (7)
```bash
auryx-agent --model google:gemini-2.0-flash-exp
auryx-agent --model google:gemini-1.5-pro-latest
auryx-agent --model google:gemini-1.5-pro
auryx-agent --model google:gemini-1.5-flash-latest
auryx-agent --model google:gemini-1.5-flash
auryx-agent --model google:gemini-1.0-pro-latest
auryx-agent --model google:gemini-1.0-pro
```

---

## Groq (прямой API - самый быстрый)

**Использование:** `auryx-agent --model groq:<model_name>`

⚠️ **Важно:** Используйте полные названия с префиксами!

### Llama модели (4)
```bash
auryx-agent --model groq:llama-3.3-70b-versatile
auryx-agent --model groq:llama-3.1-8b-instant
auryx-agent --model "groq:meta-llama/llama-4-maverick-17b-128e-instruct"
auryx-agent --model "groq:meta-llama/llama-4-scout-17b-16e-instruct"
```

### OpenAI OSS модели (2)
```bash
auryx-agent --model "groq:openai/gpt-oss-120b"
auryx-agent --model "groq:openai/gpt-oss-20b"
```

### Другие модели (5)
```bash
auryx-agent --model "groq:qwen/qwen3-32b"
auryx-agent --model "groq:moonshotai/kimi-k2-instruct"
auryx-agent --model "groq:groq/compound"
auryx-agent --model "groq:groq/compound-mini"
auryx-agent --model "groq:allam-2-7b"
```

---

## Команды для работы с моделями

### Просмотр моделей
```bash
# Все модели YellowFire
auryx-agent models list

# Модели конкретного провайдера
auryx-agent models provider yellowfire
auryx-agent models provider google
auryx-agent models provider groq

# Поиск моделей
auryx-agent models search gpt
auryx-agent models search claude
auryx-agent models search gemini
```

### В чате
```bash
# Переключение модели
/model gpt-5                                    # YellowFire
/model google:gemini-1.5-pro                    # Google AI
/model groq:llama-3.3-70b-versatile             # Groq
/model "groq:openai/gpt-oss-120b"               # Groq с префиксом

# Просмотр моделей
/models                    # Текущий провайдер
/models yellowfire         # YellowFire модели
/models google             # Google AI модели
/models groq               # Groq модели
```

---

## Рекомендации

### Для общих задач
- `command-a` (YellowFire) - быстрая и дешевая
- `gpt-4o-mini` (YellowFire) - хорошее качество
- `groq:llama-3.1-8b-instant` - самая быстрая

### Для сложных задач
- `gpt-5` (YellowFire) - самая мощная
- `claude-4-5-sonnet` (YellowFire) - отличное качество
- `groq:llama-3.3-70b-versatile` - быстрая и мощная

### Для кода
- `claude-4-5-sonnet` (YellowFire)
- `gpt-5` (YellowFire)
- `deepseek-v3` (YellowFire)

### Для русского языка
- `gpt-5` (YellowFire)
- `claude-4-5-sonnet` (YellowFire)
- `gemini-2-5-pro` (YellowFire)

---

## Примечания

1. **YellowFire** - доступ ко всем моделям, в 2 раза дешевле официальных API
2. **Google AI** - прямой доступ к официальному API Google
3. **Groq** - самый быстрый inference, но ограниченный выбор моделей
4. **Кавычки** - используйте кавычки для моделей с `/` в названии
5. **Префиксы** - для Groq обязательно указывайте полные названия с префиксами

---

**Обновлено:** 2025-11-22
