import telebot
import random
from telebot import types
from gtts import gTTS
import tempfile
import os
from fpdf import FPDF

# ========== НАСТРОЙКИ ==========
TOKEN = "8616377232:AAGfTmBBylfJiR92lO_u4Fm1gDN9sFFxlVA"
bot = telebot.TeleBot(TOKEN)

# ========== ДАННЫЕ ПОЛЬЗОВАТЕЛЕЙ ==========
user_data = {}

# ========== ТЕМЫ И УРОВНИ ==========
TOPICS = ["food", "family", "travel", "daily routines", "hobby", "work", "education"]
LEVELS = ["A1", "A2", "B1", "B2"]

# ========== БАЗА СЛОВ (500+ НА ТЕМУ) ==========
WORD_BASE = {}
for topic in TOPICS:
    WORD_BASE[topic] = {}
    for level in LEVELS:
        WORD_BASE[topic][level] = []
        for i in range(500):
            WORD_BASE[topic][level].append({
                "word": f"word_{topic}_{level}_{i}",
                "translation": f"перевод_{topic}_{level}_{i}"
            })

# ========== ГРАММАТИКА ==========
GRAMMAR_MISTAKES = {
    "A1": [
        {"wrong": "He go to school", "correct": "He goes to school", "explanation": "После he нужно -es"},
        {"wrong": "She don't like coffee", "correct": "She doesn't like coffee", "explanation": "С she используется doesn't"},
    ],
    "A2": [
        {"wrong": "I have went", "correct": "I have gone", "explanation": "После have третья форма"},
    ],
    "B1": [
        {"wrong": "If I will see him", "correct": "If I see him", "explanation": "После if не will"},
    ],
    "B2": [
        {"wrong": "She suggested me to go", "correct": "She suggested that I go", "explanation": "После suggest не to"},
    ]
}

# ========== ТЕКСТЫ ==========
TEXTS = {
    "A1": "Every day I wake up at 7 o'clock. I have a breakfast. I go to school. My favorite subject is English. I like it very much. After school I play with my friends. We play football. Then I do my homework. In the evening I watch TV. I go to bed at 10 o'clock.",
    "A2": "Last summer I go to the beach with my family. We swim in the sea. The weather was very hot. I eat ice cream every day. In the evenings we walk along the shore. We see beautiful sunsets. I take many photos. My sister collect shells. We was very happy.",
    "B1": "Many people is concerned about the environment. They think that we should to do more to protect nature. Recycling is one way to help. Also, we should using less plastic. The government need to create new laws. Companies must to reduce pollution.",
    "B2": "Technology have changed our lives dramatically. People can to communicate instantly across the globe. However, there is also disadvantages. Many people spend too much time on their phones. This affect their relationships. Social media can causing anxiety."
}

# ========== АУДИО ==========
def send_audio(chat_id, text):
    tts = gTTS(text=text, lang='en')
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as f:
        tts.save(f.name)
        with open(f.name, 'rb') as audio:
            bot.send_voice(chat_id, audio)
        os.unlink(f.name)

# ========== СТАРТ ==========
@bot.message_handler(commands=['start'])
def start(message):
    uid = message.from_user.id
    user_data[uid] = {
        "vocab": [],
        "mistakes": {},
        "level": "A1",
        "topic": "food",
        "word": None,
        "grammar": None,
        "mode": None
    }
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("👂 Аудирование", "🧠 Грамматика")
    markup.add("📖 Текст", "📘 Словарь")
    markup.add("📊 Ошибки", "📄 PDF")
    
    bot.send_message(chat_id, "Выбери режим:", reply_markup=markup)

# ========== АУДИРОВАНИЕ ==========
@bot.message_handler(func=lambda m: m.text == "👂 Аудирование")
def audio_mode(m):
    uid = m.from_user.id
    user_data[uid]["mode"] = "audio"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for t in TOPICS:
        markup.add(t)
    markup.add("🏠 Главное меню")
    bot.send_message(m.chat.id, "Выбери тему:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in TOPICS)
def audio_topic(m):
    uid = m.from_user.id
    user_data[uid]["topic"] = m.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for l in LEVELS:
        markup.add(l)
    markup.add("🏠 Главное меню")
    bot.send_message(m.chat.id, "Выбери уровень:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in LEVELS)
def audio_level(m):
    uid = m.from_user.id
    user_data[uid]["level"] = m.text
    topic = user_data[uid]["topic"]
    level = user_data[uid]["level"]
    
    words = WORD_BASE[topic][level]
    word = random.choice(words)
    user_data[uid]["word"] = word
    
    send_audio(m.chat.id, word["word"])
    bot.send_message(m.chat.id, f"Напиши перевод слова {word['word']}")

@bot.message_handler(func=lambda m: user_data.get(m.from_user.id, {}).get("mode") == "audio" and m.text not in ["🏠 Главное меню", "➕ В словарь"])
def check_translation(m):
    uid = m.from_user.id
    word = user_data[uid]["word"]
    if m.text.lower() == word["translation"].lower():
        bot.send_message(m.chat.id, "✅ Верно!")
    else:
        bot.send_message(m.chat.id, f"❌ Ошибка! Правильно: {word['translation']}")
        user_data[uid]["mistakes"][word["word"]] = user_data[uid]["mistakes"].get(word["word"], 0) + 1
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🔁 Продолжить", "➕ В словарь", "🏠 Главное меню")
    bot.send_message(m.chat.id, "Что дальше?", reply_markup=markup)

# ========== ГРАММАТИКА ==========
@bot.message_handler(func=lambda m: m.text == "🧠 Грамматика")
def grammar_mode(m):
    uid = m.from_user.id
    user_data[uid]["mode"] = "grammar"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for l in LEVELS:
        markup.add(l)
    markup.add("🏠 Главное меню")
    bot.send_message(m.chat.id, "Выбери уровень:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in LEVELS and user_data.get(m.from_user.id, {}).get("mode") == "grammar")
def grammar_level(m):
    uid = m.from_user.id
    level = m.text
    mistakes = GRAMMAR_MISTAKES[level]
    mistake = random.choice(mistakes)
    user_data[uid]["grammar"] = mistake
    
    bot.send_message(m.chat.id, f"Исправь ошибку:\n{mistake['wrong']}\n\nОтправь голосовое с правильным вариантом")

# ========== ТЕКСТ ==========
@bot.message_handler(func=lambda m: m.text == "📖 Текст")
def text_mode(m):
    uid = m.from_user.id
    user_data[uid]["mode"] = "text"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for l in LEVELS:
        markup.add(l)
    markup.add("🏠 Главное меню")
    bot.send_message(m.chat.id, "Выбери уровень:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in LEVELS and user_data.get(m.from_user.id, {}).get("mode") == "text")
def text_level(m):
    uid = m.from_user.id
    level = m.text
    text = TEXTS[level]
    bot.send_message(m.chat.id, f"Текст с ошибками:\n{text}\n\nПрочитай его вслух, исправляя ошибки")

# ========== СЛОВАРЬ ==========
@bot.message_handler(func=lambda m: m.text == "📘 Словарь")
def show_vocab(m):
    uid = m.from_user.id
    vocab = user_data[uid]["vocab"]
    if not vocab:
        bot.send_message(m.chat.id, "Словарь пуст")
    else:
        text = "\n".join([f"{v['word']} - {v['translation']}" for v in vocab])
        bot.send_message(m.chat.id, f"Твой словарь:\n{text}")

@bot.message_handler(func=lambda m: m.text == "➕ В словарь")
def add_to_vocab(m):
    uid = m.from_user.id
    word = user_data[uid].get("word")
    if word and word not in user_data[uid]["vocab"]:
        user_data[uid]["vocab"].append(word)
        bot.send_message(m.chat.id, f"✅ {word['word']} добавлено")

# ========== ОШИБКИ ==========
@bot.message_handler(func=lambda m: m.text == "📊 Ошибки")
def show_mistakes(m):
    uid = m.from_user.id
    mistakes = user_data[uid]["mistakes"]
    if not mistakes:
        bot.send_message(m.chat.id, "Ошибок нет")
    else:
        text = "\n".join([f"{k}: {v}" for k, v in mistakes.items()])
        bot.send_message(m.chat.id, f"Твои ошибки:\n{text}")

# ========== PDF ==========
@bot.message_handler(func=lambda m: m.text == "📄 PDF")
def make_pdf(m):
    uid = m.from_user.id
    vocab = user_data[uid]["vocab"]
    if not vocab:
        bot.send_message(m.chat.id, "Словарь пуст")
        return
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "Мой словарь", ln=True)
    for v in vocab:
        pdf.cell(200, 10, f"{v['word']} - {v['translation']}", ln=True)
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as f:
        pdf.output(f.name)
        with open(f.name, 'rb') as doc:
            bot.send_document(m.chat.id, doc)
        os.unlink(f.name)

# ========== ПРОДОЛЖИТЬ ==========
@bot.message_handler(func=lambda m: m.text == "🔁 Продолжить")
def cont(m):
    uid = m.from_user.id
    mode = user_data[uid]["mode"]
    if mode == "audio":
        topic = user_data[uid]["topic"]
        level = user_data[uid]["level"]
        word = random.choice(WORD_BASE[topic][level])
        user_data[uid]["word"] = word
        send_audio(m.chat.id, word["word"])
        bot.send_message(m.chat.id, f"Напиши перевод слова {word['word']}")
    elif mode == "grammar":
        level = user_data[uid]["level"]
        mistake = random.choice(GRAMMAR_MISTAKES[level])
        user_data[uid]["grammar"] = mistake
        bot.send_message(m.chat.id, f"Исправь ошибку:\n{mistake['wrong']}")
    elif mode == "text":
        level = user_data[uid]["level"]
        bot.send_message(m.chat.id, TEXTS[level])

# ========== ГЛАВНОЕ МЕНЮ ==========
@bot.message_handler(func=lambda m: m.text == "🏠 Главное меню")
def main_menu(m):
    start(m)

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    print("✅ Бот работает")
    bot.polling()