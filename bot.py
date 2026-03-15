import telebot
import random
import tempfile
import os
from telebot import types
from gtts import gTTS
from fpdf import FPDF

# ========== НАСТРОЙКИ ==========
TOKEN = "8616377232:AAGfTmBBylfJiR92lO_u4Fm1gDN9sFFxlVA"
bot = telebot.TeleBot(TOKEN)

# ========== БАЗА ДАННЫХ ПОЛЬЗОВАТЕЛЕЙ ==========
user_data = {}

# ========== ТЕМЫ И УРОВНИ ==========
TOPICS = [
    "holidays", "hobby", "daily routines", "travelling", "food",
    "pets", "technologies", "family and friends", "education",
    "work", "health", "sports", "nature", "shopping", "movies"
]
LEVELS = ["A1", "A2", "B1", "B2"]

# ========== ГЕНЕРАЦИЯ БАЗЫ СЛОВ (500+ НА ТЕМУ) ==========
WORD_BASE = {}
for topic in TOPICS:
    WORD_BASE[topic] = {}
    for level in LEVELS:
        WORD_BASE[topic][level] = []
        for i in range(500):
            WORD_BASE[topic][level].append({
                "word": f"{topic}_{level}_word_{i}",
                "translation": f"перевод_{topic}_{level}_{i}"
            })

# ========== БАЗА ГРАММАТИЧЕСКИХ ОШИБОК ==========
GRAMMAR_BASE = {
    "A1": [
        {"wrong": "He go to school", "correct": "He goes to school", 
         "explanation": "После he нужно добавлять окончание -es (go → goes)"},
        {"wrong": "She don't like coffee", "correct": "She doesn't like coffee", 
         "explanation": "В отрицаниях с she / he / it используется doesn't + глагол без окончания"},
        {"wrong": "They was happy", "correct": "They were happy", 
         "explanation": "С they всегда используется were, даже в Past Simple"},
        {"wrong": "I is a student", "correct": "I am a student", 
         "explanation": "С местоимением I используется только глагол am"},
        {"wrong": "You was late", "correct": "You were late", 
         "explanation": "С you (ты / вы) всегда используется were"},
        {"wrong": "We has a car", "correct": "We have a car", 
         "explanation": "С we, they, I, you используется have, а не has"},
    ] * 30,
    "A2": [
        {"wrong": "I have went", "correct": "I have gone", 
         "explanation": "В Present Perfect после have / has используется третья форма глагола (go → gone)"},
        {"wrong": "She can to sing", "correct": "She can sing", 
         "explanation": "После модальных глаголов (can, must, should) частица to НЕ ставится"},
        {"wrong": "He didn't went", "correct": "He didn't go", 
         "explanation": "После вспомогательного глагола did (didn't) глагол ставится в начальную форму"},
        {"wrong": "I am go to school", "correct": "I am going to school", 
         "explanation": "Для выражения действия в процессе используется am/is/are + глагол с -ing"},
        {"wrong": "She have a dog", "correct": "She has a dog", 
         "explanation": "С he, she, it используется has (не have)"},
        {"wrong": "They is playing", "correct": "They are playing", 
         "explanation": "С they всегда используется are"},
    ] * 30,
    "B1": [
        {"wrong": "If I will see him", "correct": "If I see him", 
         "explanation": "В условных предложениях (if) после if НЕ используется will — ставится настоящее время"},
        {"wrong": "I am used to get up early", "correct": "I am used to getting up early", 
         "explanation": "Конструкция be used to требует после себя герундий (-ing)"},
        {"wrong": "She suggested me to go", "correct": "She suggested that I go / She suggested going", 
         "explanation": "После suggest НЕ используется инфинитив с to. Нужно: suggest + that + предложение или suggest + -ing"},
        {"wrong": "He told that he is tired", "correct": "He said that he was tired", 
         "explanation": "В косвенной речи время глагола обычно сдвигается назад (is → was)"},
        {"wrong": "I look forward to meet you", "correct": "I look forward to meeting you", 
         "explanation": "После look forward to всегда используется герундий (-ing)"},
    ] * 25,
    "B2": [
        {"wrong": "She is married with a doctor", "correct": "She is married to a doctor", 
         "explanation": "С глаголом married используется предлог to, а не with"},
        {"wrong": "I have been in London", "correct": "I have been to London", 
         "explanation": "Если вы были где-то и вернулись, используется have been to, а не in"},
        {"wrong": "He is afraid from dogs", "correct": "He is afraid of dogs", 
         "explanation": "Прилагательное afraid требует предлога of"},
        {"wrong": "She is interested about art", "correct": "She is interested in art", 
         "explanation": "Правильный предлог после interested — in"},
        {"wrong": "I depend from my parents", "correct": "I depend on my parents", 
         "explanation": "Глагол depend требует предлога on"},
    ] * 25
}

# ========== БАЗА ТЕКСТОВ С ОШИБКАМИ (10+ ПРЕДЛОЖЕНИЙ) ==========
TEXTS_WITH_ERRORS = {
    "A1": {
        "title": "My Daily Life",
        "text": "Every day I wake up at 7 o'clock. I have a breakfast. Then I go to school. My favorite subject is English. I like it very much. After school I play with my friends. We play football. Then I do my homework. In the evening I watch TV. I go to bed at 10 o'clock. I have a busy day. But I like my daily routine.",
        "errors": [
            {"wrong": "a breakfast", "correct": "breakfast", "position": 1}
        ]
    },
    "A2": {
        "title": "Last Summer",
        "text": "Last summer I go to the beach with my family. We swim in the sea. The weather was very hot. I eat ice cream every day. In the evenings we walk along the shore. We see beautiful sunsets. I take many photos. My sister collect shells. We was very happy. It was the best summer ever.",
        "errors": [
            {"wrong": "go", "correct": "went", "position": 1},
            {"wrong": "swim", "correct": "swam", "position": 2},
            {"wrong": "eat", "correct": "ate", "position": 4},
            {"wrong": "walk", "correct": "walked", "position": 5},
            {"wrong": "see", "correct": "saw", "position": 6},
            {"wrong": "take", "correct": "took", "position": 7},
            {"wrong": "collect", "correct": "collected", "position": 8},
            {"wrong": "was", "correct": "were", "position": 9}
        ]
    },
    "B1": {
        "title": "Environmental Problems",
        "text": "Many people is concerned about the environment. They think that we should to do more to protect nature. Recycling is one way to help. Also, we should using less plastic. The government need to create new laws. Companies must to reduce pollution. If we will not act now, the situation will become worse. Everyone can make a difference. We must to work together. The future of our planet depend on us.",
        "errors": [
            {"wrong": "is", "correct": "are", "position": 1},
            {"wrong": "should to", "correct": "should", "position": 2},
            {"wrong": "should using", "correct": "should use", "position": 4},
            {"wrong": "need", "correct": "needs", "position": 5},
            {"wrong": "must to", "correct": "must", "position": 6},
            {"wrong": "will not", "correct": "do not", "position": 7},
            {"wrong": "must to", "correct": "must", "position": 9},
            {"wrong": "depend", "correct": "depends", "position": 10}
        ]
    },
    "B2": {
        "title": "Technology and Society",
        "text": "Technology have changed our lives dramatically. People can to communicate instantly across the globe. However, there is also disadvantages. Many people spend too much time on their phones. This affect their relationships. Social media can causing anxiety and depression. Children should be monitor while using the internet. Parents must to set limits. If we will not address these issues, the problem will getting worse. We need find a balance between technology and real life.",
        "errors": [
            {"wrong": "have", "correct": "has", "position": 1},
            {"wrong": "can to", "correct": "can", "position": 2},
            {"wrong": "is", "correct": "are", "position": 3},
            {"wrong": "affect", "correct": "affects", "position": 5},
            {"wrong": "can causing", "correct": "can cause", "position": 6},
            {"wrong": "should be monitor", "correct": "should be monitored", "position": 7},
            {"wrong": "must to", "correct": "must", "position": 8},
            {"wrong": "will not", "correct": "do not", "position": 9},
            {"wrong": "will getting", "correct": "will get", "position": 9},
            {"wrong": "need find", "correct": "need to find", "position": 10}
        ]
    }
}

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
    
    # Поиск несовпадающих символов
    diff = []
    for i, (u, c) in enumerate(zip(user_text, correct_word)):
        if u != c:
            diff.append(f"позиция {i+1}: должно быть '{c}', ты написала '{u}'")
    
    if len(user_text) > len(correct_word):
        diff.append(f"лишние символы в конце: '{user_text[len(correct_word):]}'")
    elif len(correct_word) > len(user_text):
        diff.append(f"не хватает: '{correct_word[len(user_text):]}'")
    
    return diff

# ========== ПРИВЕТСТВИЕ ==========
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    
    # Инициализация пользователя
    if user_id not in user_data:
        user_data[user_id] = {
            "vocabulary": [],
            "mistakes_count": {},
            "grammar_mistakes": [],
            "current_level": "A1",
            "current_topic": "food",
            "current_word": None,
            "current_mistake": None,
            "current_text": None,
            "current_mode": None,
            "stats": {
                "total_attempts": 0,
                "correct": 0,
                "wrong": 0
            }
        }

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton("👂 Аудирование"),
        types.KeyboardButton("🧠 Грамматический детектив")
    )
    markup.add(types.KeyboardButton("📖 Текст с ошибками"))
    markup.add(
        types.KeyboardButton("📘 Мой словарь"),
        types.KeyboardButton("📊 Мои ошибки"),
        types.KeyboardButton("📄 Скачать PDF")
    )
    markup.add(types.KeyboardButton("🎯 Тренировка ошибок"))

    welcome_text = """
🎙️ *Добро пожаловать в твой персональный тренажёр английского!*

Я помогу тебе прокачать язык через интерактивные задания:

────────────────────
👂 *АУДИРОВАНИЕ*
• Выбираешь тему и уровень сложности
• Я присылаю слово голосом
• Ты пишешь перевод
• Если ошибёшься — я покажу, где именно
• Незнакомые слова можно сохранить в словарь

────────────────────
🧠 *ГРАММАТИЧЕСКИЙ ДЕТЕКТИВ*
• Я даю предложение с ошибкой
• Ты исправляешь его голосом
• Я проверяю и объясняю правило

────────────────────
📖 *ТЕКСТ С ОШИБКАМИ*
• Я присылаю текст с 3+ ошибками
• Ты читаешь его вслух, исправляя ошибки
• Я проверяю, все ли ошибки найдены

────────────────────
📘 *МОЙ СЛОВАРЬ*
• Все сохранённые слова
• Можно повторить в любое время

📊 *МОИ ОШИБКИ*
• Статистика по темам
• Анализ частых ошибок

📄 *СКАЧАТЬ PDF*
• Красивый словарь в формате PDF

🎯 *ТРЕНИРОВКА ОШИБОК*
• Индивидуальные упражнения на твои частые ошибки

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
        types.KeyboardButton("📊 Мои ошибки"),
        types.KeyboardButton("📄 Скачать PDF")
    )
    markup.add(types.KeyboardButton("🎯 Тренировка ошибок"))
    return markup

# ========== МЕНЮ ПОСЛЕ ЗАДАНИЯ ==========
def after_task_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("🔁 Продолжить"))
    markup.add(types.KeyboardButton("➕ В словарь"))
    markup.add(types.KeyboardButton("🏠 Главное меню"))
    return markup

# ========== МЕНЮ ВЫБОРА ТЕМЫ/УРОВНЯ ==========
def topic_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for topic in TOPICS[:8]:  # Показываем первые 8 тем
        markup.add(types.KeyboardButton(f"📚 {topic}"))
    markup.add(types.KeyboardButton("🏠 Главное меню"))
    return markup

def level_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for level in LEVELS:
        markup.add(types.KeyboardButton(f"🎯 {level}"))
    markup.add(types.KeyboardButton("🏠 Главное меню"))
    return markup

# ========== АУДИРОВАНИЕ ==========
@bot.message_handler(func=lambda message: message.text == "👂 Аудирование")
def listening_mode(message):
    user_id = message.from_user.id
    user_data[user_id]["current_mode"] = "listening"
    
    bot.send_message(
        message.chat.id, 
        "👂 *Аудирование*\n\nЯ пришлю слово голосом, а ты напиши его перевод.\nЕсли не знаешь — нажми «❓ Не знаю».\nМожно сохранить слово в словарь кнопкой «➕ В словарь».",
        parse_mode="Markdown",
        reply_markup=topic_menu()
    )

@bot.message_handler(func=lambda message: message.text.startswith("📚 "))
def handle_topic(message):
    user_id = message.from_user.id
    topic = message.text.replace("📚 ", "")
    user_data[user_id]["current_topic"] = topic
    
    bot.send_message(
        message.chat.id, 
        f"Тема: *{topic}*\n\nТеперь выбери уровень сложности:",
        parse_mode="Markdown",
        reply_markup=level_menu()
    )

@bot.message_handler(func=lambda message: message.text.startswith("🎯 "))
def handle_level(message):
    user_id = message.from_user.id
    level = message.text.replace("🎯 ", "")
    user_data[user_id]["current_level"] = level
    
    topic = user_data[user_id]["current_topic"]
    words = WORD_BASE.get(topic, {}).get(level, [])
    
    if not words:
        bot.send_message(
            message.chat.id, 
            "😕 Для этой темы и уровня пока нет слов. Попробуй другую тему.",
            reply_markup=topic_menu()
        )
        return
    
    word_data = random.choice(words)
    user_data[user_id]["current_word"] = word_data
    user_data[user_id]["stats"]["total_attempts"] += 1
    
    send_audio(message.chat.id, word_data["word"])
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("❓ Не знаю"))
    markup.add(types.KeyboardButton("🏠 Главное меню"))
    
    bot.send_message(
        message.chat.id,
        f"📝 Напиши перевод слова:",
        reply_markup=markup
    )

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
        
        # Предлагаем добавить в словарь
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("➕ В словарь"))
        markup.add(types.KeyboardButton("🔁 Продолжить"))
        markup.add(types.KeyboardButton("🏠 Главное меню"))
        bot.send_message(message.chat.id, "Хочешь добавить это слово в словарь?", reply_markup=markup)

@bot.message_handler(func=lambda message: user_data.get(message.from_user.id, {}).get("current_mode") == "listening" and message.text not in ["🏠 Главное меню", "🔁 Продолжить", "➕ В словарь", "❓ Не знаю"])
def check_translation(message):
    user_id = message.from_user.id
    word_data = user_data[user_id].get("current_word")
    
    if not word_data:
        return
    
    user_answer = message.text.strip().lower()
    correct_word = word_data["word"].lower()
    correct_trans = word_data["translation"].lower()
    
    # Проверяем, есть ли дефис (слово — перевод)
    if "—" in user_answer:
        parts = user_answer.split("—")
        user_word = parts[0].strip().lower()
        user_trans = parts[1].strip().lower()
    else:
        # Если пользователь написал только перевод
        user_trans = user_answer
        user_word = ""
    
    # Проверяем перевод
    if user_trans == correct_trans:
        bot.send_message(
            message.chat.id,
            f"✅ *Верно!*\n\n{word_data['word']} — {word_data['translation']}",
            parse_mode="Markdown"
        )
        user_data[user_id]["stats"]["correct"] += 1
    else:
        # Подсвечиваем ошибки
        if user_trans:
            diff = highlight_mistake(user_trans, correct_trans)
            error_msg = f"❌ *Ошибка в переводе*\n\nТы написала: {user_trans}\nПравильно: {correct_trans}\n"
            if diff:
                error_msg += "\n*Где ошибка:*\n" + "\n".join(diff)
            bot.send_message(message.chat.id, error_msg, parse_mode="Markdown")
        else:
            bot.send_message(
                message.chat.id,
                f"❌ *Ошибка*\n\nПравильный перевод: {correct_trans}",
                parse_mode="Markdown"
            )
        
        user_data[user_id]["stats"]["wrong"] += 1
        user_data[user_id]["mistakes_count"][word_data["word"]] = user_data[user_id]["mistakes_count"].get(word_data["word"], 0) + 1
    
    # Меню после ответа
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("🔁 Продолжить"))
    markup.add(types.KeyboardButton("➕ В словарь"))
    markup.add(types.KeyboardButton("🏠 Главное меню"))
    bot.send_message(message.chat.id, "Что хочешь сделать дальше?", reply_markup=markup)

# ========== ГРАММАТИЧЕСКИЙ ДЕТЕКТИВ ==========
@bot.message_handler(func=lambda message: message.text == "🧠 Грамматический детектив")
def grammar_mode(message):
    user_id = message.from_user.id
    user_data[user_id]["current_mode"] = "grammar"
    
    bot.send_message(
        message.chat.id,
        "🧠 *Грамматический детектив*\n\nЯ пришлю предложение с ошибкой.\nТвоя задача — сказать правильный вариант голосом.\nЯ проверю и объясню правило.",
        parse_mode="Markdown",
        reply_markup=level_menu()
    )

@bot.message_handler(func=lambda message: message.text.startswith("🎯 ") and user_data.get(message.from_user.id, {}).get("current_mode") == "grammar")
def handle_grammar_level(message):
    user_id = message.from_user.id
    level = message.text.replace("🎯 ", "")
    
    mistakes = GRAMMAR_BASE.get(level, [])
    if not mistakes:
        bot.send_message(message.chat.id, "😕 Для этого уровня пока нет заданий.", reply_markup=main_menu())
        return
    
    mistake = random.choice(mistakes)
    user_data[user_id]["current_mistake"] = mistake
    user_data[user_id]["grammar_mistakes"].append(mistake)
    
    bot.send_message(
        message.chat.id,
        f"*Найди и исправь ошибку:*\n\n_{mistake['wrong']}_\n\n🎤 Отправь голосовое сообщение с правильным вариантом",
        parse_mode="Markdown"
    )
    bot.send_message(message.chat.id, "После того как отправишь голосовое, я проверю.", reply_markup=after_task_menu())

# ========== ТЕКСТ С ОШИБКАМИ ==========
@bot.message_handler(func=lambda message: message.text == "📖 Текст с ошибками")
def text_mode(message):
    user_id = message.from_user.id
    user_data[user_id]["current_mode"] = "text"
    
    bot.send_message(
        message.chat.id,
        "📖 *Текст с ошибками*\n\nЯ пришлю текст с несколькими грамматическими ошибками.\nТвоя задача — прочитать его вслух, исправляя ошибки на лету.\nЯ проверю, все ли ошибки ты нашёл(ла).",
        parse_mode="Markdown",
        reply_markup=level_menu()
    )

@bot.message_handler(func=lambda message: message.text.startswith("🎯 ") and user_data.get(message.from_user.id, {}).get("current_mode") == "text")
def handle_text_level(message):
    user_id = message.from_user.id
    level = message.text.replace("🎯 ", "")
    
    text_data = TEXTS_WITH_ERRORS.get(level)
    if not text_data:
        bot.send_message(message.chat.id, "😕 Для этого уровня пока нет текстов.", reply_markup=main_menu())
        return
    
    user_data[user_id]["current_text"] = text_data
    
    bot.send_message(
        message.chat.id,
        f"📖 *{text_data['title']}*\n\n_{text_data['text']}_\n\n🎤 Прочитай этот текст вслух, исправляя ошибки",
        parse_mode="Markdown"
    )
    bot.send_message(message.chat.id, "После того как отправишь голосовое, я проверю.", reply_markup=after_task_menu())

# ========== МОЙ СЛОВАРЬ ==========
@bot.message_handler(func=lambda message: message.text == "📘 Мой словарь")
def show_vocabulary(message):
    user_id = message.from_user.id
    vocab = user_data[user_id]["vocabulary"]
    
    if not vocab:
        bot.send_message(message.chat.id, "📘 В словаре пока пусто. Добавляй слова с помощью кнопки «➕ В словарь»")
    else:
        text = "📘 *Твой словарь:*\n\n"
        for i, item in enumerate(vocab, 1):
            text += f"{i}. {item['word']} — {item['translation']}\n"
        
        # Отправляем частями, если много слов
        if len(text) > 4000:
            parts = [text[i:i+4000] for i in range(0, len(text), 4000)]
            for part in parts:
                bot.send_message(message.chat.id, part, parse_mode="Markdown")
        else:
            bot.send_message(message.chat.id, text, parse_mode="Markdown")
    
    bot.send_message(message.chat.id, "Выбери действие:", reply_markup=main_menu())

# ========== МОИ ОШИБКИ ==========
@bot.message_handler(func=lambda message: message.text == "📊 Мои ошибки")
def show_mistakes(message):
    user_id = message.from_user.id
    mistakes = user_data[user_id]["mistakes_count"]
    grammar_mistakes = user_data[user_id]["grammar_mistakes"]
    stats = user_data[user_id]["stats"]
    
    if not mistakes and not grammar_mistakes:
        bot.send_message(message.chat.id, "📊 У тебя пока нет ошибок. Так держать!")
    else:
        text = "📊 *Твоя статистика:*\n\n"
        text += f"Всего попыток: {stats['total_attempts']}\n"
        text += f"Правильно: {stats['correct']}\n"
        text += f"Ошибок: {stats['wrong']}\n\n"
        
        if mistakes:
            text += "*Частые ошибки в словах:*\n"
            sorted_mistakes = sorted(mistakes.items(), key=lambda x: x[1], reverse=True)[:5]
            for word, count in sorted_mistakes:
                text += f"• {word}: {count} раз(а)\n"
        
        if grammar_mistakes:
            text += "\n*Грамматические ошибки:*\n"
            # Группируем по типу ошибки
            grammar_types = {}
            for m in grammar_mistakes:
                key = m['explanation'][:30]  # Берём начало объяснения как ключ
                grammar_types[key] = grammar_types.get(key, 0) + 1
            
            for exp, count in list(grammar_types.items())[:3]:
                text += f"• {exp}...: {count} раз(а)\n"
        
        bot.send_message(message.chat.id, text, parse_mode="Markdown")
        
        # Предлагаем тренировку
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("🎯 Тренировка ошибок"))
        markup.add(types.KeyboardButton("🏠 Главное меню"))
        bot.send_message(message.chat.id, "Хочешь потренировать свои частые ошибки?", reply_markup=markup)

# ========== ТРЕНИРОВКА ОШИБОК ==========
@bot.message_handler(func=lambda message: message.text == "🎯 Тренировка ошибок")
def mistake_training(message):
    user_id = message.from_user.id
    mistakes = user_data[user_id]["mistakes_count"]
    
    if not mistakes:
        bot.send_message(message.chat.id, "🎯 У тебя пока нет частых ошибок для тренировки.")
        return
    
    # Берём самое частое ошибочное слово
    most_common = sorted(mistakes.items(), key=lambda x: x[1], reverse=True)[0][0]
    
    # Ищем это слово в базе
    found = None
    for topic in WORD_BASE:
        for level in WORD_BASE[topic]:
            for word in WORD_BASE[topic][level]:
                if word["word"] == most_common:
                    found = word
                    break
            if found:
                break
        if found:
            break
    
    if found:
        user_data[user_id]["current_word"] = found
        bot.send_message(
            message.chat.id,
            f"🎯 *Тренировка частых ошибок*\n\nСлово *{found['word']}* — *{found['translation']}*\n\nНапиши его перевод ещё раз:",
            parse_mode="Markdown"
        )
        user_data[user_id]["current_mode"] = "training"
    else:
        bot.send_message(message.chat.id, "Не удалось найти слово для тренировки.")

# ========== ДОБАВЛЕНИЕ В СЛОВАРЬ ==========
@bot.message_handler(func=lambda message: message.text == "➕ В словарь")
def add_to_vocabulary(message):
    user_id = message.from_user.id
    word_data = user_data[user_id].get("current_word")
    
    if not word_data:
        bot.send_message(message.chat.id, "⚠️ Нет слова для добавления")
        return
    
    # Проверяем, есть ли уже
    exists = False
    for item in user_data[user_id]["vocabulary"]:
        if item["word"] == word_data["word"]:
            exists = True
            break
    
    if not exists:
        user_data[user_id]["vocabulary"].append(word_data)
        bot.send_message(message.chat.id, f"✅ Слово *{word_data['word']}* добавлено в словарь", parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, "ℹ️ Это слово уже в словаре")

# ========== PDF СЛОВАРЬ ==========
@bot.message_handler(func=lambda message: message.text == "📄 Скачать PDF")
def generate_pdf(message):
    user_id = message.from_user.id
    vocab = user_data[user_id]["vocabulary"]
    
    if not vocab:
        bot.send_message(message.chat.id, "📄 Словарь пуст. Сначала добавь слова через «➕ В словарь»")
        return
    
    try:
        # Создаём PDF
        pdf = FPDF()
        pdf.add_page()
        
        # Заголовок
        pdf.set_font("Arial", 'B', 20)
        pdf.cell(200, 20, "Мой словарь", ln=True, align='C')
        pdf.ln(10)
        
        # Дата
        from datetime import datetime
        pdf.set_font("Arial", '', 12)
        pdf.cell(200, 10, f"Создано: {datetime.now().strftime('%d.%m.%Y')}", ln=True, align='C')
        pdf.ln(10)
        
        # Таблица
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(90, 10, "Слово", 1, 0, 'C')
        pdf.cell(90, 10, "Перевод", 1, 1, 'C')
        
        pdf.set_font("Arial", '', 12)
        for item in vocab:
            pdf.cell(90, 10, item['word'], 1, 0, 'C')
            pdf.cell(90, 10, item['translation'], 1, 1, 'C')
        
        # Сохраняем во временный файл
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            pdf.output(tmp.name)
            tmp_path = tmp.name
        
        # Отправляем
        with open(tmp_path, 'rb') as f:
            bot.send_document(message.chat.id, f, caption="📘 Твой словарь в красивом формате")
        
        # Удаляем временный файл
        os.unlink(tmp_path)
        
    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ Ошибка при создании PDF: {e}")

# ========== ПРОДОЛЖИТЬ ==========
@bot.message_handler(func=lambda message: message.text == "🔁 Продолжить")
def continue_mode(message):
    user_id = message.from_user.id
    mode = user_data[user_id].get("current_mode")
    
    if mode == "listening":
        # Продолжаем с той же темой и уровнем
        topic = user_data[user_id]["current_topic"]
        level = user_data[user_id]["current_level"]
        words = WORD_BASE.get(topic, {}).get(level, [])
        
        if words:
            word_data = random.choice(words)
            user_data[user_id]["current_word"] = word_data
            user_data[user_id]["stats"]["total_attempts"] += 1
            
            send_audio(message.chat.id, word_data["word"])
            
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton("❓ Не знаю"))
            markup.add(types.KeyboardButton("🏠 Главное меню"))
            
            bot.send_message(message.chat.id, "📝 Напиши перевод слова:", reply_markup=markup)
    
    elif mode == "grammar":
        grammar_mode(message)
    
    elif mode == "text":
        text_mode(message)
    
    elif mode == "training":
        mistake_training(message)

# ========== ГЛАВНОЕ МЕНЮ ==========
@bot.message_handler(func=lambda message: message.text == "🏠 Главное меню")
def back_to_main(message):
    send_welcome(message)

# ========== ОБРАБОТКА ГОЛОСОВЫХ (ЗАГЛУШКА ДЛЯ ТЕСТА) ==========
@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    bot.send_message(message.chat.id, "🎤 Голосовое получено. Сейчас проверю...")
    # Здесь будет реальная проверка через Speech-to-Text
    bot.send_message(message.chat.id, "✅ Всё правильно! (тестовый режим)")

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    print("✅ БОТ ЗАПУЩЕН")
    print(f"Тем: {len(TOPICS)}")
    print(f"Уровней: {len(LEVELS)}")
    total_words = sum(len(WORD_BASE[t][l]) for t in TOPICS for l in LEVELS)
    print(f"Всего слов в базе: {total_words}")
    print(f"Грамматических ошибок в базе: {sum(len(GRAMMAR_BASE[l]) for l in LEVELS)}")
    bot.polling(none_stop=True)