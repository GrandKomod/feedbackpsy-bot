import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message

# =======================
# Чтение переменных окружения
# =======================
TOKEN = os.getenv("TOKEN")
ADMINS = os.getenv("ADMINS")

# =======================
# Проверка переменных
# =======================
print("Значение TOKEN:", TOKEN)
print("Значение ADMINS:", ADMINS)

if not TOKEN:
    raise RuntimeError("Ошибка: переменная TOKEN не задана! Добавьте её в Environment Variables на Railway.")
if not ADMINS:
    raise RuntimeError("Ошибка: переменная ADMINS не задана! Добавьте её в Environment Variables на Railway.")

# Преобразуем строку "12345678,87654321" в список чисел
try:
    ADMINS = [int(admin_id.strip()) for admin_id in ADMINS.split(",")]
except ValueError:
    raise RuntimeError("Ошибка: ADMINS должно быть строкой чисел через запятую, например: 12345678,87654321")

# =======================
# Инициализация бота
# =======================
bot = Bot(token=TOKEN)
dp = Dispatcher()

# =======================
# Стартовое сообщение
# =======================
@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(f"Привет, {message.from_user.first_name}! Бот работает.")

# =======================
# Команда админа /reply <user_id> <текст>
# =======================
@dp.message(Command("reply"))
async def reply_handler(message: Message):
    if message.from_user.id not in ADMINS:
        await message.reply("❌ У вас нет прав для этой команды.")
        return

    try:
        parts = message.text.split(maxsplit=2)
        user_id = int(parts[1])
        text = parts[2]
    except (IndexError, ValueError):
        await message.reply("Использование: /reply <user_id> <текст>")
        return

    try:
        await bot.send_message(chat_id=user_id, text=text)
        await message.reply(f"✅ Сообщение отправлено пользователю {user_id}")
    except Exception as e:
        await message.reply(f"❌ Не удалось отправить сообщение: {e}")

# =======================
# Ответ всем остальным пользователям
# =======================
@dp.message()
async def echo_user(message: Message):
    await message.reply("Ваше сообщение получено, админ скоро ответит.")

# =======================
# Запуск бота
# =======================
async def main():
    print("Бот запускается...")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
