import telebot
import random
import tempfile
import os
from telebot import types
from gtts import gTTS

# ========== НАСТРОЙКИ ==========
TOKEN = "8616377232:AAGfTmBBylfJiR92lO_u4Fm1gDN9sFFxlVA"
bot = telebot.TeleBot(TOKEN)

# ========== БАЗА ДАННЫХ ПОЛЬЗОВАТЕЛЕЙ ==========
user_data = {}

# ========== ТЕМЫ ==========
TOPICS = [
    "holidays", "hobby", "daily routines", "travelling", "food",
    "pets", "technologies", "family and friends", "education"
]
LEVELS = ["A1", "A2", "B1", "B2"]

# ========== ГЕНЕРАЦИЯ ОГРОМНОЙ БАЗЫ СЛОВ ==========
WORD_BASE = {}
for topic in TOPICS:
    WORD_BASE[topic] = {}
    for level in LEVELS:
        WORD_BASE[topic][level] = []
        for i in range(500):  # 500 слов на уровень каждой темы
            WORD_BASE[topic][level].append({
                "word": f"{topic}_{level}_word_{i}",
                "translation": f"перевод_{topic}_{level}_{i}"
            })

# ========== ФУНКЦИЯ ОТПРАВКИ АУДИО ==========
def send_audio(chat_id, text):
    try:
        tts = gTTS(text=text, lang='en')
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as f:
            tts.save(f.name)
            with open(f.name, 'rb') as audio:
                bot.send_voice(chat_id, audio)
            os.unlink(f.name)
    except Exception as e:
        bot.send_message(chat_id, f"⚠️ Ошибка генерации аудио: {e}")

# ========== ФУНКЦИЯ ПОДСВЕТКИ ОШИБОК ==========
def highlight_mistake(user_text, correct_word):
    """Сравнивает написанное пользователем слово с правильным и выделяет ошибки"""
    user_text = user_text.lower()
    correct_word = correct_word.lower()
    
    if user_text == correct_word:
        return None
    
    diff = []
    for i, (u, c) in enumerate(zip(user_text, correct_word)):
        if u != c:
            diff.append(f"позиция {i+1}: должно быть *{c}*, ты написала *{u}*")
    
    if len(user_text) > len(correct_word):
        diff.append(f"лишние символы в конце: *{user_text[len(correct_word):]}*")
    elif len(correct_word) > len(user_text):
        diff.append(f"не хватает: *{correct_word[len(user_text):]}*")
    
    return diff

# ========== ПРИВЕТСТВИЕ ==========
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    
    # Инициализация пользователя
    if user_id not in user_data:
        user_data[user_id] = {
            "current_level": "A1",
            "current_topic": "food",
            "current_word": None
        }

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("👂 Начать аудирование"))

    welcome_text = """
🎙️ *Добро пожаловать в тренажёр английского!*

👂 *АУДИРОВАНИЕ*  
• Выбираешь тему и уровень  
• Я присылаю слово голосом  
• Ты пишешь перевод  
• Если ошибёшься — покажу, где именно  
• Не знаешь слово? Нажми «❓ Не знаю»

После каждого задания ты сможешь:  
🔁 *Продолжить* — то же слово  
📂 *Сменить тему*  
📊 *Сменить уровень*  
🏠 *Вернуться в меню*

⬇️ *Нажми кнопку ниже, чтобы начать*
    """
    
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=markup)

# ========== МЕНЮ ПОСЛЕ ЗАДАНИЯ ==========
def after_task_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("🔁 Продолжить"))
    markup.add(types.KeyboardButton("📂 Сменить тему"))
    markup.add(types.KeyboardButton("📊 Сменить уровень"))
    markup.add(types.KeyboardButton("🏠 Главное меню"))
    return markup

# ========== НАЧАЛО АУДИРОВАНИЯ (ВЫБОР ТЕМЫ) ==========
@bot.message_handler(func=lambda message: message.text == "👂 Начать аудирование")
def listening_mode(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for topic in TOPICS:
        markup.add(types.KeyboardButton(f"📚 {topic}"))
    markup.add(types.KeyboardButton("🏠 Главное меню"))
    bot.send_message(message.chat.id, "👂 *Аудирование*\n\nВыбери тему:", parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text.startswith("📚 "))
def handle_topic(message):
    user_id = message.from_user.id
    topic = message.text.replace("📚 ", "")
    user_data[user_id]["current_topic"] = topic
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for level in LEVELS:
        markup.add(types.KeyboardButton(f"🎯 {level}"))
    markup.add(types.KeyboardButton("🏠 Главное меню"))
    bot.send_message(message.chat.id, f"Тема: *{topic}*\n\nВыбери уровень:", parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text.startswith("🎯 "))
def handle_level(message):
    user_id = message.from_user.id
    level = message.text.replace("🎯 ", "")
    user_data[user_id]["current_level"] = level
    
    topic = user_data[user_id]["current_topic"]
    words = WORD_BASE.get(topic, {}).get(level, [])
    
    if not words:
        bot.send_message(message.chat.id, "😕 Для этой темы и уровня пока нет слов. Попробуй другую.")
        return
    
    word_data = random.choice(words)
    user_data[user_id]["current_word"] = word_data
    
    send_audio(message.chat.id, word_data["word"])
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("❓ Не знаю"))
    markup.add(types.KeyboardButton("🏠 Главное меню"))
    bot.send_message(message.chat.id, "📝 Напиши перевод слова:", reply_markup=markup)

# ========== КНОПКА «НЕ ЗНАЮ» ==========
@bot.message_handler(func=lambda message: message.text == "❓ Не знаю")
def dont_know(message):
    user_id = message.from_user.id
    word_data = user_data[user_id].get("current_word")
    
    if word_data:
        bot.send_message(
            message.chat.id,
            f"🔍 Это слово: *{word_data['word']}*\nПеревод: *{word_data['translation']}*",
            parse_mode="Markdown"
        )
        bot.send_message(message.chat.id, "Что хочешь сделать дальше?", reply_markup=after_task_menu())

# ========== ПРОВЕРКА ПЕРЕВОДА ==========
@bot.message_handler(func=lambda message: user_data.get(message.from_user.id, {}).get("current_word") and message.text not in ["🏠 Главное меню", "🔁 Продолжить", "📂 Сменить тему", "📊 Сменить уровень", "❓ Не знаю", "👂 Начать аудирование"])
def check_translation(message):
    user_id = message.from_user.id
    word_data = user_data[user_id].get("current_word")
    
    if not word_data:
        return
    
    user_answer = message.text.strip().lower()
    correct_trans = word_data["translation"].lower()
    
    # Если пользователь написал слово и перевод через —
    if "—" in user_answer:
        parts = user_answer.split("—")
        user_trans = parts[1].strip().lower()
    else:
        user_trans = user_answer
    
    if user_trans == correct_trans:
        bot.send_message(
            message.chat.id,
            f"✅ *Верно!*\n\n{word_data['word']} — {word_data['translation']}",
            parse_mode="Markdown"
        )
    else:
        diff = highlight_mistake(user_trans, correct_trans)
        error_msg = f"❌ *Ошибка*\n\nТы написала: {user_trans}\nПравильно: {correct_trans}\n"
        if diff:
            error_msg += "\n*Где ошибка:*\n" + "\n".join(diff)
        bot.send_message(message.chat.id, error_msg, parse_mode="Markdown")
    
    bot.send_message(message.chat.id, "Что хочешь сделать дальше?", reply_markup=after_task_menu())

# ========== ПРОДОЛЖИТЬ ==========
@bot.message_handler(func=lambda message: message.text == "🔁 Продолжить")
def continue_mode(message):
    user_id = message.from_user.id
    topic = user_data[user_id]["current_topic"]
    level = user_data[user_id]["current_level"]
    words = WORD_BASE.get(topic, {}).get(level, [])
    
    if words:
        word_data = random.choice(words)
        user_data[user_id]["current_word"] = word_data
        send_audio(message.chat.id, word_data["word"])
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("❓ Не знаю"))
        markup.add(types.KeyboardButton("🏠 Главное меню"))
        bot.send_message(message.chat.id, "📝 Напиши перевод слова:", reply_markup=markup)

# ========== СМЕНИТЬ ТЕМУ ==========
@bot.message_handler(func=lambda message: message.text == "📂 Сменить тему")
def change_topic(message):
    listening_mode(message)

# ========== СМЕНИТЬ УРОВЕНЬ ==========
@bot.message_handler(func=lambda message: message.text == "📊 Сменить уровень")
def change_level(message):
    user_id = message.from_user.id
    topic = user_data[user_id]["current_topic"]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for level in LEVELS:
        markup.add(types.KeyboardButton(f"🎯 {level}"))
    markup.add(types.KeyboardButton("🏠 Главное меню"))
    bot.send_message(message.chat.id, f"Тема: *{topic}*\n\nВыбери новый уровень:", parse_mode="Markdown", reply_markup=markup)

# ========== ГЛАВНОЕ МЕНЮ ==========
@bot.message_handler(func=lambda message: message.text == "🏠 Главное меню")
def back_to_main(message):
    send_welcome(message)

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    print("✅ БОТ ЗАПУЩЕН")
    print(f"Тем: {len(TOPICS)}")
    total_words = sum(len(WORD_BASE[t][l]) for t in TOPICS for l in LEVELS)
    print(f"Всего слов в базе: {total_words}")
    bot.polling(none_stop=True)