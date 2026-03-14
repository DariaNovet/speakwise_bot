import telebot
import random
import requests
import os
import difflib
from telebot import types

TOKEN = "8616377232:AAGfTmBBylfJiR92lO_u4Fm1gDN9sFFxlVA"
bot = telebot.TeleBot(TOKEN)

# Хранилище данных пользователей
user_data = {}

# ========== ПРИВЕТСТВИЕ ==========
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    if user_id not in user_data:
        user_data[user_id] = {
            "vocabulary": [],
            "unknown_words": [],
            "mistakes_count": {
                "food": 0,
                "grammar": 0,
                "pronunciation": 0
            }
        }

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👂 Аудирование")
    btn2 = types.KeyboardButton("🧠 Грамматический детектив")
    btn3 = types.KeyboardButton("📖 Текст с ошибками")
    btn4 = types.KeyboardButton("📘 Мой словарь")
    btn5 = types.KeyboardButton("📊 Мои ошибки")
    btn6 = types.KeyboardButton("📄 Скачать словарь (PDF)")
    markup.add(btn1, btn2)
    markup.add(btn3)
    markup.add(btn4, btn5, btn6)

    welcome_text = """
🎙️ *Добро пожаловать в твой личный тренажёр английского!*

🔹 *Режимы:*

👂 *АУДИРОВАНИЕ*  
Я присылаю слово голосом — ты пишешь, что услышал(а), и перевод.  
Если не знаешь — жми «❓ Не знаю».

🧠 *ГРАММАТИЧЕСКИЙ ДЕТЕКТИВ*  
Я даю предложение с ошибкой — ты исправляешь голосом.

📖 *ТЕКСТ С ОШИБКАМИ*  
Я пришлю текст с 3 ошибками.  
Твоя задача — прочитать его вслух без ошибок.

➕ *Бонусы:*  
— «➕ В словарь» — сохраняй новые слова  
— «📊 Мои ошибки» — анализ твоих слабых мест  
— «📘 Мой словарь» — повторяй сохранённое  
— «📄 Скачать словарь (PDF)» — скоро будет

📈 *Адаптивный режим:*  
Я запоминаю твои ошибки и чаще даю темы, в которых ты ошибаешься.

⬇️ *Выбери режим ниже*
    """
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=markup)

# ========== АУДИРОВАНИЕ ==========
@bot.message_handler(func=lambda message: message.text == "👂 Аудирование")
def listening_mode(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    topics = ["holidays", "hobby", "daily routines", "travelling", "food", "pets", "technologies", "family and friends", "education"]
    for topic in topics:
        markup.add(types.KeyboardButton(topic))
    markup.add(types.KeyboardButton("🔙 Главное меню"))
    bot.send_message(message.chat.id, "👂 Выбери тему:", reply_markup=markup)

# ========== ГРАММАТИЧЕСКИЙ ДЕТЕКТИВ ==========
@bot.message_handler(func=lambda message: message.text == "🧠 Грамматический детектив")
def grammar_detective_mode(message):
    bot.send_message(message.chat.id, "🧠 Скоро здесь будет грамматический детектив. А пока отдыхай 🤓", reply_markup=main_menu_keyboard())

# ========== ТЕКСТ С ОШИБКАМИ ==========
@bot.message_handler(func=lambda message: message.text == "📖 Текст с ошибками")
def text_with_errors_mode(message):
    bot.send_message(message.chat.id, "📖 Скоро здесь будет текст с ошибками. Готовь голос!", reply_markup=main_menu_keyboard())

# ========== МОЙ СЛОВАРЬ ==========
@bot.message_handler(func=lambda message: message.text == "📘 Мой словарь")
def my_vocabulary(message):
    user_id = message.from_user.id
    vocab = user_data[user_id]["vocabulary"]
    if vocab:
        bot.send_message(message.chat.id, "📘 Твой словарь:\n" + "\n".join(vocab))
    else:
        bot.send_message(message.chat.id, "📘 В словаре пока пусто. Добавляй слова с помощью кнопки «➕ В словарь»")
    bot.send_message(message.chat.id, "🔙 Главное меню:", reply_markup=main_menu_keyboard())

# ========== МОИ ОШИБКИ ==========
@bot.message_handler(func=lambda message: message.text == "📊 Мои ошибки")
def my_mistakes(message):
    user_id = message.from_user.id
    mistakes = user_data[user_id]["mistakes_count"]
    text = "📊 Твои частые ошибки по темам:\n"
    for topic, count in mistakes.items():
        text += f"• {topic}: {count}\n"
    bot.send_message(message.chat.id, text, reply_markup=main_menu_keyboard())

# ========== PDF (ЗАГОТОВКА) ==========
@bot.message_handler(func=lambda message: message.text == "📄 Скачать словарь (PDF)")
def pdf_vocabulary(message):
    bot.send_message(message.chat.id, "📄 Функция в разработке. Скоро ты сможешь скачать словарь в красивом PDF!")

# ========== ГЛАВНОЕ МЕНЮ ==========
def main_menu_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton("👂 Аудирование"),
        types.KeyboardButton("🧠 Грамматический детектив")
    )
    markup.add(types.KeyboardButton("📖 Текст с ошибками"))
    markup.add(
        types.KeyboardButton("📘 Мой словарь"),
        types.KeyboardButton("📊 Мои ошибки"),
        types.KeyboardButton("📄 Скачать словарь (PDF)")
    )
    return markup

# ========== ВОЗВРАТ В МЕНЮ ==========
@bot.message_handler(func=lambda message: message.text == "🔙 Главное меню")
def back_to_main(message):
    send_welcome(message)

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    print("Бот запущен...")
    bot.polling(none_stop=True)