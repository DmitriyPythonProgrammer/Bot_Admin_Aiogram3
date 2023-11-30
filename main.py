import logging
import asyncio
from aiogram import Bot
import config
from aiogram import Router
from handlers import dp
import database
router = Router()
logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.BOT_TOKEN, parse_mode='HTML')
async def main():
    dp.include_router(router)
    await database.initialize()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=["message", "inline_query", "chat_member", "callback_query", "update_id", "my_chat_member"])