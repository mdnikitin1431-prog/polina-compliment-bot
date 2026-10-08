import asyncio
import random
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID") # Твой ID для получения уведомлений о друзьях
STICKER_PACK_NAME = "myaumurksksks_by_TgEmojiBot"

RENDER_URL = os.getenv("RENDER_EXTERNAL_URL")
WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = f"{RENDER_URL}{WEBHOOK_PATH}"
PORT = int(os.getenv("PORT", 8080))

# Списки текстов под разные состояния
SAD_RESPONSES = [
    "Эй, не грусти! Помни, что даже после самого сильного дождя всегда выходит солнце. Ты сильнее, чем думаешь! ☀️",
    "Если тебе тяжело прямо сейчас — это нормально. Дай себе выдохнуть. Всё обязательно наладится! 🙌",
    "Ты уникальный и крутой человек, и одна временная тучка на небе этого не изменит. Улыбнись! ⭐",
    "Посылаю тебе лучи поддержки! Ты не один(а), и всё образуется. Всё будет хорошо! 🎯"
    "Вся боль что ты испытываешь это лишь одна страница книги под названием жизнь, перелестни ее и продолжай историю дальше. У тебя все получится"
    "Если тебе одиноко лучше поговори с тем кто по твоему мнению действительно будет готов выслушать тебя и помочь, не молчи"
    "Подумай не о том как тебе плохо, а о том как сделать так, чтобы тебе стало хорошо. Может отвлечься на игры, книги или общение? Но посидеть одному и подумать тоже вариант если ты этого хочешь, главное не закапывайся ❤️"
    "Ты не один(а), уверен у тебя есть те кто будет готов выслушать и поддержать тебя 🙃"

]

BORED_RESPONSES = [
    "Скучно? Как насчет устроить пятиминутку прослушивания любимых треков? 🎵",
    "Отличный момент, чтобы полистать TikTok, сделать разминку или написать другу! 📱",
    "Скука — это просто знак, что пора съесть что-то вкусное или открыть для себя новый сериал. 🍿",
    "Попробуй прямо сейчас сделать 10 приседаний! 💪🏻"
    "Набери другу и поболтай обо всяком :)"
    "Как насчет ностальгии? открой старый фильм, книгу или комикс! 😜"
    "Напиши родным как ты их любишь ❤️"

]

COMPLIMENTS = [
    "У тебя потрясающая энергетика, с тобой невероятно приятно и легко общаться! ✨",
    "Твоя улыбка и чувство юмора способны поднять настроение кому угодно! 😊",
    "Ты очень целеустремленный и умный человек. Уверен, тебе по плечу любые вершины! 💪",
    "Твой стиль, эстетика и то, как ты мыслишь — это очень круто и вдохновляюще! 🌟",
    "Ты умеешь заряжать позитивом и искренне поддерживать. Это редкое и ценное качество! ⚡"
    "Внешность 10/10, характер 10/10, вайб 10/10. У нас есть победитель! 🥇"
    "Ты приятный человек и проводить время с тобой это отдельный вид исскуства! 😜"
    "Ты конечно не Макс Ферстаппен но проникаешь в разум так же быстро и ювелирно, как он заходит на круг 😉"
]

PREDICTIONS = [
    "Сегодня идеальный день, чтобы побаловать себя чем-то вкусным! 🍰",
    "Звёзды говорят, что сегодня тебя ждёт неожиданная классная новость! ✉️",
    "Уровень твоей удачи сегодня: Максимальный. Смело берись за любые дела! 🎰",
    "Сегодня отличный день для уютного отдыха и крутого общения. ☕",
    "Твоя главная задача на сегодня — просто улыбнуться миру, и он улыбнется в ответ! ⭐"
    "Сегодня тот самый день который можно посвятить только себе :)"
    "Сегодня прекрасный день чтобы провести его с родными и близкими ❤️"
    "Сегодня можно сделать то что давно планировалось"
    "Сегодня удача на нуле. Шутка! Улыбнись и вперед творить и делать что нравится!"
]

MUSIC_VIBES = [
    "Лови трек для отличного и продуктивного дня! 🎧\nhttps://music.yandex.ru/album/21716997/track/99784783?utm_source=desktop&utm_medium=copy_link",
    "Время для капельки уютного и расслабляющего вайба: ✨\nhttps://music.yandex.ru/album/5037537/track/39129071?utm_source=desktop&utm_medium=copy_link",
    "Заряжаемся мощной энергией и отличным настроением! ⚡\nhttps://music.yandex.ru/album/34947298/track/135129736?utm_source=desktop&utm_medium=copy_link",
    "Атмосферный трек для прогулок или учебы: 🌌\nhttps://music.yandex.ru/album/7637767/track/53447834?utm_source=desktop&utm_medium=copy_link"
]

bot = Bot(token=TOKEN)
dp = Dispatcher()
sticker_files = []

# Главная нижняя клавиатура (всегда на месте)
def get_main_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="🚀 Заряд мотивации"))
    builder.add(types.KeyboardButton(text="🔮 Совет дня"))
    builder.add(types.KeyboardButton(text="🐱 Котик"))
    builder.add(types.KeyboardButton(text="🎵 Музыкальный вайб"))
    builder.adjust(2, 2)
    return builder.as_markup(resize_keyboard=True)

# Инлайн-меню настроения (появляется при нажатии на Заряд мотивации)
def get_mood_inline_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Мне грустно 🥺", callback_data="mood_sad"))
    builder.add(types.InlineKeyboardButton(text="Мне скучно 🥱", callback_data="mood_bored"))
    builder.add(types.InlineKeyboardButton(text="Хочу комплимент! 🥰", callback_data="mood_compliment"))
    builder.adjust(2, 1) # Первые две кнопки в ряд, третья под ними
    return builder.as_markup()

# Старт бота (Обращается по реальному имени пользователя!)
@dp.message(CommandStart())
async def command_start_handler(message: types.Message):
    user_name = message.from_user.first_name if message.from_user.first_name else "Друг"
    
    await message.answer(
        f"Привет, {user_name}! 👋😊\n\n"
        "Добро пожаловать в твой личный карманный антистресс-помощник! 🚀\n"
        "Этот бот создан, чтобы поднимать тебе настроение, мотивировать перед сложными задачами и просто делиться теплом.\n\n"
        "Выбирай нужный раздел на кнопках ниже 👇",
        reply_markup=get_main_keyboard()
    )
    
    # Уведомление для тебя (Админа) о новом пользователе
    if ADMIN_ID:
        try:
            username_info = f"(@{message.from_user.username})" if message.from_user.username else ""
            await bot.send_message(
                chat_id=ADMIN_ID,
                text=f"🔔 **Новый запуск бота!**\nПользователь: {user_name} {username_info}\nID: {message.from_user.id}"
            )
        except Exception as e:
            print(f"Не удалось отправить уведомление админу: {e}")

# Обработка текстовой кнопки "Заряд мотивации" -> выкатываем инлайн-меню
@dp.message(lambda message: message.text == "🚀 Заряд мотивации")
async def motivation_handler(message: types.Message):
    await message.answer(
        "Выбери, что ты чувствуешь прямо сейчас, и я подберу правильные слова: 👇",
        reply_markup=get_mood_inline_keyboard()
    )

# Обработка нажатий на инлайн-кнопки настроения
@dp.callback_query(lambda c: c.data.startswith("mood_"))
async def mood_callback_handler(callback: types.CallbackQuery):
    await callback.answer() # Убираем бесконечную загрузку часиков на кнопке
    
    if callback.data == "mood_sad":
        text = random.choice(SAD_RESPONSES)
    elif callback.data == "mood_bored":
        text = random.choice(BORED_RESPONSES)
    elif callback.data == "mood_compliment":
        text = f"{callback.from_user.first_name}, " + random.choice(COMPLIMENTS)
        
    await callback.message.answer(text)
    
    # К комплименту или грусти прикрепляем случайного котика
    if callback.data in ["mood_sad", "mood_compliment"] and sticker_files:
        random_sticker = random.choice(sticker_files)
        await callback.message.answer_sticker(sticker=random_sticker)

# Обработка остальных текстовых кнопок
@dp.message(lambda message: message.text == "🔮 Совет дня")
async def send_prediction(message: types.Message):
    random_prediction = random.choice(PREDICTIONS)
    await message.answer(f"🔮 **Твой совет на сегодня:**\n\n{random_prediction}", parse_mode="Markdown")

@dp.message(lambda message: message.text == "🐱 Антистресс-котейка")
async def send_cat_sticker(message: types.Message):
    if sticker_files:
        random_sticker = random.choice(sticker_files)
        await message.answer_sticker(sticker=random_sticker)
    else:
        await message.answer("Котейки временно разбежались, но скоро вернутся! 🐾")

@dp.message(lambda message: message.text == "🎵 Музыкальный вайб")
async def send_music(message: types.Message):
    random_music = random.choice(MUSIC_VIBES)
    await message.answer(random_music)

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
