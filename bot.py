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
    },
    "work": {
        "A1": [
            {"word": "job", "translation": "работа", "example": "I have a job."},
            {"word": "office", "translation": "офис", "example": "She works in an office."},
        ],
        "A2": [
            {"word": "colleague", "translation": "коллега", "example": "My colleague is helpful."},
            {"word": "boss", "translation": "начальник", "example": "The boss is strict."},
        ],
        "B1": [
            {"word": "employee", "translation": "сотрудник", "example": "He is a good employee."},
            {"word": "employer", "translation": "работодатель", "example": "The employer pays salary."},
        ],
        "B2": [
            {"word": "deadline", "translation": "срок", "example": "We have a deadline."},
            {"word": "negotiation", "translation": "переговоры", "example": "The negotiation was hard."},
        ]
    },
    "education": {
        "A1": [
            {"word": "school", "translation": "школа", "example": "I go to school."},
            {"word": "teacher", "translation": "учитель", "example": "The teacher explains."},
        ],
        "A2": [
            {"word": "student", "translation": "студент", "example": "She is a student."},
            {"word": "homework", "translation": "домашнее задание", "example": "I do my homework."},
        ],
        "B1": [
            {"word": "university", "translation": "университет", "example": "He studies at university."},
            {"word": "degree", "translation": "степень", "example": "She has a degree."},
        ],
        "B2": [
            {"word": "scholarship", "translation": "стипендия", "example": "He won a scholarship."},
            {"word": "curriculum", "translation": "учебный план", "example": "The curriculum is tough."},
        ]
    },
    "hobby": {
        "A1": [
            {"word": "music", "translation": "музыка", "example": "I like music."},
            {"word": "game", "translation": "игра", "example": "We play a game."},
        ],
        "A2": [
            {"word": "drawing", "translation": "рисование", "example": "She enjoys drawing."},
            {"word": "dance", "translation": "танец", "example": "He loves to dance."},
        ],
        "B1": [
            {"word": "photography", "translation": "фотография", "example": "Photography is my hobby."},
            {"word": "gardening", "translation": "садоводство", "example": "Gardening is relaxing."},
        ],
        "B2": [
            {"word": "calligraphy", "translation": "каллиграфия", "example": "She practices calligraphy."},
            {"word": "pottery", "translation": "гончарное дело", "example": "He makes pottery."},
        ]
    },
    "health": {
        "A1": [
            {"word": "doctor", "translation": "врач", "example": "I see a doctor."},
            {"word": "medicine", "translation": "лекарство", "example": "Take your medicine."},
        ],
        "A2": [
            {"word": "hospital", "translation": "больница", "example": "She is in hospital."},
            {"word": "healthy", "translation": "здоровый", "example": "Eat healthy food."},
        ],
        "B1": [
            {"word": "treatment", "translation": "лечение", "example": "The treatment works."},
            {"word": "symptom", "translation": "симптом", "example": "What are your symptoms?"},
        ],
        "B2": [
            {"word": "diagnosis", "translation": "диагноз", "example": "The diagnosis is clear."},
            {"word": "prescription", "translation": "рецепт", "example": "I need a prescription."},
        ]
    },
    "nature": {
        "A1": [
            {"word": "tree", "translation": "дерево", "example": "The tree is tall."},
            {"word": "flower", "translation": "цветок", "example": "The flower is red."},
        ],
        "A2": [
            {"word": "mountain", "translation": "гора", "example": "They climbed a mountain."},
            {"word": "river", "translation": "река", "example": "The river is wide."},
        ],
        "B1": [
            {"word": "forest", "translation": "лес", "example": "We walked in the forest."},
            {"word": "climate", "translation": "климат", "example": "The climate is changing."},
        ],
        "B2": [
            {"word": "ecosystem", "translation": "экосистема", "example": "The ecosystem is fragile."},
            {"word": "biodiversity", "translation": "биоразнообразие", "example": "We must protect biodiversity."},
        ]
    },
    "technology": {
        "A1": [
            {"word": "computer", "translation": "компьютер", "example": "I use a computer."},
            {"word": "phone", "translation": "телефон", "example": "My phone is new."},
        ],
        "A2": [
            {"word": "internet", "translation": "интернет", "example": "The internet is fast."},
            {"word": "website", "translation": "сайт", "example": "I visit a website."},
        ],
        "B1": [
            {"word": "software", "translation": "программное обеспечение", "example": "The software is updated."},
            {"word": "hardware", "translation": "оборудование", "example": "The hardware is expensive."},
        ],
        "B2": [
            {"word": "innovation", "translation": "инновация", "example": "Innovation drives progress."},
            {"word": "artificial intelligence", "translation": "искусственный интеллект", "example": "AI is developing fast."},
        ]
    },
    "shopping": {
        "A1": [
            {"word": "shop", "translation": "магазин", "example": "I go to the shop."},
            {"word": "price", "translation": "цена", "example": "The price is high."},
        ],
        "A2": [
            {"word": "money", "translation": "деньги", "example": "I need money."},
            {"word": "receipt", "translation": "чек", "example": "Keep the receipt."},
        ],
        "B1": [
            {"word": "discount", "translation": "скидка", "example": "I got a discount."},
            {"word": "customer", "translation": "покупатель", "example": "The customer is happy."},
        ],
        "B2": [
            {"word": "bargain", "translation": "выгодная покупка", "example": "This was a bargain."},
            {"word": "refund", "translation": "возврат денег", "example": "I want a refund."},
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
            "errors": ["a breakfast", "is English", ""]
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

📈 *Адаптивный режим:*  
Я запоминаю твои ошибки и чаще даю темы, в которых ты ошибаешься.

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

@bot.callback_query_handler(func=lambda call: call.data.startswith("listening_"))
def handle_listening_level(call):
    user_id = call.from_user.id
    level = call.data.split("_")[1]
    topic = user_data[user_id]["current_topic"]
    
    words_in_topic = WORD_BASE.get(topic, {}).get(level, [])
    if not words_in_topic:
        bot.send_message(call.message.chat.id, "😕 Для этой темы и уровня пока нет слов. Попробуй другую тему или уровень.")
        return
    
    word_data = random.choice(words_in_topic)
    user_data[user_id]["current_word_data"] = word_data
    
    audio_file = generate_audio(word_data["word"])
    with open(audio_file, 'rb') as f:
        bot.send_voice(call.message.chat.id, f)
    os.unlink(audio_file)
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("❓ Не знаю"), types.KeyboardButton("➕ В словарь"))
    markup.add(types.KeyboardButton("🔙 Главное меню"))
    
    bot.send_message(
        call.message.chat.id, 
        f"📝 Напиши это слово и его перевод (например: {word_data['word']} — {word_data['translation']})",
        reply_markup=markup
    )

def generate_audio(word):
    tts = gTTS(text=word, lang='en')
    filename = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3').name
    tts.save(filename)
    return filename

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
    
    elif text == "➕ В словарь":
        if word_data["word"] not in user_data[user_id]["vocabulary"]:
            user_data[user_id]["vocabulary"].append({
                "word": word_data["word"],
                "translation": word_data["translation"],
                "example": word_data["example"],
                "topic": user_data[user_id]["current_topic"]
            })
            bot.send_message(message.chat.id, f"✅ Слово *{word_data['word']}* добавлено в словарь", parse_mode="Markdown")
        else:
            bot.send_message(message.chat.id, "ℹ️ Это слово уже в словаре")

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
    bot.send_message(call.message.chat.id, "Говори...")

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
    bot.send_message(call.message.chat.id, "Говори...")

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
        text += f"\n💡 Чаще всего ты ошибаешься в теме *{most_common}*. Хочешь потренировать её?"
    
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