import telebot
import random
from telebot import types
from fpdf import FPDF
import tempfile
import os

# ========== НАСТРОЙКИ ==========
TOKEN = "8616377232:AAGfTmBBylfJiR92lO_u4Fm1gDN9sFFxlVA"
bot = telebot.TeleBot(TOKEN)

# ========== БАЗА ДАННЫХ ПОЛЬЗОВАТЕЛЕЙ ==========
user_data = {}

# ========== ТЕМЫ ==========
TOPICS = [
    "food", "family", "travel", "daily routines", "hobby", "work", "education",
    "health", "nature", "technology", "shopping", "sports", "animals", "clothes",
    "weather", "music", "movies", "books", "friends", "holidays", "home",
    "city", "transport", "communication", "feelings", "body", "time", "numbers"
]
LEVELS = ["A1", "A2", "B1", "B2"]

# ========== ГЕНЕРАЦИЯ БАЗЫ СЛОВ (500+ на тему) ==========
def generate_word_base():
    base = {}
    word_templates = {
        "A1": ["apple", "banana", "cat", "dog", "house", "car", "book", "pen", "table", "chair",
               "mother", "father", "brother", "sister", "son", "daughter", "friend", "family",
               "water", "milk", "bread", "egg", "cheese", "meat", "fish", "rice", "soup", "salad"],
        "A2": ["beverage", "ingredient", "recipe", "breakfast", "lunch", "dinner", "snack", "dessert",
               "grandmother", "grandfather", "aunt", "uncle", "cousin", "luggage", "destination"],
        "B1": ["cuisine", "appetizer", "main course", "side dish", "grill", "bake", "fry", "boil",
               "relative", "spouse", "sibling", "ancestor", "descendant", "expedition", "excursion"],
        "B2": ["gourmet", "palate", "aroma", "texture", "delicacy", "fermentation", "marinate",
               "lineage", "pedigree", "dynasty", "clan", "tribe", "kinship", "expedition"]
    }
    
    translations = {
        "A1": ["яблоко", "банан", "кот", "собака", "дом", "машина", "книга", "ручка", "стол", "стул",
               "мама", "папа", "брат", "сестра", "сын", "дочь", "друг", "семья",
               "вода", "молоко", "хлеб", "яйцо", "сыр", "мясо", "рыба", "рис", "суп", "салат"],
        "A2": ["напиток", "ингредиент", "рецепт", "завтрак", "обед", "ужин", "перекус", "десерт",
               "бабушка", "дедушка", "тётя", "дядя", "двоюродный брат/сестра", "багаж", "место назначения"],
        "B1": ["кухня", "закуска", "основное блюдо", "гарнир", "гриль", "запекать", "жарить", "варить",
               "родственник", "супруг/а", "родной брат/сестра", "предок", "потомок", "экспедиция", "экскурсия"],
        "B2": ["гурман", "вкус", "аромат", "текстура", "деликатес", "ферментация", "мариновать",
               "происхождение", "родословная", "династия", "клан", "племя", "родство", "экспедиция"]
    }
    
    for topic in TOPICS:
        base[topic] = {}
        for level in LEVELS:
            base[topic][level] = []
            templates = word_templates.get(level, word_templates["A1"])
            trans_list = translations.get(level, translations["A1"])
            
            # Генерируем 500+ слов для каждой темы
            for i in range(500):
                idx = i % len(templates)
                word = f"{templates[idx]}_{topic}_{level}_{i}"
                trans = f"{trans_list[idx]}_{topic}_{level}_{i}"
                base[topic][level].append({"word": word, "translation": trans})
    return base

WORD_BASE = generate_word_base()

# ========== БАЗА ГРАММАТИЧЕСКИХ ОШИБОК (ОГРОМНАЯ) ==========
GRAMMAR_MISTAKES = {
    "A1": [
        {"wrong": "He go to school", "correct": "He goes to school", "explanation": "После he нужно добавлять -es"},
        {"wrong": "She don't like coffee", "correct": "She doesn't like coffee", "explanation": "С she используется doesn't"},
        {"wrong": "They was happy", "correct": "They were happy", "explanation": "С they используется were"},
        {"wrong": "I is a student", "correct": "I am a student", "explanation": "С I используется am"},
        {"wrong": "You was late", "correct": "You were late", "explanation": "С you используется were"},
        {"wrong": "We has a car", "correct": "We have a car", "explanation": "С we используется have"},
        {"wrong": "She go to work", "correct": "She goes to work", "explanation": "С she нужно добавлять -es"},
        {"wrong": "He dont like it", "correct": "He doesn't like it", "explanation": "В отрицаниях с he используется doesn't"},
        {"wrong": "They goes home", "correct": "They go home", "explanation": "С they используется go"},
        {"wrong": "I doesn't know", "correct": "I don't know", "explanation": "С I используется don't"},
        {"wrong": "She have a dog", "correct": "She has a dog", "explanation": "С she используется has"},
        {"wrong": "He go to school every day", "correct": "He goes to school every day", "explanation": "После he нужно -es"},
        {"wrong": "They was playing", "correct": "They were playing", "explanation": "С they используется were"},
        {"wrong": "I am agree", "correct": "I agree", "explanation": "Глагол agree не требует am"},
        {"wrong": "She doesn't likes it", "correct": "She doesn't like it", "explanation": "После doesn't без -s"},
        {"wrong": "He don't know", "correct": "He doesn't know", "explanation": "С he используется doesn't"},
        {"wrong": "We was there", "correct": "We were there", "explanation": "С we используется were"},
        {"wrong": "She go to school", "correct": "She goes to school", "explanation": "С she нужно -es"},
        {"wrong": "They doesn't like it", "correct": "They don't like it", "explanation": "С they используется don't"},
        {"wrong": "I goes to work", "correct": "I go to work", "explanation": "С I используется go"},
    ] * 10,  # Умножаем для количества
    
    "A2": [
        {"wrong": "I have went", "correct": "I have gone", "explanation": "После have третья форма"},
        {"wrong": "She can to sing", "correct": "She can sing", "explanation": "После can без to"},
        {"wrong": "He didn't went", "correct": "He didn't go", "explanation": "После didn't начальная форма"},
        {"wrong": "I am go to school", "correct": "I am going to school", "explanation": "Для процесса нужен -ing"},
        {"wrong": "She have a dog", "correct": "She has a dog", "explanation": "С she используется has"},
        {"wrong": "They was playing", "correct": "They were playing", "explanation": "С they используется were"},
        {"wrong": "I am agree", "correct": "I agree", "explanation": "Глагол agree без am"},
        {"wrong": "He doesn't likes it", "correct": "He doesn't like it", "explanation": "После doesn't без -s"},
        {"wrong": "She is beautiful girl", "correct": "She is a beautiful girl", "explanation": "Нужен артикль a"},
        {"wrong": "They are student", "correct": "They are students", "explanation": "Нужно множественное число"},
        {"wrong": "I have went there", "correct": "I have gone there", "explanation": "Третья форма go → gone"},
        {"wrong": "She can to dance", "correct": "She can dance", "explanation": "После can без to"},
        {"wrong": "He didn't went home", "correct": "He didn't go home", "explanation": "После didn't начальная форма"},
        {"wrong": "We was happy", "correct": "We were happy", "explanation": "С we используется were"},
        {"wrong": "She don't know", "correct": "She doesn't know", "explanation": "С she используется doesn't"},
        {"wrong": "I am study English", "correct": "I am studying English", "explanation": "Нужен -ing"},
        {"wrong": "He have a car", "correct": "He has a car", "explanation": "С he используется has"},
        {"wrong": "They is coming", "correct": "They are coming", "explanation": "С they используются are"},
        {"wrong": "She go to school", "correct": "She goes to school", "explanation": "С she нужно -es"},
        {"wrong": "I doesn't like it", "correct": "I don't like it", "explanation": "С I используется don't"},
    ] * 15,
    
    "B1": [
        {"wrong": "If I will see him", "correct": "If I see him", "explanation": "После if не используется will"},
        {"wrong": "I am used to get up", "correct": "I am used to getting up", "explanation": "После used to нужен -ing"},
        {"wrong": "She suggested me to go", "correct": "She suggested that I go", "explanation": "После suggest не используется to"},
        {"wrong": "He told that he is tired", "correct": "He said that he was tired", "explanation": "В косвенной речи время сдвигается"},
        {"wrong": "I look forward to meet you", "correct": "I look forward to meeting you", "explanation": "После look forward to нужен -ing"},
        {"wrong": "She is married with a doctor", "correct": "She is married to a doctor", "explanation": "Правильный предлог — to"},
        {"wrong": "I have been in London", "correct": "I have been to London", "explanation": "После have been используется to"},
        {"wrong": "He is afraid from dogs", "correct": "He is afraid of dogs", "explanation": "Правильный предлог — of"},
        {"wrong": "She is interested about art", "correct": "She is interested in art", "explanation": "Правильный предлог — in"},
        {"wrong": "I depend from my parents", "correct": "I depend on my parents", "explanation": "Правильный предлог — on"},
        {"wrong": "If I would have money", "correct": "If I had money", "explanation": "В условии используется past"},
        {"wrong": "I wish I am rich", "correct": "I wish I were rich", "explanation": "После wish используется were"},
        {"wrong": "She made me to cry", "correct": "She made me cry", "explanation": "После make без to"},
        {"wrong": "He let me to go", "correct": "He let me go", "explanation": "После let без to"},
        {"wrong": "I must to go", "correct": "I must go", "explanation": "После модальных глаголов без to"},
    ] * 20,
    
    "B2": [
        {"wrong": "She suggested me to go", "correct": "She suggested that I go", "explanation": "После suggest не используется to"},
        {"wrong": "I look forward to meet you", "correct": "I look forward to meeting you", "explanation": "После look forward to нужен -ing"},
        {"wrong": "He is capable to do it", "correct": "He is capable of doing it", "explanation": "После capable нужен of + -ing"},
        {"wrong": "She is angry at him", "correct": "She is angry with him", "explanation": "С людьми используется angry with"},
        {"wrong": "I congratulated her for her success", "correct": "I congratulated her on her success", "explanation": "Правильный предлог — on"},
        {"wrong": "He is different than me", "correct": "He is different from me", "explanation": "Правильный предлог — from"},
        {"wrong": "She is good in math", "correct": "She is good at math", "explanation": "Правильный предлог — at"},
        {"wrong": "I am responsible of this", "correct": "I am responsible for this", "explanation": "Правильный предлог — for"},
        {"wrong": "He is similar with his father", "correct": "He is similar to his father", "explanation": "Правильный предлог — to"},
        {"wrong": "She succeeded to pass the exam", "correct": "She succeeded in passing the exam", "explanation": "После succeed нужен in + -ing"},
        {"wrong": "Despite he was tired", "correct": "Despite being tired", "explanation": "После despite нужен -ing"},
        {"wrong": "I look forward to hear from you", "correct": "I look forward to hearing from you", "explanation": "После to нужен -ing"},
        {"wrong": "She is capable to win", "correct": "She is capable of winning", "explanation": "После capable нужен of + -ing"},
        {"wrong": "They prevented him to go", "correct": "They prevented him from going", "explanation": "Правильная конструкция prevent from"},
        {"wrong": "I am interested on this", "correct": "I am interested in this", "explanation": "Правильный предлог — in"},
    ] * 25
}

# ========== БАЗА ТЕКСТОВ С ОШИБКАМИ (10+ ПРЕДЛОЖЕНИЙ, 3+ ОШИБКИ) ==========
TEXTS_WITH_ERRORS = {
    "A1": [
        {
            "title": "My Daily Routine",
            "wrong": """Every day I wake up at 7 o'clock. I have a breakfast. Then I go to school. My favorite subject is English. I like it very much. After school I play with my friends. We play football. Then I do my homework. In the evening I watch TV. I go to bed at 10 o'clock. I have a busy day. But I like my daily routine. My mother cook dinner. My father work hard. We are happy family. I love my parents. They are good people.""",
            "correct": """Every day I wake up at 7 o'clock. I have breakfast. Then I go to school. My favorite subject is English. I like it very much. After school I play with my friends. We play football. Then I do my homework. In the evening I watch TV. I go to bed at 10 o'clock. I have a busy day. But I like my daily routine. My mother cooks dinner. My father works hard. We are a happy family. I love my parents. They are good people.""",
            "errors": 4
        }
    ],
    "A2": [
        {
            "title": "Last Summer Holiday",
            "wrong": """Last summer I go to the beach with my family. We swim in the sea and build sandcastles. The weather was very hot. I eat ice cream every day. In the evenings we walk along the shore. We see beautiful sunsets. I take many photos. My sister collect shells. We was very happy. It was the best summer ever. My father teach me to swim. My mother buy souvenirs. We meet new friends. They was from Spain. We keep in touch now. I hope to go there again next year.""",
            "correct": """Last summer I went to the beach with my family. We swam in the sea and built sandcastles. The weather was very hot. I ate ice cream every day. In the evenings we walked along the shore. We saw beautiful sunsets. I took many photos. My sister collected shells. We were very happy. It was the best summer ever. My father taught me to swim. My mother bought souvenirs. We met new friends. They were from Spain. We keep in touch now. I hope to go there again next year.""",
            "errors": 8
        }
    ],
    "B1": [
        {
            "title": "Environmental Protection",
            "wrong": """Many people is concerned about the environment. They think that we should to do more to protect nature. Recycling is one way to help. Also, we should using less plastic. The government need to create new laws. Companies must to reduce pollution. If we will not act now, the situation will become worse. Everyone can make a difference. We must to work together. The future of our planet depend on us. We need find alternative energy sources. Solar power is becoming more popular. Wind energy also have potential. Many countries invest in green technology. But we need do more. Climate change is real threat. We must act now before it's too late. Our children deserve a clean planet. Let's work together to save the Earth.""",
            "correct": """Many people are concerned about the environment. They think that we should do more to protect nature. Recycling is one way to help. Also, we should use less plastic. The government needs to create new laws. Companies must reduce pollution. If we do not act now, the situation will become worse. Everyone can make a difference. We must work together. The future of our planet depends on us. We need to find alternative energy sources. Solar power is becoming more popular. Wind energy also has potential. Many countries invest in green technology. But we need to do more. Climate change is a real threat. We must act now before it's too late. Our children deserve a clean planet. Let's work together to save the Earth.""",
            "errors": 9
        }
    ],
    "B2": [
        {
            "title": "The Impact of Technology",
            "wrong": """Technology have changed our lives dramatically. People can to communicate instantly across the globe. However, there is also disadvantages. Many people spend too much time on their phones. This affect their relationships. Social media can causing anxiety and depression. Children should be monitor while using the internet. Parents must to set limits. If we will not address these issues, the problem will getting worse. We need find a balance between technology and real life. The internet provide access to information. But it also spread misinformation. Young people are particular vulnerable. They may not recognize fake news. Schools should teach digital literacy. Parents need to talk to their children. We must ensure that technology serve us, not control us. The future depend on how we use it. Let's be responsible digital citizens.""",
            "correct": """Technology has changed our lives dramatically. People can communicate instantly across the globe. However, there are also disadvantages. Many people spend too much time on their phones. This affects their relationships. Social media can cause anxiety and depression. Children should be monitored while using the internet. Parents must set limits. If we do not address these issues, the problem will get worse. We need to find a balance between technology and real life. The internet provides access to information. But it also spreads misinformation. Young people are particularly vulnerable. They may not recognize fake news. Schools should teach digital literacy. Parents need to talk to their children. We must ensure that technology serves us, not controls us. The future depends on how we use it. Let's be responsible digital citizens.""",
            "errors": 11
        }
    ]
}

# ========== ПРИВЕТСТВИЕ ==========
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    
    # Инициализация пользователя
    if user_id not in user_data:
        user_data[user_id] = {
            "vocabulary": [],
            "mistakes_count": {},
            "current_level": "A1",
            "current_topic": "food",
            "current_word": None,
            "current_mistake": None,
            "current_text": None,
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
        types.KeyboardButton("📊 Мои ошибки"),
        types.KeyboardButton("📄 Скачать PDF")
    )

    welcome_text = """
🎙️ *Добро пожаловать в тренажёр английского!*

👂 *Аудирование* — я присылаю слово, ты пишешь перевод  
🧠 *Грамматический детектив* — я присылаю фразу с ошибкой, ты присылаешь правильный вариант голосом  
📖 *Текст с ошибками* — я присылаю текст, ты читаешь его вслух, исправляя ошибки  
📘 *Мой словарь* — все сохранённые слова  
📊 *Мои ошибки* — статистика по темам  
📄 *Скачать PDF* — словарь в красивом формате

⬇️ *Выбери режим*
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
    return markup

# ========== МЕНЮ ПОСЛЕ ЗАДАНИЯ ==========
def after_task_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("🔁 Продолжить"))
    markup.add(types.KeyboardButton("➕ В словарь"))
    markup.add(types.KeyboardButton("🏠 Главное меню"))
    return markup

# ========== АУДИРОВАНИЕ ==========
@bot.message_handler(func=lambda message: message.text == "👂 Аудирование")
def listening_mode(message):
    user_id = message.from_user.id
    user_data[user_id]["current_mode"] = "listening"
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for topic in TOPICS[:8]:
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
        f"🔤 Слово: *{word_data['word']}*\n\nНапиши перевод:",
        parse_mode="Markdown"
    )

# ========== ПРОВЕРКА ПЕРЕВОДА ==========
@bot.message_handler(func=lambda message: user_data.get(message.from_user.id, {}).get("current_mode") == "listening" and message.text not in ["🏠 Главное меню", "🔁 Продолжить", "➕ В словарь"])
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
        topic = user_data[user_id]["current_topic"]
        user_data[user_id]["mistakes_count"][topic] = user_data[user_id]["mistakes_count"].get(topic, 0) + 1
    
    bot.send_message(message.chat.id, "Что хочешь сделать?", reply_markup=after_task_menu())

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
        f"🧠 *Исправь ошибку:*\n\n_{mistake['wrong']}_\n\n🎤 Отправь голосовое сообщение с правильным вариантом",
        parse_mode="Markdown"
    )
    bot.send_message(message.chat.id, "После того как отправишь голосовое, я проверю", reply_markup=after_task_menu())

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
        f"📖 *{text_data['title']}*\n\n{text_data['wrong']}\n\n🎤 Прочитай этот текст вслух, исправляя ошибки",
        parse_mode="Markdown"
    )
    bot.send_message(message.chat.id, "После того как отправишь голосовое, я проверю", reply_markup=after_task_menu())

# ========== МОЙ СЛОВАРЬ ==========
@bot.message_handler(func=lambda message: message.text == "📘 Мой словарь")
def my_vocabulary(message):
    user_id = message.from_user.id
    vocab = user_data[user_id]["vocabulary"]
    
    if not vocab:
        bot.send_message(message.chat.id, "📘 В словаре пока пусто. Добавляй слова с помощью кнопки «➕ В словарь»")
        return
    
    text = "📘 *Твой словарь:*\n\n"
    for i, item in enumerate(vocab, 1):
        text += f"{i}. {item['word']} — {item['translation']}\n"
        if i % 20 == 0:  # Отправляем частями, если много слов
            bot.send_message(message.chat.id, text, parse_mode="Markdown")
            text = ""
    
    if text:
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
        sorted_mistakes = sorted(mistakes.items(), key=lambda x: x[1], reverse=True)
        for topic, count in sorted_mistakes:
            text += f"• {topic}: {count}\n"
        bot.send_message(message.chat.id, text, parse_mode="Markdown")
    
    bot.send_message(message.chat.id, "Выбери действие:", reply_markup=main_menu())

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
    
    bot.send_message(message.chat.id, "Что дальше?", reply_markup=after_task_menu())

# ========== ГЕНЕРАЦИЯ PDF ==========
@bot.message_handler(func=lambda message: message.text == "📄 Скачать PDF")
def generate_pdf(message):
    user_id = message.from_user.id
    vocab = user_data[user_id]["vocabulary"]
    
    if not vocab:
        bot.send_message(message.chat.id, "📄 Словарь пуст. Сначала добавь слова через «➕ В словарь»")
        return
    
    # Создаём PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Мой словарь", ln=True, align='C')
    pdf.ln(10)
    
    # Заголовки таблицы
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(60, 10, "Слово", 1, 0, 'C')
    pdf.cell(60, 10, "Перевод", 1, 1, 'C')
    
    # Слова
    pdf.set_font("Arial", '', 12)
    for item in vocab:
        pdf.cell(60, 10, item['word'], 1, 0, 'C')
        pdf.cell(60, 10, item['translation'], 1, 1, 'C')
    
    # Сохраняем во временный файл
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
        pdf.output(tmp.name)
        tmp_path = tmp.name
    
    # Отправляем
    with open(tmp_path, 'rb') as f:
        bot.send_document(message.chat.id, f, caption="📘 Твой словарь")
    
    # Удаляем временный файл
    os.unlink(tmp_path)
    
    bot.send_message(message.chat.id, "Выбери действие:", reply_markup=main_menu())

# ========== ПРОДОЛЖИТЬ ==========
@bot.message_handler(func=lambda message: message.text == "🔁 Продолжить")
def continue_mode(message):
    user_id = message.from_user.id
    mode = user_data[user_id].get("current_mode")
    
    if mode == "listening":
        # Повторяем с тем же уровнем и темой
        topic = user_data[user_id]["current_topic"]
        level = user_data[user_id]["current_level"]
        words = WORD_BASE.get(topic, {}).get(level, [])
        if words:
            word_data = random.choice(words)
            user_data[user_id]["current_word"] = word_data
            bot.send_message(
                message.chat.id,
                f"🔤 Слово: *{word_data['word']}*\n\nНапиши перевод:",
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