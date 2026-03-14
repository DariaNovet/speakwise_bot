import telebot
import random
from telebot import types

# ========== НАСТРОЙКИ ==========
TOKEN = "8616377232:AAGfTmBBylfJiR92lO_u4Fm1gDN9sFFxlVA"
bot = telebot.TeleBot(TOKEN)

# ========== БАЗА ДАННЫХ ПОЛЬЗОВАТЕЛЕЙ ==========
user_data = {}

# ========== ТЕМЫ ==========
TOPICS = ["food", "family", "travel", "daily routines", "hobby", "work", "education"]
LEVELS = ["A1", "A2"]

# ========== БАЗА СЛОВ ==========
WORD_BASE = {
    "food": {
        "A1": [
            {"word": "apple", "translation": "яблоко"},
            {"word": "banana", "translation": "банан"},
            {"word": "bread", "translation": "хлеб"},
            {"word": "milk", "translation": "молоко"},
            {"word": "egg", "translation": "яйцо"},
        ],
        "A2": [
            {"word": "beverage", "translation": "напиток"},
            {"word": "recipe", "translation": "рецепт"},
            {"word": "ingredient", "translation": "ингредиент"},
        ]
    },
    "family": {
        "A1": [
            {"word": "mother", "translation": "мама"},
            {"word": "father", "translation": "папа"},
            {"word": "brother", "translation": "брат"},
            {"word": "sister", "translation": "сестра"},
            {"word": "son", "translation": "сын"},
        ],
        "A2": [
            {"word": "aunt", "translation": "тётя"},
            {"word": "uncle", "translation": "дядя"},
            {"word": "cousin", "translation": "двоюродный брат/сестра"},
        ]
    },
    "travel": {
        "A1": [
            {"word": "hotel", "translation": "отель"},
            {"word": "plane", "translation": "самолёт"},
            {"word": "ticket", "translation": "билет"},
            {"word": "train", "translation": "поезд"},
            {"word": "bus", "translation": "автобус"},
        ],
        "A2": [
            {"word": "luggage", "translation": "багаж"},
            {"word": "passport", "translation": "паспорт"},
            {"word": "tourist", "translation": "турист"},
        ]
    },
    "daily routines": {
        "A1": [
            {"word": "wake up", "translation": "просыпаться"},
            {"word": "breakfast", "translation": "завтрак"},
            {"word": "work", "translation": "работа"},
            {"word": "sleep", "translation": "спать"},
            {"word": "shower", "translation": "душ"},
        ],
        "A2": [
            {"word": "routine", "translation": "распорядок"},
            {"word": "schedule", "translation": "расписание"},
            {"word": "habit", "translation": "привычка"},
        ]
    },
    "hobby": {
        "A1": [
            {"word": "music", "translation": "музыка"},
            {"word": "sport", "translation": "спорт"},
            {"word": "game", "translation": "игра"},
            {"word": "draw", "translation": "рисовать"},
            {"word": "read", "translation": "читать"},
        ],
        "A2": [
            {"word": "photography", "translation": "фотография"},
            {"word": "gardening", "translation": "садоводство"},
            {"word": "collection", "translation": "коллекция"},
        ]
    },
    "work": {
        "A1": [
            {"word": "job", "translation": "работа"},
            {"word": "office", "translation": "офис"},
            {"word": "boss", "translation": "начальник"},
            {"word": "colleague", "translation": "коллега"},
            {"word": "salary", "translation": "зарплата"},
        ],
        "A2": [
            {"word": "employee", "translation": "сотрудник"},
            {"word": "employer", "translation": "работодатель"},
            {"word": "deadline", "translation": "срок"},
        ]
    },
    "education": {
        "A1": [
            {"word": "school", "translation": "школа"},
            {"word": "teacher", "translation": "учитель"},
            {"word": "student", "translation": "ученик"},
            {"word": "book", "translation": "книга"},
            {"word": "pen", "translation": "ручка"},
        ],
        "A2": [
            {"word": "university", "translation": "университет"},
            {"word": "degree", "translation": "степень"},
            {"word": "homework", "translation": "домашнее задание"},
        ]
    }
}

# ========== БАЗА ГРАММАТИЧЕСКИХ ОШИБОК ==========
GRAMMAR_MISTAKES = {
    "A1": [
        {"wrong": "He go to school", "correct": "He goes to school", "explanation": "После he нужно добавлять -es к глаголу"},
        {"wrong": "She don't like coffee", "correct": "She doesn't like coffee", "explanation": "С she используется doesn't"},
        {"wrong": "They was happy", "correct": "They were happy", "explanation": "С they используется were"},
    ],
    "A2": [
        {"wrong": "I have went", "correct": "I have gone", "explanation": "После have используется третья форма глагола"},
        {"wrong": "She can to sing", "correct": "She can sing", "explanation": "После can не ставится to"},
    ]
}

# ========== БАЗА ТЕКСТОВ С ОШИБКАМИ ==========
TEXTS_WITH_ERRORS = {
    "A1": [
        {
            "title": "My Day",
            "wrong": "Every day I wake up at 7 o'clock. I have a breakfast. I go to school. My favorite subject is English.",
            "correct": "Every day I wake up at 7 o'clock. I have breakfast. I go to school. My favorite subject is English.",
            "errors": 1
        }
    ],
    "A2": [
        {
            "title": "Last Weekend",
            "wrong": "Last weekend I go to the park with my friends. We play football and then we eat ice cream.",
            "correct": "Last weekend I went to the park with my friends. We played football and then we ate ice cream.",
            "errors": 3
        }
    ]
}

# ========== ПРИВЕТСТВИЕ ==========
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    
    # Инициализация данных пользователя
    user_data[user_id] = {
        "vocabulary": [],
        "mistakes_count": {},
        "current_level": "A1",
        "current_topic": "food",
        "current_word": None,
        "current_mode": None
    }

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton("👂 Аудирование"),
        types.KeyboardButton("🧠 Грамматический детектив")
    )
    markup.add(types.KeyboardButton("📖 Текст с ошибками"))
    markup.add(
        types.KeyboardButton("📘 Мой словарь"),
        types.KeyboardButton("📊 Мои ошибки")
    )

    welcome_text = """
🎙️ *Добро пожаловать в твой личный тренажёр английского!*

Я помогу тебе прокачать английский шаг за шагом. Вот что я умею:

────────────────────
👂 *АУДИРОВАНИЕ*
• Ты выбираешь тему и уровень сложности
• Я присылаю слово голосом (скоро) или текстом
• Ты пишешь перевод
• Если ошибёшься — я покажу правильный ответ
• Незнакомые слова можно добавить в словарь

────────────────────
🧠 *ГРАММАТИЧЕСКИЙ ДЕТЕКТИВ*
• Я даю предложение с грамматической ошибкой
• Ты исправляешь его голосом или текстом
• Я проверяю и объясняю правило
• Отличная тренировка для начинающих

────────────────────
📖 *ТЕКСТ С ОШИБКАМИ*
• Я присылаю небольшой текст
• В нём спрятано 3 грамматические ошибки
• Твоя задача — прочитать текст вслух, исправляя ошибки
• Я проверю, все ли ошибки ты нашёл(ла)

────────────────────
📘 *МОЙ СЛОВАРЬ*
• Все слова, которые ты сохранил(а)
• Можно повторить в любое время

📊 *МОИ ОШИБКИ*
• Статистика по темам
• Помогает понять, что нужно подтянуть

────────────────────
⬇️ *Выбери режим ниже*
    """
    
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=markup)

# ========== ГЛАВНОЕ МЕНЮ ==========
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton("👂 Аудирование"),
        types.KeyboardButton("🧠 Грамматический детектив")
    )
    markup.add(types.KeyboardButton("📖 Текст с ошибками"))
    markup.add(
        types.KeyboardButton("📘 Мой словарь"),
        types.KeyboardButton("📊 Мои ошибки")
    )
    return markup

# ========== МЕНЮ ПОСЛЕ ЗАДАНИЯ ==========
def after_task_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("🔁 Продолжить"))
    markup.add(types.KeyboardButton("🏠 Главное меню"))
    return markup

# ========== АУДИРОВАНИЕ ==========
@bot.message_handler(func=lambda message: message.text == "👂 Аудирование")
def listening_mode(message):
    user_id = message.from_user.id
    user_data[user_id]["current_mode"] = "listening"
    
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
        bot.send_message(message.chat.id, "😕 Для этой темы пока нет слов. Попробуй другую.")
        return
    
    word_data = random.choice(words)
    user_data[user_id]["current_word"] = word_data
    
    bot.send_message(
        message.chat.id,
        f"🔤 Слово: *{word_data['word']}*\n\nНапиши его перевод:",
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda message: user_data.get(message.from_user.id, {}).get("current_mode") == "listening" and message.text not in ["🏠 Главное меню", "🔁 Продолжить", "👂 Аудирование", "🧠 Грамматический детектив", "📖 Текст с ошибками", "📘 Мой словарь", "📊 Мои ошибки"])
def check_translation(message):
    user_id = message.from_user.id
    word_data = user_data[user_id].get("current_word")
    
    if not word_data:
        return
    
    user_answer = message.text.strip().lower()
    correct = word_data["translation"].lower()
    
    if user_answer == correct:
        bot.send_message(
            message.chat.id,
            f"✅ *Верно!*\n\n{word_data['word']} — {word_data['translation']}",
            parse_mode="Markdown"
        )
    else:
        bot.send_message(
            message.chat.id,
            f"❌ *Ошибка*\n\nТы написала: {user_answer}\nПравильно: {correct}\n\nСлово: {word_data['word']} — {word_data['translation']}",
            parse_mode="Markdown"
        )
        # Увеличиваем счётчик ошибок
        topic = user_data[user_id]["current_topic"]
        user_data[user_id]["mistakes_count"][topic] = user_data[user_id]["mistakes_count"].get(topic, 0) + 1
    
    # Кнопка добавления в словарь
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("➕ В словарь"))
    markup.add(types.KeyboardButton("🔁 Продолжить"))
    markup.add(types.KeyboardButton("🏠 Главное меню"))
    
    bot.send_message(message.chat.id, "Что хочешь сделать?", reply_markup=markup)

# ========== ГРАММАТИЧЕСКИЙ ДЕТЕКТИВ ==========
@bot.message_handler(func=lambda message: message.text == "🧠 Грамматический детектив")
def grammar_detective_mode(message):
    user_id = message.from_user.id
    user_data[user_id]["current_mode"] = "grammar"
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for level in LEVELS:
        markup.add(types.KeyboardButton(f"🎯 {level}"))
    markup.add(types.KeyboardButton("🏠 Главное меню"))
    
    bot.send_message(message.chat.id, "🧠 *Грамматический детектив*\n\nВыбери уровень:", parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text.startswith("🎯 ") and user_data.get(message.from_user.id, {}).get("current_mode") == "grammar")
def handle_grammar_level(message):
    user_id = message.from_user.id
    level = message.text.replace("🎯 ", "")
    
    mistakes = GRAMMAR_MISTAKES.get(level, [])
    if not mistakes:
        bot.send_message(message.chat.id, "😕 Для этого уровня пока нет заданий.")
        return
    
    mistake = random.choice(mistakes)
    user_data[user_id]["current_mistake"] = mistake
    
    bot.send_message(
        message.chat.id,
        f"🧠 *Найди ошибку:*\n\n_{mistake['wrong']}_\n\nНапиши правильный вариант:",
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda message: user_data.get(message.from_user.id, {}).get("current_mode") == "grammar" and message.text not in ["🏠 Главное меню", "🔁 Продолжить", "👂 Аудирование", "🧠 Грамматический детектив", "📖 Текст с ошибками", "📘 Мой словарь", "📊 Мои ошибки"])
def check_grammar(message):
    user_id = message.from_user.id
    mistake = user_data[user_id].get("current_mistake")
    
    if not mistake:
        return
    
    user_answer = message.text.strip()
    
    if user_answer.lower() == mistake["correct"].lower():
        bot.send_message(
            message.chat.id,
            f"✅ *Верно!*\n\n{mistake['correct']}",
            parse_mode="Markdown"
        )
    else:
        bot.send_message(
            message.chat.id,
            f"❌ *Ошибка*\n\nПравильно: {mistake['correct']}\n\n{mistake['explanation']}",
            parse_mode="Markdown"
        )
    
    bot.send_message(message.chat.id, "Что хочешь сделать дальше?", reply_markup=after_task_menu())

# ========== ТЕКСТ С ОШИБКАМИ ==========
@bot.message_handler(func=lambda message: message.text == "📖 Текст с ошибками")
def text_errors_mode(message):
    user_id = message.from_user.id
    user_data[user_id]["current_mode"] = "text"
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for level in LEVELS:
        markup.add(types.KeyboardButton(f"🎯 {level}"))
    markup.add(types.KeyboardButton("🏠 Главное меню"))
    
    bot.send_message(message.chat.id, "📖 *Текст с ошибками*\n\nВыбери уровень:", parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text.startswith("🎯 ") and user_data.get(message.from_user.id, {}).get("current_mode") == "text")
def handle_text_level(message):
    user_id = message.from_user.id
    level = message.text.replace("🎯 ", "")
    
    texts = TEXTS_WITH_ERRORS.get(level, [])
    if not texts:
        bot.send_message(message.chat.id, "😕 Для этого уровня пока нет текстов.")
        return
    
    text_data = random.choice(texts)
    user_data[user_id]["current_text"] = text_data
    
    bot.send_message(
        message.chat.id,
        f"📖 *{text_data['title']}*\n\n{text_data['wrong']}\n\nНапиши исправленный текст:",
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda message: user_data.get(message.from_user.id, {}).get("current_mode") == "text" and message.text not in ["🏠 Главное меню", "🔁 Продолжить", "👂 Аудирование", "🧠 Грамматический детектив", "📖 Текст с ошибками", "📘 Мой словарь", "📊 Мои ошибки"])
def check_text(message):
    user_id = message.from_user.id
    text_data = user_data[user_id].get("current_text")
    
    if not text_data:
        return
    
    # Простая проверка (для демо)
    if message.text.strip() == text_data["correct"]:
        bot.send_message(message.chat.id, "✅ *Отлично!* Ты исправил(а) все ошибки.", parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, f"❌ *Не все ошибки исправлены*\n\nПравильный вариант:\n{text_data['correct']}", parse_mode="Markdown")
    
    bot.send_message(message.chat.id, "Что хочешь сделать дальше?", reply_markup=after_task_menu())

# ========== МОЙ СЛОВАРЬ ==========
@bot.message_handler(func=lambda message: message.text == "📘 Мой словарь")
def my_vocabulary(message):
    user_id = message.from_user.id
    vocab = user_data[user_id]["vocabulary"]
    
    if not vocab:
        bot.send_message(message.chat.id, "📘 В словаре пока пусто. Добавляй слова с помощью кнопки «➕ В словарь»")
    else:
        text = "📘 *Твой словарь:*\n\n"
        for item in vocab:
            text += f"• {item['word']} — {item['translation']}\n"
        bot.send_message(message.chat.id, text, parse_mode="Markdown")
    
    bot.send_message(message.chat.id, "Выбери действие:", reply_markup=main_menu())

# ========== МОИ ОШИБКИ ==========
@bot.message_handler(func=lambda message: message.text == "📊 Мои ошибки")
def my_mistakes(message):
    user_id = message.from_user.id
    mistakes = user_data[user_id]["mistakes_count"]
    
    if not mistakes:
        bot.send_message(message.chat.id, "📊 У тебя пока нет ошибок. Так держать!")
    else:
        text = "📊 *Твои ошибки по темам:*\n\n"
        for topic, count in mistakes.items():
            text += f"• {topic}: {count}\n"
        bot.send_message(message.chat.id, text, parse_mode="Markdown")
    
    bot.send_message(message.chat.id, "Выбери действие:", reply_markup=main_menu())

# ========== ДОБАВЛЕНИЕ В СЛОВАРЬ ==========
@bot.message_handler(func=lambda message: message.text == "➕ В словарь")
def add_to_vocabulary(message):
    user_id = message.from_user.id
    word_data = user_data[user_id].get("current_word")
    
    if word_data and word_data not in user_data[user_id]["vocabulary"]:
        user_data[user_id]["vocabulary"].append(word_data)
        bot.send_message(message.chat.id, f"✅ Слово *{word_data['word']}* добавлено в словарь", parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, "ℹ️ Это слово уже в словаре")
    
    bot.send_message(message.chat.id, "Что дальше?", reply_markup=after_task_menu())

# ========== ПРОДОЛЖИТЬ ==========
@bot.message_handler(func=lambda message: message.text == "🔁 Продолжить")
def continue_mode(message):
    user_id = message.from_user.id
    mode = user_data[user_id].get("current_mode")
    
    if mode == "listening":
        # Повторяем последний запрос
        topic = user_data[user_id]["current_topic"]
        level = user_data[user_id]["current_level"]
        words = WORD_BASE.get(topic, {}).get(level, [])
        if words:
            word_data = random.choice(words)
            user_data[user_id]["current_word"] = word_data
            bot.send_message(
                message.chat.id,
                f"🔤 Слово: *{word_data['word']}*\n\nНапиши его перевод:",
                parse_mode="Markdown"
            )
    elif mode == "grammar":
        grammar_detective_mode(message)
    elif mode == "text":
        text_errors_mode(message)

# ========== ГЛАВНОЕ МЕНЮ ==========
@bot.message_handler(func=lambda message: message.text == "🏠 Главное меню")
def back_to_main(message):
    send_welcome(message)

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    print("✅ БОТ ЗАПУЩЕН")
    bot.polling(none_stop=True)