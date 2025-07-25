import os
import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from handlers import router
from database.models import Base
from database.db import engine

load_dotenv()

BOT = os.getenv("TOKEN")

async def main():
    Base.metadata.create_all(engine)
    bot = Bot(token=BOT, parse_mode=None)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())