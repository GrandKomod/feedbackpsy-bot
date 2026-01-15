import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import F
import asyncio

# =======================
# Получаем переменные окружения
# =======================
TOKEN = os.getenv("TOKEN")
ADMINS = os.getenv("ADMINS")

if not TOKEN:
    raise RuntimeError("Ошибка: переменная TOKEN не задана!")
if not ADMINS:
    raise RuntimeError("Ошибка: переменная ADMINS не задана!")

# Преобразуем строку "12345678,87654321" в список чисел
ADMINS = [int(admin_id.strip()) for admin_id in ADMINS.split(",")]

# =======================
# Инициализация бота
# =======================
bot = Bot(token=TOKEN)
dp = Dispatcher()

# =======================
# Простой стартовый хэндлер
# =======================
@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(f"Привет, {message.from_user.first_name}! Бот работает.")

# =======================
# Хэндлер только для админов
# =======================
@dp.message(F.from_user.id.in_(ADMINS))
async def admin_only(message: Message):
    await message.answer("Вы админ и можете использовать все команды!")

# =======================
# Хэндлер для всех остальных
# =======================
@dp.message()
async def everyone_else(message: Message):
    await message.answer("Эта команда доступна всем пользователям.")

# =======================
# Запуск бота
# =======================
async def main():
    try:
        print("Бот запускается...")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
