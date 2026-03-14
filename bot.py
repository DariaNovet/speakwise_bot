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

# ========== ОГРОМНАЯ БАЗА СЛОВ (10 000+) ==========
# Здесь представлена сокращённая версия для читаемости.
# В реальном коде будет 10 000+ слов, разбитых по темам и уровням.
WORD_BASE = {
    "food": {
        "A1": [{"word": w, "translation": t} for w, t in [
            ("apple", "яблоко"), ("banana", "банан"), ("bread", "хлеб"), ("milk", "молоко"),
            ("egg", "яйцо"), ("cheese", "сыр"), ("water", "вода"), ("juice", "сок"),
            ("meat", "мясо"), ("fish", "рыба"), ("rice", "рис"), ("soup", "суп"),
            ("salad", "салат"), ("sugar", "сахар"), ("salt", "соль"), ("tea", "чай"),
            ("coffee", "кофе"), ("cake", "торт"), ("cookie", "печенье"), ("butter", "масло")
        ]],
        "A2": [{"word": w, "translation": t} for w, t in [
            ("beverage", "напиток"), ("recipe", "рецепт"), ("ingredient", "ингредиент"),
            ("breakfast", "завтрак"), ("lunch", "обед"), ("dinner", "ужин"), ("snack", "перекус"),
            ("dessert", "десерт"), ("spice", "специя"), ("flour", "мука"), ("oven", "духовка"),
            ("pan", "сковорода"), ("plate", "тарелка"), ("cup", "чашка"), ("bowl", "миска")
        ]],
        "B1": [{"word": w, "translation": t} for w, t in [
            ("cuisine", "кухня"), ("appetizer", "закуска"), ("main course", "основное блюдо"),
            ("side dish", "гарнир"), ("beverage", "напиток"), ("grill", "гриль"), ("bake", "запекать"),
            ("fry", "жарить"), ("boil", "варить"), ("steam", "готовить на пару"), ("roast", "жарить в духовке"),
            ("dough", "тесто"), ("yeast", "дрожжи"), ("vinegar", "уксус"), ("sauce", "соус")
        ]],
        "B2": [{"word": w, "translation": t} for w, t in [
            ("gourmet", "гурман"), ("palate", "нёбо"), ("aroma", "аромат"), ("texture", "текстура"),
            ("cuisine", "высокая кухня"), ("delicacy", "деликатес"), ("fermentation", "ферментация"),
            ("marinate", "мариновать"), ("seasoning", "приправа"), ("herb", "трава"), ("spice blend", "смесь специй"),
            ("infusion", "настой"), ("culinary", "кулинарный"), ("gastronomy", "гастрономия")
        ]]
    },
    "family": {
        "A1": [{"word": w, "translation": t} for w, t in [
            ("mother", "мама"), ("father", "папа"), ("brother", "брат"), ("sister", "сестра"),
            ("son", "сын"), ("daughter", "дочь"), ("grandmother", "бабушка"), ("grandfather", "дедушка"),
            ("aunt", "тётя"), ("uncle", "дядя"), ("cousin", "двоюродный брат/сестра"), ("baby", "младенец"),
            ("parents", "родители"), ("children", "дети"), ("wife", "жена"), ("husband", "муж")
        ]],
        "A2": [{"word": w, "translation": t} for w, t in [
            ("grandparents", "бабушка и дедушка"), ("grandson", "внук"), ("granddaughter", "внучка"),
            ("stepmother", "мачеха"), ("stepfather", "отчим"), ("stepson", "пасынок"), ("stepdaughter", "падчерица"),
            ("half-brother", "единокровный брат"), ("half-sister", "единокровная сестра"), ("in-laws", "родственники со стороны супруга"),
            ("mother-in-law", "свекровь/тёща"), ("father-in-law", "свёкор/тесть")
        ]],
        "B1": [{"word": w, "translation": t} for w, t in [
            ("relative", "родственник"), ("spouse", "супруг/а"), ("sibling", "родной брат или сестра"),
            ("ancestor", "предок"), ("descendant", "потомок"), ("generation", "поколение"), ("family tree", "родословное древо"),
            ("hereditary", "наследственный"), ("paternity", "отцовство"), ("maternity", "материнство"), ("kinship", "родство"),
            ("offspring", "потомство"), ("foster family", "приёмная семья"), ("adoption", "усыновление")
        ]],
        "B2": [{"word": w, "translation": t} for w, t in [
            ("lineage", "происхождение"), ("pedigree", "родословная"), ("dynasty", "династия"), ("clan", "клан"),
            ("tribe", "племя"), ("genealogy", "генеалогия"), ("matriarch", "матриарх"), ("patriarch", "патриарх"),
            ("filial", "сыновний/дочерний"), ("fraternal", "братский"), ("sororal", "сестринский"), ("conjugal", "супружеский")
        ]]
    },
    "travel": {
        "A1": [{"word": w, "translation": t} for w, t in [
            ("hotel", "отель"), ("plane", "самолёт"), ("ticket", "билет"), ("train", "поезд"),
            ("bus", "автобус"), ("car", "машина"), ("map", "карта"), ("passport", "паспорт"),
            ("bag", "сумка"), ("suitcase", "чемодан"), ("trip", "поездка"), ("holiday", "отпуск"),
            ("beach", "пляж"), ("mountain", "гора"), ("city", "город"), ("country", "страна")
        ]],
        "A2": [{"word": w, "translation": t} for w, t in [
            ("luggage", "багаж"), ("boarding pass", "посадочный талон"), ("check-in", "регистрация"),
            ("departure", "отправление"), ("arrival", "прибытие"), ("delay", "задержка"), ("platform", "платформа"),
            ("tourist", "турист"), ("guide", "гид"), ("sightseeing", "осмотр достопримечательностей"),
            ("museum", "музей"), ("restaurant", "ресторан"), ("reservation", "бронирование")
        ]],
        "B1": [{"word": w, "translation": t} for w, t in [
            ("destination", "место назначения"), ("itinerary", "маршрут"), ("accommodation", "размещение"),
            ("all-inclusive", "всё включено"), ("cruise", "круиз"), ("excursion", "экскурсия"),
            ("backpacking", "поход с рюкзаком"), ("hitchhiking", "автостоп"), ("souvenir", "сувенир"),
            ("currency", "валюта"), ("exchange rate", "обменный курс"), ("visa", "виза")
        ]],
        "B2": [{"word": w, "translation": t} for w, t in [
            ("expedition", "экспедиция"), ("journey", "путешествие"), ("voyage", "морское путешествие"),
            ("pilgrimage", "паломничество"), ("nomad", "кочевник"), ("itinerant", "странствующий"),
            ("cosmopolitan", "космополитичный"), ("wanderlust", "страсть к путешествиям"), ("globetrotter", "бывалый путешественник"),
            ("backpacker", "путешественник с рюкзаком"), ("bucket list", "список желаний"), ("road trip", "путешествие на машине")
        ]]
    }
}

# Дополнительные темы будут добавлены аналогично:
# work, education, hobby, health, nature, technology, shopping, sports, animals, clothes, etc.
# В реальном коде здесь будет 10 000+ слов

# ========== БАЗА ГРАММАТИЧЕСКИХ ОШИБОК ==========
GRAMMAR_MISTAKES = {
    "A1": [
        {"wrong": "He go to school", "correct": "He goes to school", "explanation": "После he нужно добавлять -es к глаголу (go → goes)"},
        {"wrong": "She don't like coffee", "correct": "She doesn't like coffee", "explanation": "С she используется doesn't, а не don't"},
        {"wrong": "They was happy", "correct": "They were happy", "explanation": "С they используется were, а не was"},
        {"wrong": "I is a student", "correct": "I am a student", "explanation": "С I используется am, а не is"},
        {"wrong": "You was late", "correct": "You were late", "explanation": "С you используется were, а не was"},
        {"wrong": "We has a car", "correct": "We have a car", "explanation": "С we используется have, а не has"},
        {"wrong": "She go to work", "correct": "She goes to work", "explanation": "С she нужно добавлять -es к глаголу"},
        {"wrong": "He dont like it", "correct": "He doesn't like it", "explanation": "В отрицаниях с he используется doesn't"},
        {"wrong": "They goes home", "correct": "They go home", "explanation": "С they используется go, а не goes"},
        {"wrong": "I doesn't know", "correct": "I don't know", "explanation": "С I используется don't, а не doesn't"}
    ],
    "A2": [
        {"wrong": "I have went", "correct": "I have gone", "explanation": "После have используется третья форма глагола (go → gone)"},
        {"wrong": "She can to sing", "correct": "She can sing", "explanation": "После модальных глаголов (can, must, should) частица to не ставится"},
        {"wrong": "He didn't went", "correct": "He didn't go", "explanation": "После didn't используется начальная форма глагола"},
        {"wrong": "I am go to school", "correct": "I am going to school", "explanation": "Для действий в процессе используется am/is/are + глагол с -ing"},
        {"wrong": "She have a dog", "correct": "She has a dog", "explanation": "С she используется has, а не have"},
        {"wrong": "They was playing", "correct": "They were playing", "explanation": "С they используется were, а не was"},
        {"wrong": "I am agree", "correct": "I agree", "explanation": "Глагол agree не требует am, это просто I agree"},
        {"wrong": "He doesn't likes it", "correct": "He doesn't like it", "explanation": "После doesn't глагол без окончания -s"},
        {"wrong": "She is beautiful girl", "correct": "She is a beautiful girl", "explanation": "Перед исчисляемым существительным нужен артикль a/an"},
        {"wrong": "They are student", "correct": "They are students", "explanation": "После they нужно множественное число students"}
    ],
    "B1": [
        {"wrong": "If I will see him", "correct": "If I see him", "explanation": "В условных предложениях после if не используется will"},
        {"wrong": "I am used to get up early", "correct": "I am used to getting up early", "explanation": "После be used to нужен герундий (-ing)"},
        {"wrong": "She suggested me to go", "correct": "She suggested that I go", "explanation": "После suggest не используется инфинитив с to"},
        {"wrong": "He told that he is tired", "correct": "He said that he was tired", "explanation": "В косвенной речи время часто сдвигается (is → was)"},
        {"wrong": "I look forward to meet you", "correct": "I look forward to meeting you", "explanation": "После look forward to нужен герундий (-ing)"},
        {"wrong": "She is married with a doctor", "correct": "She is married to a doctor", "explanation": "Правильный предлог — married to"},
        {"wrong": "I have been in London", "correct": "I have been to London", "explanation": "После have been используется to, а не in"},
        {"wrong": "He is afraid from dogs", "correct": "He is afraid of dogs", "explanation": "Правильный предлог — afraid of"},
        {"wrong": "She is interested about art", "correct": "She is interested in art", "explanation": "Правильный предлог — interested in"},
        {"wrong": "I depend from my parents", "correct": "I depend on my parents", "explanation": "Правильный предлог — depend on"}
    ],
    "B2": [
        {"wrong": "She suggested me to go", "correct": "She suggested that I go", "explanation": "После suggest не используется инфинитив с to"},
        {"wrong": "I look forward to meet you", "correct": "I look forward to meeting you", "explanation": "После look forward to нужен герундий (-ing)"},
        {"wrong": "He is capable to do it", "correct": "He is capable of doing it", "explanation": "После capable нужен of + герундий"},
        {"wrong": "She is angry at him", "correct": "She is angry with him", "explanation": "С людьми используется angry with"},
        {"wrong": "I congratulated her for her success", "correct": "I congratulated her on her success", "explanation": "Правильный предлог — congratulate on"},
        {"wrong": "He is different than me", "correct": "He is different from me", "explanation": "Правильный предлог — different from"},
        {"wrong": "She is good in math", "correct": "She is good at math", "explanation": "Правильный предлог — good at"},
        {"wrong": "I am responsible of this", "correct": "I am responsible for this", "explanation": "Правильный предлог — responsible for"},
        {"wrong": "He is similar with his father", "correct": "He is similar to his father", "explanation": "Правильный предлог — similar to"},
        {"wrong": "She succeeded to pass the exam", "correct": "She succeeded in passing the exam", "explanation": "После succeed нужен in + герундий"}
    ]
}

# ========== БАЗА ТЕКСТОВ С ОШИБКАМИ ==========
TEXTS_WITH_ERRORS = {
    "A1": [
        {
            "title": "My Day",
            "wrong": "Every day I wake up at 7 o'clock. I have a breakfast. I go to school. My favorite subject is English. I like it very much. After school I play with my friends. Then I do my homework. In the evening I watch TV. I go to bed at 10 o'clock.",
            "correct": "Every day I wake up at 7 o'clock. I have breakfast. I go to school. My favorite subject is English. I like it very much. After school I play with my friends. Then I do my homework. In the evening I watch TV. I go to bed at 10 o'clock.",
            "errors": ["a breakfast", "", ""]
        },
        {
            "title": "My Family",
            "wrong": "I have a mother, a father and a brother. My mother is a teacher. My father is a doctor. My brother is a student. We are a happy family. We live in a big house. We have a dog. His name is Rex.",
            "correct": "I have a mother, a father and a brother. My mother is a teacher. My father is a doctor. My brother is a student. We are a happy family. We live in a big house. We have a dog. His name is Rex.",
            "errors": ["", "", ""]
        }
    ],
    "A2": [
        {
            "title": "Last Weekend",
            "wrong": "Last weekend I go to the park with my friends. We play football and then we eat ice cream. It was fun. In the evening we watch a movie. The movie was interesting. I like weekends very much.",
            "correct": "Last weekend I went to the park with my friends. We played football and then we ate ice cream. It was fun. In the evening we watched a movie. The movie was interesting. I like weekends very much.",
            "errors": ["go", "play", "eat"]
        },
        {
            "title": "My Hobby",
            "wrong": "I have a hobby. I like to reading books. I read every day. My favorite books are about adventures. I have many books at home. I also like to write stories. It is very interesting.",
            "correct": "I have a hobby. I like to read books. I read every day. My favorite books are about adventures. I have many books at home. I also like to write stories. It is very interesting.",
            "errors": ["to reading", "", ""]
        }
    ],
    "B1": [
        {
            "title": "Travel Plans",
            "wrong": "If I will have money, I travel to Japan next year. I want visit Tokyo and see the cherry blossoms. I also want to try Japanese food. I heard it's delicious. I hope my dream will come true.",
            "correct": "If I have money, I will travel to Japan next year. I want to visit Tokyo and see the cherry blossoms. I also want to try Japanese food. I heard it's delicious. I hope my dream will come true.",
            "errors": ["will have", "travel", "want visit"]
        },
        {
            "title": "Healthy Lifestyle",
            "wrong": "To be healthy, you should to eat fruits and vegetables. You also need to exercise regularly. Many people don't have time for sport, but it's important. I try to eat healthy and do sport every day.",
            "correct": "To be healthy, you should eat fruits and vegetables. You also need to exercise regularly. Many people don't have time for sport, but it's important. I try to eat healthy and do sport every day.",
            "errors": ["should to", "", ""]
        }
    ],
    "B2": [
        {
            "title": "Environmental Issues",
            "wrong": "Many people is concerned about climate change. They think that we should to do more to protect the environment. Recycling is one way to help. Also, we should use less plastic. It is everyone's responsibility.",
            "correct": "Many people are concerned about climate change. They think that we should do more to protect the environment. Recycling is one way to help. Also, we should use less plastic. It is everyone's responsibility.",
            "errors": ["is", "should to", ""]
        },
        {
            "title": "Career Choices",
            "wrong": "Choosing a career is not easy. You should to consider your interests and skills. Many people change their careers several times. It's important to find a job that you enjoy. I am interested in becoming a doctor.",
            "correct": "Choosing a career is not easy. You should consider your interests and skills. Many people change their careers several times. It's important to find a job that you enjoy. I am interested in becoming a doctor.",
            "errors": ["should to", "", ""]
        }
    ]
}

# ========== ПРИВЕТСТВИЕ ==========
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    
    # Полный сброс состояния пользователя при входе в главное меню
    user_data[user_id] = {
        "vocabulary": [],
        "unknown_words": [],
        "mistakes_count": {},
        "current_level": "A1",
        "current_topic": "food",
        "current_word_data": None,
        "current_mode": None  # track current mode: "listening", "grammar", "text"
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

# ========== ФУНКЦИЯ СБРОСА КОНТЕКСТА ==========
def clear_user_context(user_id):
    """Очищает контекст текущего задания, но сохраняет словарь и статистику"""
    if user_id in user_data:
        user_data[user_id]["current_word_data"] = None
        user_data[user_id]["current_mistake"] = None
        user_data[user_id]["current_text"] = None
        user_data[user_id]["current_mode"] = None

# ========== АУДИРОВАНИЕ ==========
@bot.message_handler(func=lambda message: message.text == "👂 Аудирование")
def listening_mode(message):
    user_id = message.from_user.id
    clear_user_context(user_id)
    user_data[user_id]["current_mode"] = "listening"
    
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
        f"📝 Напиши это слово и его перевод",
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
        clear_user_context(user_id)
        send_welcome(message)
        return
    
    if text == "🔁 Продолжить в этой теме":
        if user_data[user_id]["current_mode"] == "listening":
            send_next_word(message.chat.id, user_id)
        elif user_data[user_id]["current_mode"] == "grammar":
            grammar_detective_mode(message)
        elif user_data[user_id]["current_mode"] == "text":
            text_with_errors_mode(message)
        return
    
    if text == "📂 Сменить тему":
        if user_data[user_id]["current_mode"] == "listening":
            listening_mode(message)
        return
    
    if text == "📊 Поменять уровень":
        if user_data[user_id]["current_mode"] == "listening":
            bot.send_message(message.chat.id, "Выбери новый уровень:", reply_markup=level_keyboard("listening"))
        elif user_data[user_id]["current_mode"] == "grammar":
            bot.send_message(message.chat.id, "Выбери новый уровень:", reply_markup=level_keyboard("grammar"))
        elif user_data[user_id]["current_mode"] == "text":
            bot.send_message(message.chat.id, "Выбери новый уровень:", reply_markup=level_keyboard("text"))
        return

# ========== ОБРАБОТКА СПЕЦИАЛЬНЫХ КНОПОК ==========
@bot.message_handler(func=lambda message: message.text in ["❓ Не знаю", "➕ В словарь", "🔙 Главное меню"])
def handle_special_buttons(message):
    user_id = message.from_user.id
    text = message.text
    
    if text == "🔙 Главное меню":
        clear_user_context(user_id)
        send_welcome(message)
        return
    
    word_data = user_data[user_id].get("current_word_data")
    if not word_data:
        bot.send_message(message.chat.id, "Сначала выбери слово в режиме аудирования")
        return
    
    if text == "❓ Не знаю":
        bot.send_message(
            message.chat.id, 
            f"🔍 Это слово: *{word_data['word']}*\nПеревод: *{word_data['translation']}*",
            parse_mode="Markdown"
        )
        user_data[user_id]["unknown_words"].append(word_data["word"])
        
        # Меню действий после задания
        bot.send_message(message.chat.id, "Что хочешь сделать дальше?", reply_markup=after_task_keyboard())
    
    elif text == "➕ В словарь":
        word_entry = {
            "word": word_data["word"],
            "translation": word_data["translation"],
            "topic": user_data[user_id]["current_topic"]
        }
        
        # Проверяем, есть ли уже такое слово в словаре
        exists = False
        for item in user_data[user_id]["vocabulary"]:
            if item["word"] == word_data["word"]:
                exists = True
                break
        
        if not exists:
            user_data[user_id]["vocabulary"].append(word_entry)
            bot.send_message(message.chat.id, f"✅ Слово *{word_data['word']}* добавлено в словарь", parse_mode="Markdown")
        else:
            bot.send_message(message.chat.id, "ℹ️ Это слово уже в словаре")
        
        # Меню действий после задания
        bot.send_message(message.chat.id, "Что хочешь сделать дальше?", reply_markup=after_task_keyboard())

# ========== ПРОВЕРКА ОТВЕТА НА АУДИРОВАНИЕ ==========
@bot.message_handler(func=lambda message: message.text not in ["❓ Не знаю", "➕ В словарь", "🔙 Главное меню", "🔁 Продолжить в этой теме", "📂 Сменить тему", "📊 Поменять уровень", "🏠 Главное меню", "👂 Аудирование", "🧠 Грамматический детектив", "📖 Текст с ошибками", "📘 Мой словарь", "📊 Мои ошибки", "📄 Скачать словарь (PDF)"])
def check_listening_answer(message):
    user_id = message.from_user.id
    text = message.text.strip()

    # Проверяем, в правильном ли мы режиме
    if user_data[user_id].get("current_mode") != "listening":
        return

    word_data = user_data[user_id].get("current_word_data")
    if not word_data:
        bot.send_message(message.chat.id, "⚠️ Сначала выбери слово в режиме аудирования")
        return

    expected_word = word_data["word"]
    translation = word_data["translation"]

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
            f"✅ *Верно!*\n\nСлово: {expected_word}\nПеревод: {translation}",
            parse_mode="Markdown"
        )
    else:
        bot.send_message(
            message.chat.id,
            f"❌ *Ошибка в написании*\n\nТы написала: {user_word}\nПравильно: {expected_word}\n\nПеревод: {translation}",
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
    clear_user_context(user_id)
    user_data[user_id]["current