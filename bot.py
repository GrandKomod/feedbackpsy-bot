import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime

# =======================
# Чтение переменных окружения
# =======================
TOKEN = os.getenv("TOKEN")
ADMINS = os.getenv("ADMINS")

print("TOKEN:", TOKEN)
print("ADMINS:", ADMINS)

if not TOKEN or not ADMINS:
    print("⚠️ ВНИМАНИЕ: TOKEN или ADMINS не заданы! Бот может не работать.")

# Преобразуем строку "12345678,87654321" в список чисел
if ADMINS:
    try:
        ADMINS = [int(admin.strip()) for admin in ADMINS.split(",")]
    except ValueError:
        print("⚠️ Ошибка: ADMINS должно быть числами через запятую.")
        ADMINS = []

# =======================
# Инициализация бота
# =======================
if TOKEN:
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
else:
    bot = None
    dp = None

# =======================
# Команды
# =======================
if dp:
    # /start
    @dp.message(Command("start"))
    async def start_handler(message: Message):
        await message.answer(f"Добрый день, {message.from_user.first_name}, напишите ваш вопрос.")

    # /reply <user_id> <текст> — для админа
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

    # Обработка сообщений от пользователей
    @dp.message()
    async def user_message_handler(message: Message):
        # Ответ пользователю
        await message.reply("Ваше сообщение получено, скоро ответим!.")

        # Время сообщения
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Формируем текст уведомления для админа
        admin_text = (
            f"📩 Новое сообщение от пользователя:\n"
            f"ID: {message.from_user.id}\n"
            f"Имя: {message.from_user.full_name}\n"
            f"Username: @{message.from_user.username}\n"
            f"Время: {timestamp}\n\n"
            f"Сообщение:\n{message.text}"
        )

        # Кнопка "Ответить пользователю"
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="Ответить пользователю",
                switch_inline_query_current_chat=f"/reply {message.from_user.id} "
            )]
        ])

        # Пересылаем сообщение всем администраторам с кнопкой
        for admin_id in ADMINS:
            try:
                await bot.send_message(chat_id=admin_id, text=admin_text, reply_markup=keyboard)
            except Exception as e:
                print(f"Не удалось отправить администратору {admin_id}: {e}")

# =======================
# Запуск бота
# =======================
async def main():
    if bot and dp:
        print("Бот запускается...")
        try:
            await dp.start_polling(bot)
        finally:
            await bot.session.close()
    else:
        print("Бот не запущен из-за отсутствия TOKEN или ADMINS")

if __name__ == "__main__":
    asyncio.run(main())
