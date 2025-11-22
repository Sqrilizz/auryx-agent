# Multi-Provider Support

Auryx Agent теперь поддерживает несколько AI провайдеров! Вы можете использовать модели от разных компаний.

## Поддерживаемые провайдеры

### 1. YellowFire (по умолчанию)
- **Преимущества**: Дешевле официальных API в 2 раза, бесплатный $1 баланс
- **Модели**: GPT-5, GPT-4, Claude 4, Gemini 3.0, DeepSeek, Grok и другие (50+ моделей)
- **Получить ключ**: https://t.me/GPT4_Unlimit_bot?start=api

```toml
provider = "yellowfire"
default_model = "command-a"  # или gpt-5, claude-4-5-sonnet, etc.

[api_keys]
yellowfire = "your_key_here"
```

### 2. OpenAI
- **Преимущества**: Официальный API, стабильность
- **Модели**: GPT-4o, GPT-4o-mini, GPT-4-turbo, o1-preview, o1-mini
- **Получить ключ**: https://platform.openai.com/api-keys

```toml
provider = "openai"
default_model = "gpt-4o-mini"

[api_keys]
openai = "sk-..."
```

**Установка**:
```bash
pip install openai
# или
poetry add openai
```

### 3. Anthropic (Claude)
- **Преимущества**: Лучшие модели для кода и анализа
- **Модели**: Claude 3.5 Sonnet, Claude 3.5 Haiku, Claude 3 Opus
- **Получить ключ**: https://console.anthropic.com/

```toml
provider = "anthropic"
default_model = "claude-3-5-sonnet-20241022"

[api_keys]
anthropic = "sk-ant-..."
```

**Установка**:
```bash
pip install anthropic
# или
poetry add anthropic
```

### 4. Google (Gemini)
- **Преимущества**: Бесплатный tier, большой контекст
- **Модели**: Gemini 2.0 Flash, Gemini 1.5 Pro, Gemini 1.5 Flash
- **Получить ключ**: https://makersuite.google.com/app/apikey

```toml
provider = "google"
default_model = "gemini-1.5-flash"

[api_keys]
google = "AIza..."
```

**Установка**:
```bash
pip install google-generativeai
# или
poetry add google-generativeai
```

### 5. Groq
- **Преимущества**: Самый быстрый inference, бесплатный tier
- **Модели**: Llama 3.3 70B, Llama 3.1, Mixtral, Gemma2
- **Получить ключ**: https://console.groq.com/keys

```toml
provider = "groq"
default_model = "llama-3.3-70b-versatile"

[api_keys]
groq = "gsk_..."
```

**Установка**:
```bash
pip install groq
# или
poetry add groq
```

## 🚀 Результаты тестов скорости

Реальные тесты на простых запросах:

```
🏆 Winner: GROQ (llama-3.3-70b-versatile)
   Average response time: 0.12s
   23.4x faster than Google Gemini

Rank   Provider        Model                          Avg Time    
------------------------------------------------------------
🥇 1   groq            llama-3.3-70b-versatile        0.12s
🥈 2   google          gemini-2.5-flash               2.83s
```

**Вывод**: Groq - самый быстрый провайдер с огромным отрывом!

## Быстрая установка

### Установить все провайдеры сразу:
```bash
pip install openai anthropic google-generativeai groq
# или
poetry install --extras all-providers
```

### Установить конкретный провайдер:
```bash
# OpenAI
poetry install --extras openai

# Anthropic
poetry install --extras anthropic

# Google
poetry install --extras google

# Groq
poetry install --extras groq
```

## Конфигурация

Отредактируйте `~/.config/auryx-agent/config.toml`:

```toml
# Выберите провайдера
provider = "yellowfire"  # или openai, anthropic, google, groq, vercel

# Модель по умолчанию
default_model = "command-a"

# API ключи (заполните только те, которые используете)
[api_keys]
yellowfire = "your_yellowfire_key"
openai = ""
anthropic = ""
google = ""
groq = ""
```

## Использование

После настройки просто запустите:

```bash
auryx-agent chat
```

Агент автоматически использует выбранного провайдера!

### Переключение провайдера в runtime

Вы можете переключать провайдеров, изменив конфиг и перезапустив агента.

## Сравнение провайдеров

| Провайдер | Цена | Скорость | Качество | Бесплатный tier | Реальная скорость* |
|-----------|------|----------|----------|-----------------|-------------------|
| YellowFire | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | $1 | ~2s |
| OpenAI | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Нет | ~1-2s |
| Anthropic | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Нет | ~1-2s |
| Google | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | Да (щедрый) | ~2.8s |
| Groq | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Да | **~0.12s** 🚀 |

*Реальные тесты на простых запросах. Groq в **23x быстрее** Google!

## Рекомендации

- **Для начала**: YellowFire (бесплатный $1, много моделей)
- **Для продакшена**: OpenAI или Anthropic (стабильность)
- **Для экспериментов**: Google или Groq (бесплатные)
- **Для скорости**: Groq (самый быстрый)
- **Для кода**: Anthropic Claude (лучший для программирования)

## Troubleshooting

### Ошибка: "API key not configured"
Убедитесь, что добавили API ключ в `~/.config/auryx-agent/config.toml`

### Ошибка: "Failed to initialize provider"
Установите необходимую библиотеку:
```bash
pip install openai  # для OpenAI/Vercel
pip install anthropic  # для Anthropic
pip install google-generativeai  # для Google
pip install groq  # для Groq
```

### Модель не найдена
Проверьте список доступных моделей для вашего провайдера в этом документе.

## Примеры использования

### YellowFire (дешево, много моделей)
```toml
provider = "yellowfire"
default_model = "gpt-5"  # или claude-4-5-sonnet, deepseek-v3
```

### OpenAI (стабильно)
```toml
provider = "openai"
default_model = "gpt-4o"
```

### Anthropic (для кода)
```toml
provider = "anthropic"
default_model = "claude-3-5-sonnet-20241022"
```

### Google (бесплатно)
```toml
provider = "google"
default_model = "gemini-1.5-flash"
```

### Groq (быстро)
```toml
provider = "groq"
default_model = "llama-3.3-70b-versatile"
```
