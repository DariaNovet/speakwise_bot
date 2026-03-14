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

TOKEN = "8616377232:AAGfTmBBylfJiR92lO_u4Fm1gDN9sFFxlVA"
bot = telebot.TeleBot(TOKEN)

# ========== БАЗА ДАННЫХ ПОЛЬЗОВАТЕЛЕЙ ==========
user_data = {}

# ========== БОЛЬШАЯ БАЗА СЛОВ ПО ТЕМАМ И УРОВНЯМ ==========
WORD_BASE = {
    "food": {
        "A1": [
            {"word": "apple", "translation": "яблоко", "example": "I eat an apple every day."},
            {"word": "banana", "translation": "банан", "example": "Monkeys like bananas."},
            {"word": "bread", "translation": "хлеб", "example": "I buy bread in the morning."},
            {"word": "milk", "translation": "молоко", "example": "Children drink milk."},
            {"word": "egg", "translation": "яйцо", "example": "I have an egg for breakfast."},
        ],
        "A2": [
            {"word": "beverage", "translation": "напиток", "example": "Tea is a hot beverage."},
            {"word": "recipe", "translation": "рецепт", "example": "This recipe is easy."},
            {"word": "ingredient", "translation": "ингредиент", "example": "Flour is the main ingredient."},
        ],
        "B1": [
            {"word": "cuisine", "translation": "кухня (национальная)", "example": "Italian cuisine is popular."},
            {"word": "appetizer", "translation": "закуска", "example": "We ordered an appetizer."},
        ],
        "B2": [
            {"word": "gourmet", "translation": "гурман", "example": "He is a gourmet chef."},
            {"word": "palate", "translation": "нёбо / вкус", "example": "This dish pleases the palate."},
        ]
    },
    "family": {
        "A1": [
            {"word": "mother", "translation": "мама", "example": "My mother is kind."},
            {"word": "father", "translation": "папа", "example": "My father works hard."},
            {"word": "brother", "translation": "брат", "example": "I have a brother."},
            {"word": "sister", "translation": "сестра", "example": "My sister is young."},
        ],
        "A2": [
            {"word": "grandmother", "translation": "бабушка", "example": "My grandmother tells stories."},
            {"word": "grandfather", "translation": "дедушка", "example": "My grandfather is old."},
        ],
        "B1": [
            {"word": "relative", "translation": "родственник", "example": "We visited our relatives."},
            {"word": "spouse", "translation": "супруг/а", "example": "My spouse works in a bank."},
        ],
        "B2": [
            {"word": "ancestor", "translation": "предок", "example": "My ancestors came from Europe."},
            {"word": "descendant", "translation": "потомок", "example": "He is a descendant of a famous family."},
        ]
    },
    "travel": {
        "A1": [
            {"word": "hotel", "translation": "отель", "example": "We stayed in a hotel."},
            {"word": "plane", "translation": "самолёт", "example": "The plane is fast."},
            {"word": "ticket", "translation": "билет", "example": "I bought a ticket."},
        ],
        "A2": [
            {"word": "passport", "translation": "паспорт", "example": "Don't forget your passport."},
            {"word": "luggage", "translation": "багаж", "example": "My luggage is heavy."},
        ],
        "B1": [
            {"word": "destination", "translation": "место назначения", "example": "Our destination is Paris."},
            {"word": "itinerary", "translation": "маршрут", "example": "We planned an itinerary."},
        ],
        "B2": [
            {"word": "expedition", "translation": "экспедиция", "example": "They went on an expedition."},
            {"word": "excursion", "translation": "экскурсия", "example": "We booked an excursion."},
        ]
    }
}

# ========== БАЗА ГРАММАТИЧЕСКИХ ОШИБОК ==========
GRAMMAR_MISTAKES = {
    "A1": [
        {"wrong": "He go to school", "correct": "He goes to school", "explanation": "После he нужно добавлять -es к глаголу (go → goes)"},
        {"wrong": "She don't like coffee", "correct": "She doesn't like coffee", "explanation": "С she используется doesn't, а не don't"},
        {"wrong": "They was happy", "correct": "They were happy", "explanation": "С they используется were, а не was"},
    ],
    "A2": [
        {"wrong": "I have went", "correct": "I have gone", "explanation": "После have используется третья форма глагола (go → gone)"},
        {"wrong": "She can to sing", "correct": "She can sing", "explanation": "После модальных глаголов (can, must, should) частица to не ставится"},
    ],
    "B1": [
        {"wrong": "If I will see him", "correct": "If I see him", "explanation": "В условных предложениях после if не используется will"},
        {"wrong": "I am used to get up early", "correct": "I am used to getting up early", "explanation": "После be used to нужен герундий (-ing)"},
    ],
    "B2": [
        {"wrong": "She suggested me to go", "correct": "She suggested that I go", "explanation": "После suggest не используется инфинитив с to"},
        {"wrong": "I look forward to meet you", "correct": "I look forward to meeting you", "explanation": "После look forward to нужен герундий (-ing)"},
    ]
}

# ========== БАЗА ТЕКСТОВ С ОШИБКАМИ ==========
TEXTS_WITH_ERRORS = {
    "A1": [
        {
            "title": "My Day",
            "wrong": "Every day I wake up at 7 o'clock. I have a breakfast. I go to school. My favorite subject is English. I like it.",
            "correct": "Every day I wake up at 7 o'clock. I have breakfast. I go to school. My favorite subject is English. I like it.",
            "errors": ["a breakfast", "", ""]
        }
    ],
    "A2": [
        {
            "title": "Last Weekend",
            "wrong": "Last weekend I go to the park with my friends. We play football and then we eat ice cream. It was fun.",
            "correct": "Last weekend I went to the park with my friends. We played football and then we ate ice cream. It was fun.",
            "errors": ["go", "play", "eat"]
        }
    ],
    "B1": [
        {
            "title": "Travel Plans",
            "wrong": "If I will have money, I travel to Japan next year. I want visit Tokyo and see the cherry blossoms.",
            "correct": "If I have money, I will travel to Japan next year. I want to visit Tokyo and see the cherry blossoms.",
            "errors": ["will have", "travel", "want visit"]
        }
    ],
    "B2": [
        {
            "title": "Environmental Issues",
            "wrong": "Many people is concerned about climate change. They think that we should to do more to protect the environment.",
            "correct": "Many people are concerned about climate change. They think that we should do more to protect the environment.",
            "errors": ["is", "should to", ""]
        }
    ]
}

# ========== ПРИВЕТСТВИЕ ==========
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    if user_id not in user_data:
        user_data[user_id] = {
            "vocabulary": [],
            "unknown_words": [],
            "mistakes_count": {},
            "current_level": "A1",
            "current_topic": "food",
            "current_word_data": None
        }

    markup = main_menu_keyboard()
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
— «📄 Скачать словарь (PDF)» — красивое оформление

⬇️ *Выбери режим ниже*
    """
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=markup)

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

# ========== ВЫБОР УРОВНЯ ==========
def level_keyboard(callback_prefix):
    markup = types.InlineKeyboardMarkup()
    levels = ["A1", "A2", "B1", "B2"]
    for level in levels:
        markup.add(types.InlineKeyboardButton(level, callback_data=f"{callback_prefix}_{level}"))
    return markup

# ========== МЕНЮ ДЕЙСТВИЙ ПОСЛЕ ЗАДАНИЯ ==========
def after_task_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("🔁 Продолжить в этой теме"))
    markup.add(types.KeyboardButton("📂 Сменить тему"), types.KeyboardButton("📊 Поменять уровень"))
    markup.add(types.KeyboardButton("🏠 Главное меню"))
    return markup

# ========== АУДИРОВАНИЕ ==========
@bot.message_handler(func=lambda message: message.text == "👂 Аудирование")
def listening_mode(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    topics = list(WORD_BASE.keys())
    for topic in topics:
        markup.add(types.KeyboardButton(f"🎧 {topic}"))
    markup.add(types.KeyboardButton("🔙 Главное меню"))
    bot.send_message(message.chat.id, "👂 Сначала выбери тему:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text.startswith("🎧 "))
def handle_topic_choice(message):
    user_id = message.from_user.id
    topic = message.text.replace("🎧 ", "").strip()
    user_data[user_id]["current_topic"] = topic
    
    bot.send_message(message.chat.id, f"📚 Тема: {topic}\nТеперь выбери уровень сложности:")
    bot.send_message(message.chat.id, "Уровни:", reply_markup=level_keyboard("listening"))

def generate_audio(word):
    tts = gTTS(text=word, lang='en')
    filename = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3').name
    tts.save(filename)
    return filename

def send_next_word(chat_id, user_id):
    topic = user_data[user_id]["current_topic"]
    level = user_data[user_id]["current_level"]
    
    words_in_topic = WORD_BASE.get(topic, {}).get(level, [])
    if not words_in_topic:
        bot.send_message(chat_id, "😕 Для этой темы и уровня пока нет слов. Попробуй другую тему или уровень.")
        return
    
    word_data = random.choice(words_in_topic)
    user_data[user_id]["current_word_data"] = word_data
    
    audio_file = generate_audio(word_data["word"])
    with open(audio_file, 'rb') as f:
        bot.send_voice(chat_id, f)
    os.unlink(audio_file)
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("❓ Не знаю"), types.KeyboardButton("➕ В словарь"))
    markup.add(types.KeyboardButton("🔙 Главное меню"))
    
    bot.send_message(
        chat_id, 
        f"📝 Напиши это слово и его перевод (например: {word_data['word']} — {word_data['translation']})",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("listening_"))
def handle_listening_level(call):
    user_id = call.from_user.id
    level = call.data.split("_")[1]
    user_data[user_id]["current_level"] = level
    send_next_word(call.message.chat.id, user_id)

# ========== ОБРАБОТКА КНОПОК ПОСЛЕ ЗАДАНИЯ ==========
@bot.message_handler(func=lambda message: message.text in ["🔁 Продолжить в этой теме", "📂 Сменить тему", "📊 Поменять уровень", "🏠 Главное меню"])
def handle_after_task_buttons(message):
    user_id = message.from_user.id
    text = message.text
    
    if text == "🏠 Главное меню":
        send_welcome(message)
        return
    
    if text == "🔁 Продолжить в этой теме":
        send_next_word(message.chat.id, user_id)
        return
    
    if text == "📂 Сменить тему":
        listening_mode(message)
        return
    
    if text == "📊 Поменять уровень":
        bot.send_message(message.chat.id, "Выбери новый уровень:", reply_markup=level_keyboard("listening"))
        return

# ========== ОБРАБОТКА СПЕЦИАЛЬНЫХ КНОПОК ==========
@bot.message_handler(func=lambda message: message.text in ["❓ Не знаю", "➕ В словарь", "🔙 Главное меню"])
def handle_special_buttons(message):
    user_id = message.from_user.id
    text = message.text
    
    if text == "🔙 Главное меню":
        send_welcome(message)
        return
    
    word_data = user_data[user_id].get("current_word_data")
    if not word_data:
        bot.send_message(message.chat.id, "Сначала выбери слово в режиме аудирования")
        return
    
    if text == "❓ Не знаю":
        bot.send_message(
            message.chat.id, 
            f"🔍 Это слово: *{word_data['word']}*\nПеревод: *{word_data['translation']}*\nПример: {word_data['example']}",
            parse_mode="Markdown"
        )
        user_data[user_id]["unknown_words"].append(word_data["word"])
        
        # Меню действий после задания
        bot.send_message(message.chat.id, "Что хочешь сделать дальше?", reply_markup=after_task_keyboard())
    
    elif text == "➕ В словарь":
        word_entry = {
            "word": word_data["word"],
            "translation": word_data["translation"],
            "example": word_data["example"],
            "topic": user_data[user_id]["current_topic"]
        }
        if word_entry not in user_data[user_id]["vocabulary"]:
            user_data[user_id]["vocabulary"].append(word_entry)
            bot.send_message(message.chat.id, f"✅ Слово *{word_data['word']}* добавлено в словарь", parse_mode="Markdown")
        else:
            bot.send_message(message.chat.id, "ℹ️ Это слово уже в словаре")
        
        # Меню действий после задания
        bot.send_message(message.chat.id, "Что хочешь сделать дальше?", reply_markup=after_task_keyboard())

# ========== ПРОВЕРКА ОТВЕТА НА АУДИРОВАНИЕ ==========
@bot.message_handler(func=lambda message: message.text not in ["❓ Не знаю", "➕ В словарь", "🔙 Главное меню", "🔁 Продолжить в этой теме", "📂 Сменить тему", "📊 Поменять уровень", "🏠 Главное меню"])
def check_listening_answer(message):
    user_id = message.from_user.id
    text = message.text.strip()

    word_data = user_data[user_id].get("current_word_data")
    if not word_data:
        bot.send_message(message.chat.id, "⚠️ Сначала выбери слово в режиме аудирования")
        return

    expected_word = word_data["word"]
    translation = word_data["translation"]
    example = word_data["example"]

    # Если пользователь написал слово и перевод через —
    if "—" in text:
        parts = text.split("—")
        user_word = parts[0].strip().lower()
        user_trans = parts[1].strip()
    else:
        user_word = text.lower()
        user_trans = ""

    # Проверка слова
    if user_word == expected_word.lower():
        bot.send_message(
            message.chat.id,
            f"✅ *Верно!*\n\nСлово: {expected_word}\nПеревод: {translation}\nПример: {example}",
            parse_mode="Markdown"
        )
    else:
        bot.send_message(
            message.chat.id,
            f"❌ *Ошибка в написании*\n\nТы написала: {user_word}\nПравильно: {expected_word}\n\nПеревод: {translation}\nПример: {example}",
            parse_mode="Markdown"
        )
        # Увеличиваем счётчик ошибок по теме
        topic = user_data[user_id].get("current_topic", "unknown")
        user_data[user_id]["mistakes_count"][topic] = user_data[user_id]["mistakes_count"].get(topic, 0) + 1
    
    # Меню действий после задания
    bot.send_message(message.chat.id, "Что хочешь сделать дальше?", reply_markup=after_task_keyboard())

# ========== ГРАММАТИЧЕСКИЙ ДЕТЕКТИВ ==========
@bot.message_handler(func=lambda message: message.text == "🧠 Грамматический детектив")
def grammar_detective_mode(message):
    user_id = message.from_user.id
    bot.send_message(message.chat.id, "🎯 Выбери уровень сложности:", reply_markup=level_keyboard("grammar"))

@bot.callback_query_handler(func=lambda call: call.data.startswith("grammar_"))
def handle_grammar_level(call):
    user_id = call.from_user.id
    level = call.data.split("_")[1]
    
    mistakes = GRAMMAR_MISTAKES.get(level, [])
    if not mistakes:
        bot.send_message(call.message.chat.id, "😕 Для этого уровня пока нет заданий. Попробуй другой уровень.")
        return
    
    mistake = random.choice(mistakes)
    user_data[user_id]["current_mistake"] = mistake
    
    bot.send_message(
        call.message.chat.id,
        f"🧠 *Найди и исправь ошибку:*\n\n_{mistake['wrong']}_\n\n🎤 Скажи правильный вариант голосом",
        parse_mode="Markdown"
    )
    bot.send_message(call.message.chat.id, "Говори...", reply_markup=after_task_keyboard())

# ========== ТЕКСТ С ОШИБКАМИ ==========
@bot.message_handler(func=lambda message: message.text == "📖 Текст с ошибками")
def text_with_errors_mode(message):
    user_id = message.from_user.id
    bot.send_message(message.chat.id, "📖 Выбери уровень сложности:", reply_markup=level_keyboard("text"))

@bot.callback_query_handler(func=lambda call: call.data.startswith("text_"))
def handle_text_level(call):
    user_id = call.from_user.id
    level = call.data.split("_")[1]
    
    texts = TEXTS_WITH_ERRORS.get(level, [])
    if not texts:
        bot.send_message(call.message.chat.id, "😕 Для этого уровня пока нет текстов. Попробуй другой уровень.")
        return
    
    text_data = random.choice(texts)
    user_data[user_id]["current_text"] = text_data
    
    bot.send_message(
        call.message.chat.id,
        f"📖 *{text_data['title']}*\n\n_{text_data['wrong']}_\n\n🎤 Прочитай этот текст вслух, исправляя ошибки",
        parse_mode="Markdown"
    )
    bot.send_message(call.message.chat.id, "Говори...", reply_markup=after_task_keyboard())

# ========== МОЙ СЛОВАРЬ ==========
@bot.message_handler(func=lambda message: message.text == "📘 Мой словарь")
def my_vocabulary(message):
    user_id = message.from_user.id
    vocab = user_data[user_id]["vocabulary"]
    
    if not vocab:
        bot.send_message(message.chat.id, "📘 В словаре пока пусто. Добавляй слова с помощью кнопки «➕ В словарь»")
        return
    
    text = "📘 *Твой словарь:*\n\n"
    for item in vocab:
        text += f"• {item['word']} — {item['translation']}\n  _{item['example']}_\n\n"
    
    # Разбиваем на части, если слишком длинно
    if len(text) > 4000:
        parts = [text[i:i+4000] for i in range(0, len(text), 4000)]
        for part in parts:
            bot.send_message(message.chat.id, part, parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, text, parse_mode="Markdown")

# ========== МОИ ОШИБКИ ==========
@bot.message_handler(func=lambda message: message.text == "📊 Мои ошибки")
def my_mistakes(message):
    user_id = message.from_user.id
    mistakes = user_data[user_id]["mistakes_count"]
    
    if not mistakes:
        bot.send_message(message.chat.id, "📊 У тебя пока нет зафиксированных ошибок. Продолжай тренировки!")
        return
    
    text = "📊 *Твои частые ошибки по темам:*\n"
    sorted_mistakes = sorted(mistakes.items(), key=lambda x: x[1], reverse=True)
    
    for topic, count in sorted_mistakes:
        text += f"• {topic}: {count} ошибок\n"
    
    most_common = sorted_mistakes[0][0] if sorted_mistakes else None
    if most_common:
        text += f"\n💡 Чаще всего ты ошибаешься в теме *{most_common}*."
    
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

# ========== PDF СЛОВАРЬ ==========
@bot.message_handler(func=lambda message: message.text == "📄 Скачать словарь (PDF)")
def pdf_vocabulary(message):
    user_id = message.from_user.id
    vocab = user_data[user_id]["vocabulary"]
    
    if not vocab:
        bot.send_message(message.chat.id, "📄 Словарь пуст. Нечего скачивать.")
        return
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Мой словарь", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", size=12)
    for item in vocab:
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 8, txt=f"{item['word']} — {item['translation']}", ln=True)
        pdf.set_font("Arial", 'I', 10)
        pdf.cell(200, 6, txt=f"Пример: {item['example']}", ln=True)
        pdf.ln(4)
    
    pdf_output = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    pdf.output(pdf_output.name)
    
    with open(pdf_output.name, 'rb') as f:
        bot.send_document(message.chat.id, f, caption="📘 Твой личный словарь")
    
    os.unlink(pdf_output.name)

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    print("✅ БОТ ЗАПУЩЕН")
    bot.polling(none_stop=True)