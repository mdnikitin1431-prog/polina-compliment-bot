import asyncio
import random
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

TOKEN = "8601587831:AAGOxwTYLq_gJ7oHOzrDR-001TXubjeFPWc"
STICKER_PACK_NAME = "myaumurksksks_by_TgEmojiBot"

# Render автоматически выдает URL твоего приложения в переменную окружения RENDER_EXTERNAL_URL
RENDER_URL = os.getenv("RENDER_EXTERNAL_URL")
WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = f"{RENDER_URL}{WEBHOOK_PATH}"

# Настройки порта для сервера
PORT = int(os.getenv("PORT", 8080))

COMPLIMENTS = [
    "Полина, у тебя потрясающее чувство юмора! С тобой всегда весело и легко. ✨",
    "Полина, твоя улыбка способна поднять настроение в любой, даже самый хмурый день! 😊",
    "Ты очень целеустремленная и умная. Уверен, у тебя всё получится! 💪",
    "Полина, с тобой безумно интересно общаться, ты классный собеседник. 📚",
    "У тебя очень классный стиль и эстетика! 🌟",
    "Полина, ты умеешь вдохновлять и заряжать позитивом. Спасибо за твою классную энергию! ⚡",
    "Ты невероятно искренний и надежный человек. Это очень круто! 🙌",
    "Полина, пусть сегодняшний день принесет тебе кучу крутых моментов и поводов для улыбки! ☀️"
]

bot = Bot(token=TOKEN)
dp = Dispatcher()
sticker_files = []

def get_compliment_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="✨ Получить приятные слова ✨"))
    return builder.as_markup(resize_keyboard=True)

@dp.message(CommandStart())
async def command_start_handler(message: types.Message):
    await message.answer(
        "Привет, Полина! 😊\n"
        "Создал этого небольшого бота специально для тебя, чтобы он мог поднять тебе настроение в любой момент. "
        "Просто нажимай на кнопку ниже!",
        reply_markup=get_compliment_keyboard()
    )

@dp.message(lambda message: message.text == "✨ Получить приятные слова ✨")
async def send_compliment(message: types.Message):
    random_compliment = random.choice(COMPLIMENTS)
    await message.answer(random_compliment, reply_markup=get_compliment_keyboard())
    
    if sticker_files:
        random_sticker = random.choice(sticker_files)
        await message.answer_sticker(sticker=random_sticker)

# Функция, которая сработает при запуске сервера
async def on_startup(bot: Bot):
    global sticker_files
    print("Проверяем и загружаем стикерпак с котятами...")
    try:
        sticker_set = await bot.get_sticker_set(name=STICKER_PACK_NAME)
        sticker_files = [sticker.file_id for sticker in sticker_set.stickers]
        print(f"Успешно загружено стикеров: {len(sticker_files)}")
    except Exception as e:
        print(f"Не удалось загрузить стикеры. Ошибка: {e}")
        
    print(f"Устанавливаем вебхук на адрес: {WEBHOOK_URL}")
    await bot.set_webhook(WEBHOOK_URL)

def main():
    dp.startup.register(on_startup)
    
    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    
    setup_application(app, dp, bot=bot)
    
    print(f"Запуск веб-сервера на порту {PORT}...")
    web.run_app(app, host="0.0.0.0", port=PORT)

if __name__ == "__main__":
    main()
