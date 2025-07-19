# Telegram AI News Bot

🤖 Автоматический Telegram-бот для публикации новостей об электротранспорте в России с использованием ИИ.

## 🚀 Возможности

- **Автоматический парсинг новостей** с сайта [РИА Новости](https://ria.ru/)
- **Генерация постов через DeepSeek AI** с естественным стилем
- **Планировщик публикаций** (2 раза в день: 9:00 и 18:00)
- **Systemd сервис** для автозапуска
- **Асинхронная обработка** с таймаутами

## 📋 Требования

- Python 3.8+
- Telegram Bot Token
- DeepSeek API Key (через OpenRouter)
- Telegram Channel ID

## 🛠️ Установка

1. **Клонируйте репозиторий:**
```bash
git clone https://github.com/your-username/telegram-ai-news-bot.git
cd telegram-ai-news-bot
```

2. **Установите зависимости:**
```bash
pip install -r requirements.txt
```

3. **Настройте конфигурацию:**
```bash
cp env.example pass.env
# Отредактируйте pass.env и добавьте свои данные
```

4. **Заполните pass.env:**
```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHANNEL_ID=your_channel_id_here
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_MODEL=deepseek/deepseek-r1-0528-qwen3-8b:free
```

## 🔧 Настройка

### Telegram Bot
1. Создайте бота через [@BotFather](https://t.me/BotFather)
2. Получите токен бота
3. Добавьте бота в канал как администратора
4. Получите ID канала (можно через @userinfobot)

### DeepSeek API
1. Зарегистрируйтесь на [OpenRouter](https://openrouter.ai/)
2. Получите API ключ
3. Убедитесь, что модель `deepseek/deepseek-r1-0528-qwen3-8b:free` доступна

## 🚀 Запуск

### Ручной запуск
```bash
python3 bot.py
```

### Через systemd (рекомендуется)
```bash
# Установите сервис
sudo cp tgkAI_bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable tgkAI_bot.service
sudo systemctl start tgkAI_bot.service

# Проверьте статус
sudo systemctl status tgkAI_bot.service
```

## 📊 Управление сервисом

```bash
# Статус
sudo systemctl status tgkAI_bot.service

# Остановить
sudo systemctl stop tgkAI_bot.service

# Перезапустить
sudo systemctl restart tgkAI_bot.service

# Логи
sudo journalctl -u tgkAI_bot.service -f
```

## 🔍 Поиск новостей

Бот автоматически ищет новости по ключевым словам:
- электросамокат
- электровелосипед
- электротранспорт
- электроскутер
- электробайк

## 📝 Генерация постов

ИИ создает естественные посты с:
- Анализом новостей
- Эмодзи
- Человеческим стилем
- Без технических элементов

## 🛡️ Безопасность

- Все конфиденциальные данные хранятся в `pass.env`
- Файл `pass.env` исключен из Git через `.gitignore`
- Используются асинхронные запросы с таймаутами

## 📁 Структура проекта

```
tgkAI/
├── bot.py              # Основной файл бота
├── requirements.txt    # Зависимости Python
├── env.example         # Пример конфигурации
├── .gitignore         # Исключения Git
├── README.md          # Документация
└── tgkAI_bot.service  # Systemd сервис
```

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции
3. Внесите изменения
4. Создайте Pull Request

## 📄 Лицензия

MIT License

## ⚠️ Отказ от ответственности

Этот бот предназначен только для образовательных целей. Убедитесь, что вы соблюдаете условия использования API и правила Telegram.

## 🔗 Ссылки

- [РИА Новости](https://ria.ru/)
- [OpenRouter](https://openrouter.ai/)
- [Telegram Bot API](https://core.telegram.org/bots/api) 