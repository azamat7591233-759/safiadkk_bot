import asyncio import logging from aiogram import Bot, Dispatcher, types from aiogram.filters import Command
TOKEN = "8198750723:AAGRA1RqTnpsSYaa0gAsU7FZcvGaMhRJ6rk"
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN) dp = Dispatcher()
@dp.message(Command("start")) async def start_handler(message: types.Message): await message.answer("Salom! Bot muvaffaqiyatli ishga tushdi va ishlayapti! 🚀")
async def main(): await bot.delete_webhook(drop_pending_updates=True) await dp.start_polling(bot)
if name == "main": asyncio.run(main())
