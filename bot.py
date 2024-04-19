from aiogram import types
from aiogram.types import WebAppInfo
from aiogram.utils import executor
import sqlite3
from config import dp, bot

DATABASE_NAME = "users_bd"


def create_database():
    conn = sqlite3.connect(f"{DATABASE_NAME}.sqlite")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users(user_id TEXT PRIMARY KEY, username TEXT, first_name TEXT)''')
    conn.commit()
    conn.close()


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    # Получаем информацию о пользователе
    user_id = str(message.from_user.id)
    username = message.from_user.username
    first_name = message.from_user.first_name

    # Подключаемся к базе данных
    conn = sqlite3.connect(f"{DATABASE_NAME}.sqlite")
    cursor = conn.cursor()

    # Проверяем, есть ли пользователь в базе данных
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    existing_user = cursor.fetchone()

    if not existing_user:
        # Добавляем пользователя в базу данных
        cursor.execute("INSERT INTO users (user_id, username, first_name) VALUES (?, ?, ?)",
                       (user_id, username, first_name))
        conn.commit()

    # Закрываем соединение с базой данных
    conn.close()
    keyboard = types.InlineKeyboardMarkup()

    povel_durev_button = types.InlineKeyboardButton(text="POVEL DUREV", url="https://t.me/poveldurev")
    ru_chat_button = types.InlineKeyboardButton(text="RU CHAT", url="http://t.me/SafeguardRobot?start=-1001936733550")
    eng_chat_button = types.InlineKeyboardButton(text="ENG CHAT", url="http://t.me/SafeguardRobot?start=-1002104437904")
    site_button = types.InlineKeyboardButton(text="Site", web_app=WebAppInfo(url="http://durev.xyz"))
    x_button = types.InlineKeyboardButton(text="X (Twitter)", url="https://x.com/poveldurev")
    purchase_exchange_button = types.InlineKeyboardButton(text="Purchase and exchange",
                                                          callback_data="purchase_exchange")
    keyboard.add(povel_durev_button)
    keyboard.add(ru_chat_button, eng_chat_button)
    keyboard.add(site_button, x_button)
    keyboard.add(purchase_exchange_button)

    await message.answer("Navigation menu", reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == 'back_to_menu')
async def back_to_menu_callback_handler(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    await start_command(callback_query.message)


@dp.callback_query_handler(lambda c: c.data == 'purchase_exchange')
async def purchase_exchange_callback_handler(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    keyboard = types.InlineKeyboardMarkup()

    stonfi_button = types.InlineKeyboardButton(text="Ston.FI", web_app=WebAppInfo(
        url="https://app.ston.fi/swap?chartVisible=false&chartInterval=1w&ft=TON&tt=durev"))
    dedust_button = types.InlineKeyboardButton(text="DeDust", web_app=WebAppInfo(url="https://dedust.io/swap/TON/DUREV"))
    ton_diamonds_button = types.InlineKeyboardButton(text="TON Diamonds", web_app=WebAppInfo(
        url="https://ton.diamonds/dex/swap?inputToken=TON&outputToken=EQB02DJ0cdUD4iQDRbBv4aYG3htePHBRK1tGeRtCnatescK0"))
    ton_planets_button = types.InlineKeyboardButton(text="TON Planets", web_app=WebAppInfo(
        url="https://mars.tonplanets.com/en/dex/?from=TON&to=EQB02DJ0cdUD4iQDRbBv4aYG3htePHBRK1tGeRtCnatescK0"))
    back_button = types.InlineKeyboardButton(text="Back to Menu", callback_data="back_to_menu")

    keyboard.add(stonfi_button, dedust_button)
    keyboard.add(ton_diamonds_button, ton_planets_button)
    keyboard.add(back_button)
    await callback_query.message.answer("Choose an option:", reply_markup=keyboard)


async def startup(dp):
    create_database()
    print("Бот запущен!")


async def shutdown(dp):
    pass


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=startup, on_shutdown=shutdown)
