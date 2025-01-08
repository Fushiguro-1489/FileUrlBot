# main.py
import asyncio
import logging
from aiogram import Bot, Dispatcher

from config import TOKEN
from database.db import init_db
from handlers import handlers

logging.basicConfig(level=logging.INFO)

bot = Bot(TOKEN)
dp = Dispatcher()

def main():
    # Регистрируем обработчики команд
    dp.include_router(handlers.router)

    init_db()

    # Запускаем бота
    asyncio.run(start_bot())


async def start_bot():
    """
    Главная функция
    """
    await bot.delete_webhook(drop_pending_updates=True)

    try:
        await dp.start_polling(bot)
    except (KeyboardInterrupt, SystemExit):
        await dp.stop_polling()

if __name__ == "__main__":
    main()
