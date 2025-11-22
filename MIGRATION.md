# Migration Guide: Multi-Provider Support

## Для существующих пользователей

Если вы уже используете Auryx Agent, вот что нужно знать:

### ✅ Обратная совместимость

Ваш текущий конфиг **продолжит работать**! Старый формат автоматически конвертируется:

**Старый формат** (все еще работает):
```toml
[yellowfire]
api_key = "your_key"

[agent]
default_model = "command-a"
```

**Новый формат** (рекомендуется):
```toml
provider = "yellowfire"
default_model = "command-a"

[api_keys]
yellowfire = "your_key"
```

### 🔄 Как обновить конфиг

1. Откройте `~/.config/auryx-agent/config.toml`

2. Замените старый формат на новый:

**Было:**
```toml
[yellowfire]
api_key = "your_key_here"

[agent]
default_model = "command-a"
assistant_name = "Auryx"
temperature = 0.7
```

**Стало:**
```toml
provider = "yellowfire"
default_model = "command-a"

[api_keys]
yellowfire = "your_key_here"

[ai]
assistant_name = "Auryx"
temperature = 0.7
```

3. Сохраните и перезапустите агента

### 🆕 Добавление новых провайдеров

Теперь вы можете добавить другие провайдеры:

```toml
provider = "openai"  # Переключитесь на OpenAI
default_model = "gpt-4o-mini"

[api_keys]
yellowfire = "your_yellowfire_key"
openai = "sk-..."  # Добавьте ключ OpenAI
anthropic = ""
google = ""
groq = ""
```

### 📦 Установка дополнительных провайдеров

```bash
# Установить все провайдеры
pip install openai anthropic google-generativeai groq

# Или только нужные
pip install openai  # для OpenAI
pip install anthropic  # для Anthropic
pip install google-generativeai  # для Google
pip install groq  # для Groq
```

### ⚠️ Deprecation Warning

При использовании старого `YellowFireClient` напрямую в коде вы увидите предупреждение:

```
DeprecationWarning: YellowFireClient is deprecated. 
Use auryx_agent.core.providers.YellowFireProvider instead.
```

Это не критично - код продолжит работать. Но рекомендуется обновиться:

**Старый код:**
```python
from auryx_agent.core.yellowfire_client import YellowFireClient
client = YellowFireClient(api_key="...", default_model="command-a")
```

**Новый код:**
```python
from auryx_agent.core.providers import ProviderFactory
client = ProviderFactory.create("yellowfire", api_key="...", model="command-a")
```

### 🎯 Что изменилось

1. **Добавлена поддержка 6 провайдеров**: YellowFire, OpenAI, Anthropic, Google, Groq, Vercel
2. **Новый формат конфига**: более гибкий и расширяемый
3. **Фабрика провайдеров**: единый интерфейс для всех API
4. **Опциональные зависимости**: устанавливайте только нужные библиотеки

### 📚 Дополнительная информация

- [PROVIDERS.md](PROVIDERS.md) - Полная документация по провайдерам
- [PROVIDERS.en.md](PROVIDERS.en.md) - English version
- [config.example.toml](config.example.toml) - Пример конфигурации

### 🐛 Проблемы?

Если что-то не работает:

1. Проверьте формат конфига
2. Убедитесь, что API ключ правильный
3. Установите нужные библиотеки (`pip install openai` и т.д.)
4. Создайте issue: https://github.com/Sqrilizz/auryx-agent/issues
