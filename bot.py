import asyncio
import random
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

TOKEN = os.getenv("BOT_TOKEN")
STICKER_PACK_NAME = "myaumurksksks_by_TgEmojiBot"

# Render автоматически выдает URL твоего приложения в переменную окружения RENDER_EXTERNAL_URL
RENDER_URL = os.getenv("RENDER_EXTERNAL_URL")
WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = f"{RENDER_URL}{WEBHOOK_PATH}"

# Настройки порта для сервера
PORT = int(os.getenv("PORT", 8080))

COMPLIMENTS = [
    "Успехов тебе на занятиях 🙃",
    "Ты очень умная и меня поражает твое упорство в учебе, всем бы быть такими упорными как ты 🤩",
    "С тобой классно шутить и угарать вместе, спасибо за это",
    "С тобой безумно интересно общаться, ты классный собеседник. 📚",
    "твоя эстетика просто топ 😎",
    "ты умеешь вдохновлять и заряжать позитивом. Спасибо за твою классную энергию! ⚡",
    "Ты невероятно искренний и надежный человек. Это очень круто! 💪🏻",
    "пусть сегодняшний дентопринесет тебе много крутых моментов и поводов для улыбки! А если что пиши мне ;)",
    "ты не 10/10, ты как мемы с меллстройностью у меня в реках: 100/10 😊",
    "у тебя прикольный голос",
    "рад что у нас есть общие интересы 😋",
    "не думал что найду в Дайвинчике такого крутого человека 👌🏻",
    "хорошего дня!",
    "не грусти :)"
    "улыбнись 😁",
    "можешь написать мне как день прошел, я выслушаю 😌",
    "если есть проблемы то не грузись а делись со мной 😉",
    "ты просто босс, ты просто начальник 😮‍💨",
    "бесплатный лимит комплиментов исчерпан! Купите подписку для большего количества комплиментов! Шутка, хорошего настроения тебе :)",
    "спасибо что можем болтать :)",
    "пиши почаще не стесняйся 😉",
    "как тебе погодка? Или слишком банально? Тогда в лс за более оригинальным комплиментом 😋"

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
        "Привет!\n"
        "Создал этого небольшого бота чтобы он мог поднять тебе настроение в любой момент. "
        "Просто нажимай на кнопку ниже чтобы получить комплимент! Удачного пользования :)",
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
