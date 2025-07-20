import os
import requests
from aiogram import Bot, Dispatcher, types
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
import asyncio
import feedparser
import aiohttp
from bs4 import BeautifulSoup

# Загружаем переменные из tgkAI/pass.env
load_dotenv("tgkAI/pass.env")

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID')
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
DEEPSEEK_MODEL = os.getenv('DEEPSEEK_MODEL')

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()

NEWS_KEYWORDS = [
    'электросамокат', 'электросамокаты', 'электровелосипед', 'электровелосипеды', 'электротранспорт',
    'электроскутер', 'электроскутеры', 'электробайк', 'электробайки', 'электромопед', 'электромопеды'
]

NEWS_SOURCES = [
    # Только РИА Новости
    'https://ria.ru/'
]

async def fetch_news():
    print('fetch_news() стартовал')
    news = []
    
    # Парсинг только РИА Новости
    try:
        print('Парсинг РИА Новости...')
        async with aiohttp.ClientSession() as session:
            # Пробуем несколько поисковых запросов
            search_queries = [
                'электросамокат',
                'электротранспорт',
                'электровелосипед',
                'электроскутер'
            ]
            
            for query in search_queries:
                try:
                    url = f'https://ria.ru/search/?query={query}'
                    async with session.get(url, timeout=aiohttp.ClientTimeout(total=8)) as resp:
                        if resp.status == 200:
                            html = await resp.text()
                            soup = BeautifulSoup(html, 'html.parser')
                            
                            # Расширенный поиск заголовков
                            selectors = [
                                'h2', 'h3', 'h4', 'h5',
                                '.list-item__title',
                                '.list-item__content-title',
                                '.search-item__title',
                                '.article__title',
                                '.news-item__title',
                                'a[href*="/202"]',  # Ссылки на новости с датой
                                '.b-list__item-title'
                            ]
                            
                            for selector in selectors:
                                articles = soup.select(selector)
                                for article in articles[:5]:  # Берём первые 5 статей
                                    title = article.get_text(strip=True)
                                    if title and len(title) > 10 and any(kw.lower() in title.lower() for kw in NEWS_KEYWORDS):
                                        news.append(title)
                                        print(f'Найдена новость: {title[:50]}...')
                            
                            if news:  # Если нашли новости, прекращаем поиск
                                break
                                
                except Exception as e:
                    print(f"Ошибка при поиске '{query}': {e}")
                    continue
            
            print(f'Найдено {len(news)} новостей на РИА Новости')
    except Exception as e:
        print(f"Ошибка при парсинге РИА Новости: {e}")
    
    # Если новостей не найдено, возвращаем fallback
    if not news:
        print('Новости не найдены, используем fallback')
        news = [
            "В Москве открыли новый сервис аренды электросамокатов.",
            "В Санкт-Петербурге увеличилось количество электровелосипедов на улицах."
        ]
    
    # Удаляем дубли и ограничиваем до 5 новостей
    news = list(dict.fromkeys(news))[:5]
    return news

async def generate_post(news_list):
    print('generate_post() стартовал')
    prompt = (
        "Напиши краткую новостную сводку для Telegram-канала об электротранспорте в России. "
        "Пиши от первого лица, естественно и просто. "
        "НЕ используй хэштеги, НЕ добавляй комментарии типа 'Вот вариант:' или 'Выбирайте'. "
        "НЕ используй технические элементы типа '**Заголовок:**'. "
        "НЕ предлагай варианты с 'Или чуть иначе:'. "
        "Просто напиши ОДНУ интересную сводку новостей с эмодзи. "
        "Новости:\n" + "\n".join(news_list)
    )
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": DEEPSEEK_MODEL,
        "messages": [
            {"role": "system", "content": "Ты — редактор Telegram-канала. Пиши только ОДНУ новостную сводку. НЕ добавляй варианты, комментарии, хэштеги или технические элементы. Только чистый текст одной сводки."},
            {"role": "user", "content": prompt}
        ]
    }
    print('Payload:', data)
    print('Headers:', headers)
    print('Отправляю запрос к DeepSeek...')
    try:
        timeout = aiohttp.ClientTimeout(total=60)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data
            ) as response:
                print('Ответ от DeepSeek получен')
                print('Статус:', response.status)
                text = await response.text()
                print('Тело ответа:', text)
                if response.status == 200:
                    result = await response.json()
                    content = result['choices'][0]['message']['content']
                    
                    # Постобработка: убираем варианты и лишние элементы
                    if "---" in content:
                        content = content.split("---")[0].strip()
                    if "Или чуть иначе:" in content:
                        content = content.split("Или чуть иначе:")[0].strip()
                    if "Вот вариант:" in content:
                        content = content.split("Вот вариант:")[1].strip() if "Вот вариант:" in content else content
                    
                    return content
                else:
                    print('Ошибка DeepSeek:', response.status, text)
                    return "Не удалось сгенерировать новость."
    except Exception as e:
        print('Ошибка при запросе к DeepSeek:', e)
        return "Ошибка при обращении к DeepSeek API."

async def publish_news():
    print('publish_news() стартовал')
    news_list = await fetch_news()
    print('Собранные новости:', news_list)
    post_text = await generate_post(news_list)
    print('Сгенерированный пост:', post_text)
    try:
        await bot.send_message(TELEGRAM_CHANNEL_ID, post_text)
        print('Пост успешно отправлен в канал.')
    except Exception as e:
        print('Ошибка при отправке поста:', e)

async def on_startup():
    scheduler = AsyncIOScheduler()
    # Отправка новостей каждый час
    scheduler.add_job(lambda: asyncio.create_task(publish_news()), 'cron', minute=0)
    scheduler.start()
    await publish_news()
    print("Бот запущен, тестовая новость отправлена и расписание установлено.")

async def main():
    await on_startup()
    while True:
        await asyncio.sleep(3600)  # Держим event loop живым

if __name__ == "__main__":
    asyncio.run(main()) 