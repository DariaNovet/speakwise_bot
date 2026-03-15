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
    "food", "family and friends", "travel", "holidays", "hobby",
    "daily routines", "pets", "technologies", "education",
    "work", "health", "sports", "nature", "weather", "clothes",
    "shopping", "transport", "music", "movies", "books", "animals"
]
LEVELS = ["A1", "A2", "B1", "B2"]

# ========== РЕАЛЬНАЯ БАЗА СЛОВ OXFORD 5000 ==========
WORD_BASE = {
    "food": {
        "A1": [
            {"word": "apple", "translation": "яблоко"}, {"word": "banana", "translation": "банан"},
            {"word": "bread", "translation": "хлеб"}, {"word": "butter", "translation": "масло"},
            {"word": "cake", "translation": "торт"}, {"word": "cheese", "translation": "сыр"},
            {"word": "chicken", "translation": "курица"}, {"word": "coffee", "translation": "кофе"},
            {"word": "cookie", "translation": "печенье"}, {"word": "egg", "translation": "яйцо"},
            {"word": "fish", "translation": "рыба"}, {"word": "fruit", "translation": "фрукт"},
            {"word": "grape", "translation": "виноград"}, {"word": "honey", "translation": "мёд"},
            {"word": "juice", "translation": "сок"}, {"word": "meat", "translation": "мясо"},
            {"word": "milk", "translation": "молоко"}, {"word": "orange", "translation": "апельсин"},
            {"word": "pasta", "translation": "паста"}, {"word": "pizza", "translation": "пицца"},
            {"word": "rice", "translation": "рис"}, {"word": "salad", "translation": "салат"},
            {"word": "salt", "translation": "соль"}, {"word": "sandwich", "translation": "бутерброд"},
            {"word": "soup", "translation": "суп"}, {"word": "sugar", "translation": "сахар"},
            {"word": "tea", "translation": "чай"}, {"word": "water", "translation": "вода"},
            {"word": "yogurt", "translation": "йогурт"}, {"word": "beef", "translation": "говядина"},
            {"word": "pork", "translation": "свинина"}, {"word": "lamb", "translation": "баранина"},
            {"word": "turkey", "translation": "индейка"}, {"word": "ham", "translation": "ветчина"},
            {"word": "bacon", "translation": "бекон"}, {"word": "sausage", "translation": "колбаса"},
            {"word": "salmon", "translation": "лосось"}, {"word": "tuna", "translation": "тунец"},
            {"word": "shrimp", "translation": "креветка"}, {"word": "crab", "translation": "краб"},
            {"word": "mushroom", "translation": "гриб"}, {"word": "onion", "translation": "лук"},
            {"word": "garlic", "translation": "чеснок"}, {"word": "potato", "translation": "картофель"},
            {"word": "tomato", "translation": "помидор"}, {"word": "cucumber", "translation": "огурец"},
            {"word": "carrot", "translation": "морковь"}, {"word": "broccoli", "translation": "брокколи"},
            {"word": "cabbage", "translation": "капуста"}, {"word": "lettuce", "translation": "салат-латук"},
            {"word": "spinach", "translation": "шпинат"}, {"word": "pepper", "translation": "перец"},
            {"word": "olive", "translation": "оливка"}, {"word": "oil", "translation": "масло"},
            {"word": "vinegar", "translation": "уксус"}, {"word": "sauce", "translation": "соус"},
            {"word": "mustard", "translation": "горчица"}, {"word": "ketchup", "translation": "кетчуп"},
            {"word": "mayonnaise", "translation": "майонез"}, {"word": "flour", "translation": "мука"},
            {"word": "cereal", "translation": "хлопья"}, {"word": "oat", "translation": "овёс"},
            {"word": "corn", "translation": "кукуруза"}, {"word": "bean", "translation": "фасоль"},
            {"word": "pea", "translation": "горох"}, {"word": "nut", "translation": "орех"},
            {"word": "almond", "translation": "миндаль"}, {"word": "walnut", "translation": "грецкий орех"},
            {"word": "peanut", "translation": "арахис"}, {"word": "coconut", "translation": "кокос"},
            {"word": "chocolate", "translation": "шоколад"}, {"word": "candy", "translation": "конфета"},
            {"word": "biscuit", "translation": "печенье"}, {"word": "doughnut", "translation": "пончик"},
            {"word": "muffin", "translation": "кекс"}, {"word": "pancake", "translation": "блин"},
            {"word": "pie", "translation": "пирог"}, {"word": "pudding", "translation": "пудинг"},
            {"word": "jelly", "translation": "желе"}, {"word": "syrup", "translation": "сироп"},
            {"word": "cream", "translation": "сливки"}, {"word": "ice", "translation": "лёд"},
            {"word": "lemon", "translation": "лимон"}, {"word": "lime", "translation": "лайм"},
            {"word": "melon", "translation": "дыня"}, {"word": "watermelon", "translation": "арбуз"},
            {"word": "strawberry", "translation": "клубника"}, {"word": "raspberry", "translation": "малина"},
            {"word": "blueberry", "translation": "голубика"}, {"word": "cherry", "translation": "вишня"},
            {"word": "peach", "translation": "персик"}, {"word": "plum", "translation": "слива"},
            {"word": "apricot", "translation": "абрикос"}, {"word": "pear", "translation": "груша"},
            {"word": "pineapple", "translation": "ананас"}, {"word": "mango", "translation": "манго"},
            {"word": "kiwi", "translation": "киви"}, {"word": "avocado", "translation": "авокадо"},
            {"word": "pumpkin", "translation": "тыква"}, {"word": "zucchini", "translation": "цуккини"},
            {"word": "eggplant", "translation": "баклажан"}, {"word": "celery", "translation": "сельдерей"},
            {"word": "radish", "translation": "редис"}, {"word": "beetroot", "translation": "свёкла"},
            {"word": "asparagus", "translation": "спаржа"}, {"word": "artichoke", "translation": "артишок"},
            {"word": "leek", "translation": "лук-порей"}, {"word": "chive", "translation": "лук-резанец"},
            {"word": "parsley", "translation": "петрушка"}, {"word": "cilantro", "translation": "кинза"},
            {"word": "dill", "translation": "укроп"}, {"word": "basil", "translation": "базилик"},
            {"word": "oregano", "translation": "орегано"}, {"word": "thyme", "translation": "тимьян"},
            {"word": "rosemary", "translation": "розмарин"}, {"word": "mint", "translation": "мята"},
            {"word": "chili", "translation": "чили"}, {"word": "paprika", "translation": "паприка"},
            {"word": "cinnamon", "translation": "корица"}, {"word": "ginger", "translation": "имбирь"},
            {"word": "vanilla", "translation": "ваниль"}
        ],
        "A2": [
            {"word": "appetizer", "translation": "закуска"}, {"word": "beverage", "translation": "напиток"},
            {"word": "bite", "translation": "кусочек"}, {"word": "bitter", "translation": "горький"},
            {"word": "boil", "translation": "варить"}, {"word": "bake", "translation": "печь"},
            {"word": "fry", "translation": "жарить"}, {"word": "grill", "translation": "жарить на гриле"},
            {"word": "roast", "translation": "запекать"}, {"word": "steam", "translation": "готовить на пару"},
            {"word": "breakfast", "translation": "завтрак"}, {"word": "lunch", "translation": "обед"},
            {"word": "dinner", "translation": "ужин"}, {"word": "snack", "translation": "перекус"},
            {"word": "dessert", "translation": "десерт"}, {"word": "ingredient", "translation": "ингредиент"},
            {"word": "recipe", "translation": "рецепт"}, {"word": "taste", "translation": "вкус"},
            {"word": "flavor", "translation": "аромат"}, {"word": "spicy", "translation": "острый"},
            {"word": "sour", "translation": "кислый"}, {"word": "sweet", "translation": "сладкий"},
            {"word": "salty", "translation": "соленый"}, {"word": "fresh", "translation": "свежий"},
            {"word": "frozen", "translation": "замороженный"}, {"word": "raw", "translation": "сырой"},
            {"word": "cooked", "translation": "приготовленный"}, {"word": "delicious", "translation": "вкусный"},
            {"word": "hungry", "translation": "голодный"}, {"word": "thirsty", "translation": "испытывающий жажду"},
            {"word": "full", "translation": "сытый"}, {"word": "plate", "translation": "тарелка"},
            {"word": "bowl", "translation": "миска"}, {"word": "cup", "translation": "чашка"},
            {"word": "glass", "translation": "стакан"}, {"word": "fork", "translation": "вилка"},
            {"word": "knife", "translation": "нож"}, {"word": "spoon", "translation": "ложка"},
            {"word": "pan", "translation": "сковорода"}, {"word": "pot", "translation": "кастрюля"},
            {"word": "oven", "translation": "духовка"}, {"word": "microwave", "translation": "микроволновка"},
            {"word": "fridge", "translation": "холодильник"}, {"word": "freezer", "translation": "морозилка"},
            {"word": "cupboard", "translation": "шкаф"}, {"word": "kitchen", "translation": "кухня"},
            {"word": "dining room", "translation": "столовая"}
        ],
        "B1": [
            {"word": "cuisine", "translation": "кухня"}, {"word": "gourmet", "translation": "гурман"},
            {"word": "delicacy", "translation": "деликатес"}, {"word": "appetizing", "translation": "аппетитный"},
            {"word": "aromatic", "translation": "ароматный"}, {"word": "crispy", "translation": "хрустящий"},
            {"word": "creamy", "translation": "сливочный"}, {"word": "tender", "translation": "нежный"},
            {"word": "tough", "translation": "жесткий"}, {"word": "juicy", "translation": "сочный"},
            {"word": "ripe", "translation": "спелый"}, {"word": "rotten", "translation": "гнилой"},
            {"word": "stale", "translation": "черствый"}, {"word": "dough", "translation": "тесто"},
            {"word": "pastry", "translation": "выпечка"}, {"word": "yeast", "translation": "дрожжи"},
            {"word": "marinate", "translation": "мариновать"}, {"word": "season", "translation": "приправлять"},
            {"word": "garnish", "translation": "украшать"}, {"word": "whisk", "translation": "взбивать"},
            {"word": "knead", "translation": "месить"}, {"word": "roll", "translation": "раскатывать"},
            {"word": "slice", "translation": "нарезать ломтиками"}, {"word": "dice", "translation": "нарезать кубиками"},
            {"word": "chop", "translation": "рубить"}, {"word": "grate", "translation": "тереть"},
            {"word": "peel", "translation": "чистить"}, {"word": "core", "translation": "удалять сердцевину"},
            {"word": "drain", "translation": "сливать"}, {"word": "strain", "translation": "процеживать"},
            {"word": "mash", "translation": "разминать"}, {"word": "puree", "translation": "пюрировать"},
            {"word": "blend", "translation": "смешивать"}, {"word": "mix", "translation": "смешивать"},
            {"word": "stir", "translation": "размешивать"}, {"word": "beat", "translation": "взбивать"},
            {"word": "fold", "translation": "аккуратно перемешивать"}, {"word": "batter", "translation": "жидкое тесто"}
        ],
        "B2": [
            {"word": "gastronomy", "translation": "гастрономия"}, {"word": "culinary", "translation": "кулинарный"},
            {"word": "palate", "translation": "нёбо"}, {"word": "aftertaste", "translation": "послевкусие"},
            {"word": "fermentation", "translation": "ферментация"}, {"word": "infusion", "translation": "настой"},
            {"word": "emulsion", "translation": "эмульсия"}, {"word": "reduction", "translation": "выпаривание"},
            {"word": "caramelization", "translation": "карамелизация"}, {"word": "caramelize", "translation": "карамелизировать"},
            {"word": "carve", "translation": "нарезать мясо"}, {"word": "fillet", "translation": "филе"},
            {"word": "sirloin", "translation": "вырезка"}, {"word": "tenderloin", "translation": "филейная часть"},
            {"word": "brisket", "translation": "грудинка"}, {"word": "offal", "translation": "потроха"},
            {"word": "bouillon", "translation": "бульон"}, {"word": "consomme", "translation": "консоме"},
            {"word": "broth", "translation": "бульон"}, {"word": "stock", "translation": "основа"},
            {"word": "roux", "translation": "ру"}, {"word": "bechamel", "translation": "бешамель"},
            {"word": "hollandaise", "translation": "голландский соус"}, {"word": "pesto", "translation": "песто"},
            {"word": "aioli", "translation": "айоли"}, {"word": "tartare", "translation": "тартар"}
        ]
    }
}

# Добавляем темы (для остальных тем можно добавить аналогично)
# Здесь для краткости показана только тема "food"
# В полной версии будут все темы с таким же количеством слов

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
def highlight_word_mistake(user_word, correct_word):
    """Сравнивает написанное пользователем английское слово с правильным"""
    user_word = user_word.lower().strip()
    correct_word = correct_word.lower().strip()
    
    if user_word == correct_word:
        return None, True
    
    diff = []
    for i, (u, c) in enumerate(zip(user_word, correct_word)):
        if u != c:
            diff.append(f"позиция {i+1}: должно быть *{c}*, ты написала *{u}*")
    
    if len(user_word) > len(correct_word):
        diff.append(f"лишние символы в конце: *{user_word[len(correct_word):]}*")
    elif len(correct_word) > len(user_word):
        diff.append(f"не хватает: *{correct_word[len(user_word):]}*")
    
    return diff, False

# ========== ПРИВЕТСТВИЕ ==========
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    
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
• Ты пишешь слово на английском и перевод (например: apple — яблоко)  
• Я проверяю правописание английского слова и перевод  
• Если ошибёшься — покажу, где именно  
• Не знаешь слово? Нажми «❓ Не знаю»

После каждого задания ты сможешь:  
🔁 *Продолжить* — новое слово из той же темы и уровня  
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

# ========== НАЧАЛО АУДИРОВАНИЯ ==========
@bot.message_handler(func=lambda message: message.text == "👂 Начать аудирование")
def listening_mode(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(0, len(TOPICS), 2):
        if i+1 < len(TOPICS):
            markup.add(
                types.KeyboardButton(f"📚 {TOPICS[i]}"),
                types.KeyboardButton(f"📚 {TOPICS[i+1]}")
            )
        else:
            markup.add(types.KeyboardButton(f"📚 {TOPICS[i]}"))
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
    bot.send_message(message.chat.id, "📝 Напиши слово на английском и перевод через — (например: apple — яблоко):", reply_markup=markup)

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

# ========== ПРОВЕРКА ОТВЕТА ==========
@bot.message_handler(func=lambda message: user_data.get(message.from_user.id, {}).get("current_word") and message.text not in ["🏠 Главное меню", "🔁 Продолжить", "📂 Сменить тему", "📊 Сменить уровень", "❓ Не знаю", "👂 Начать аудирование"])
def check_answer(message):
    user_id = message.from_user.id
    word_data = user_data[user_id].get("current_word")
    
    if not word_data:
        return
    
    text = message.text.strip()
    correct_word = word_data["word"]
    correct_trans = word_data["translation"]
    
    # Парсим ответ пользователя
    if "—" in text:
        parts = text.split("—")
        user_word = parts[0].strip()
        user_trans = parts[1].strip()
    else:
        user_word = text
        user_trans = ""
    
    # Проверяем слово
    word_diff, word_ok = highlight_word_mistake(user_word, correct_word)
    
    # Проверяем перевод
    trans_ok = (user_trans.lower() == correct_trans.lower())
    
    # Формируем ответ
    response = ""
    
    if word_ok and trans_ok:
        response = f"✅ *Полностью верно!*\n\n{correct_word} — {correct_trans}"
    else:
        response = "❌ *Ошибки:*\n\n"
        
        if not word_ok:
            response += f"*В слове:*\n"
            response += f"Ты написала: {user_word}\n"
            response += f"Правильно: {correct_word}\n"
            if word_diff:
                response += "\n*Где ошибка:*\n" + "\n".join(word_diff) + "\n"
        
        if not trans_ok and user_trans:
            response += f"\n*В переводе:*\n"
            response += f"Твой перевод: {user_trans}\n"
            response += f"Правильный перевод: {correct_trans}\n"
    
    bot.send_message(message.chat.id, response, parse_mode="Markdown")
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
        bot.send_message(message.chat.id, "📝 Напиши слово на английском и перевод через — (например: apple — яблоко):", reply_markup=markup)

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
    bot.polling(none_stop=True)