import telebot
import random
import requests
import os
import difflib
import tempfile
from telebot import types
from gtts import gTTS
from fpdf import FPDF
import time
import re
import json

TOKEN = "8616377232:AAGfTmBBylfJiR92lO_u4Fm1gDN9sFFxlVA"
bot = telebot.TeleBot(TOKEN)

# ========== БАЗА ДАННЫХ ПОЛЬЗОВАТЕЛЕЙ ==========
user_data = {}

# ========== БАЗА СЛОВ ==========
WORD_BASE = {
    "food": {
        "A1": [{"word": "apple", "translation": "яблоко"}, {"word": "banana", "translation": "банан"}],
        "A2": [{"word": "beverage", "translation": "напиток"}],
        "B1": [{"word": "cuisine", "translation": "кухня"}],
        "B2": [{"word": "gourmet", "translation": "гурман"}]
    },
    "family": {
        "A1": [{"word": "mother", "translation": "мама"}, {"word": "father", "translation": "папа"}],
        "A2": [{"word": "grandmother", "translation": "бабушка"}],
        "B1": [{"word": "relative", "translation": "родственник"}],
        "B2": [{"word": "ancestor", "translation": "предок"}]
    }
}

# ========== ГРАММАТИКА ==========
GRAMMAR_MISTAKES = {
    "A1": [{"wrong": "He go to school", "correct": "He goes to school", "explanation": "После he нужен глагол с -es"}],
    "A2": [{"wrong": "I have went", "correct": "I have gone", "explanation": "После have нужна третья форма"}]
}

# ========== ТЕКСТЫ ==========
TEXTS_WITH_ERRORS = {
    "A1": [{"title": "My Day", "wrong": "I have a breakfast", "correct": "I have breakfast"}]
}

# ========== ПРИВЕТСТВИЕ ==========
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    user_data[user_id] = {
        "vocabulary": [],
        "unknown_words": [],
        "mistakes_count": {},
        "current_level": "A1",
        "current_topic": "food",
        "current_word_data": None,
        "current_mistake": None,
        "current_text": None,
        "current_mode": None
    }

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton("👂 Аудирование"),
        types.KeyboardButton("🧠 Грамматический детектив"),
        types.KeyboardButton("📖 Текст с ошибками"),
        types.KeyboardButton("📘 Мой словарь"),
        types.KeyboardButton("📊 Мои ошибки"),
        types.KeyboardButton("📄 Скачать словарь (PDF)")
    )
    bot.send_message(
        message.chat.id,
        "🎙️ Добро пожаловать!",
        reply_markup=markup
    )

# ========== АУДИРОВАНИЕ ==========
@bot.message_handler(func=lambda message: message.text == "👂 Аудирование")
def listening_mode(message):
    user_id = message.from_user.id
    user_data[user_id]["current_mode"] = "listening"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for topic in WORD_BASE.keys():
        markup.add(types.KeyboardButton(f"🎧 {topic}"))
    markup.add(types.KeyboardButton("🏠 Главное меню"))
    bot.send_message(message.chat.id, "Выбери тему:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text.startswith("🎧 "))
def handle_topic(message):
    user_id = message.from_user.id
    topic = message.text.replace("🎧 ", "")
    user_data[user_id]["current_topic"] = topic
    bot.send_message(message.chat.id, "Выбери уровень:", reply_markup=level_keyboard("listening"))

def level_keyboard(prefix):
    markup = types.InlineKeyboardMarkup()
    for level in ["A1", "A2", "B1", "B2"]:
        markup.add(types.InlineKeyboardButton(level, callback_data=f"{prefix}_{level}"))
    return markup

def generate_audio(word):
    tts = gTTS(text=word, lang='en')
    path = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3').name
    tts.save(path)
    return path

def send_word(chat_id, user_id):
    topic = user_data[user_id]["current_topic"]
    level = user_data[user_id]["current_level"]
    words = WORD_BASE.get(topic, {}).get(level, [])
    if not words:
        bot.send_message(chat_id, "Нет слов")
        return
    word_data = random.choice(words)
    user_data[user_id]["current_word_data"] = word_data
    audio = generate_audio(word_data["word"])
    with open(audio, 'rb') as f:
        bot.send_voice(chat_id, f)
    os.unlink(audio)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("❓ Не знаю"), types.KeyboardButton("➕ В словарь"))
    markup.add(types.KeyboardButton("🏠 Главное меню"))
    bot.send_message(chat_id, "Напиши слово и перевод через —", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("listening_"))
def handle_level(call):
    user_id = call.from_user.id
    level = call.data.split("_")[1]
    user_data[user_id]["current_level"] = level
    send_word(call.message.chat.id, user_id)

@bot.message_handler(func=lambda message: message.text in ["❓ Не знаю", "➕ В словарь", "🏠 Главное меню"])
def handle_buttons(message):
    user_id = message.from_user.id
    if message.text == "🏠 Главное меню":
        send_welcome(message)
        return
    word_data = user_data[user_id].get("current_word_data")
    if not word_data:
        return
    if message.text == "❓ Не знаю":
        bot.send_message(message.chat.id, f"{word_data['word']} — {word_data['translation']}")
        user_data[user_id]["unknown_words"].append(word_data["word"])
    elif message.text == "➕ В словарь":
        user_data[user_id]["vocabulary"].append(word_data)
        bot.send_message(message.chat.id, "✅ Добавлено")
    bot.send_message(message.chat.id, "Что дальше?", reply_markup=after_keyboard())

def after_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("🔁 Продолжить"))
    markup.add(types.KeyboardButton("🏠 Главное меню"))
    return markup

@bot.message_handler(func=lambda message: message.text == "🔁 Продолжить")
def continue_listening(message):
    user_id = message.from_user.id
    if user_data[user_id].get("current_mode") == "listening":
        send_word(message.chat.id, user_id)

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    print("✅ Бот запущен")
    bot.polling(none_stop=True)