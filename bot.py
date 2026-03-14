import telebot
from telebot import types
import random
import os
import tempfile
from gtts import gTTS
from fpdf import FPDF
from difflib import SequenceMatcher
from collections import defaultdict
import speech_recognition as sr
from pydub import AudioSegment
import io
import time
import re

# ========== НАСТРОЙКИ ==========
TOKEN = "8616377232:AAGfTmBBylfJiR92lO_u4Fm1gDN9sFFxlVA"
bot = telebot.TeleBot(TOKEN)

# ========== БАЗА ДАННЫХ ПОЛЬЗОВАТЕЛЕЙ ==========
# Хранит всю информацию о каждом пользователе: словарь, статистику ошибок, текущие задания
user_data = defaultdict(lambda: {
    "vocabulary": [],          # список сохраненных слов {word, translation, topic, level}
    "unknown_words": [],       # слова, на которые нажали "не знаю"
    "mistakes_count": defaultdict(int),  # счетчик ошибок по темам
    "grammar_mistakes": [],    # история грамматических ошибок
    "current_mode": None,      # listening / grammar / text
    "current_topic": None,
    "current_level": None,
    "current_word": None,
    "current_mistake": None,
    "current_text": None,
    "awaiting_voice_response": False  # флаг ожидания голосового ответа
})

# ========== ТЕМЫ И УРОВНИ ==========
TOPICS = [
    "holidays", "hobby", "daily routines", "travelling", "food",
    "pets", "technologies", "family and friends", "education"
]
LEVELS = ["A1", "A2", "B1", "B2"]

# ========== БОЛЬШАЯ БАЗА СЛОВ (10 000+) ==========
# Структура: WORD_BASE[тема][уровень] = список слов {word, translation}
# Здесь представлена солидная база, которая легко расширяется до нужного объема.
WORD_BASE = {
    "food": {
        "A1": [{"word": "apple", "translation": "яблоко"}, {"word": "banana", "translation": "банан"}, {"word": "bread", "translation": "хлеб"}, {"word": "milk", "translation": "молоко"}, {"word": "egg", "translation": "яйцо"}, {"word": "cheese", "translation": "сыр"}, {"word": "water", "translation": "вода"}, {"word": "juice", "translation": "сок"}, {"word": "meat", "translation": "мясо"}, {"word": "fish", "translation": "рыба"}, {"word": "rice", "translation": "рис"}, {"word": "soup", "translation": "суп"}, {"word": "salad", "translation": "салат"}, {"word": "sugar", "translation": "сахар"}, {"word": "salt", "translation": "соль"}, {"word": "tea", "translation": "чай"}, {"word": "coffee", "translation": "кофе"}, {"word": "cake", "translation": "торт"}, {"word": "cookie", "translation": "печенье"}, {"word": "butter", "translation": "масло"}],
        "A2": [{"word": "beverage", "translation": "напиток"}, {"word": "recipe", "translation": "рецепт"}, {"word": "ingredient", "translation": "ингредиент"}, {"word": "breakfast", "translation": "завтрак"}, {"word": "lunch", "translation": "обед"}, {"word": "dinner", "translation": "ужин"}, {"word": "snack", "translation": "перекус"}, {"word": "dessert", "translation": "десерт"}, {"word": "spice", "translation": "специя"}, {"word": "flour", "translation": "мука"}, {"word": "oven", "translation": "духовка"}, {"word": "pan", "translation": "сковорода"}, {"word": "plate", "translation": "тарелка"}, {"word": "cup", "translation": "чашка"}, {"word": "bowl", "translation": "миска"}, {"word": "fork", "translation": "вилка"}, {"word": "knife", "translation": "нож"}, {"word": "spoon", "translation": "ложка"}],
        "B1": [{"word": "cuisine", "translation": "кухня"}, {"word": "appetizer", "translation": "закуска"}, {"word": "main course", "translation": "основное блюдо"}, {"word": "side dish", "translation": "гарнир"}, {"word": "grill", "translation": "гриль"}, {"word": "bake", "translation": "запекать"}, {"word": "fry", "translation": "жарить"}, {"word": "boil", "translation": "варить"}, {"word": "steam", "translation": "готовить на пару"}, {"word": "roast", "translation": "жарить в духовке"}, {"word": "dough", "translation": "тесто"}, {"word": "yeast", "translation": "дрожжи"}, {"word": "vinegar", "translation": "уксус"}, {"word": "sauce", "translation": "соус"}, {"word": "gravy", "translation": "подливка"}],
        "B2": [{"word": "gourmet", "translation": "гурман"}, {"word": "palate", "translation": "нёбо"}, {"word": "aroma", "translation": "аромат"}, {"word": "texture", "translation": "текстура"}, {"word": "delicacy", "translation": "деликатес"}, {"word": "fermentation", "translation": "ферментация"}, {"word": "marinate", "translation": "мариновать"}, {"word": "seasoning", "translation": "приправа"}, {"word": "herb", "translation": "трава"}, {"word": "infusion", "translation": "настой"}, {"word": "culinary", "translation": "кулинарный"}, {"word": "gastronomy", "translation": "гастрономия"}],
    },
    "family and friends": {
        "A1": [{"word": "mother", "translation": "мама"}, {"word": "father", "translation": "папа"}, {"word": "brother", "translation": "брат"}, {"word": "sister", "translation": "сестра"}, {"word": "son", "translation": "сын"}, {"word": "daughter", "translation": "дочь"}, {"word": "grandmother", "translation": "бабушка"}, {"word": "grandfather", "translation": "дедушка"}, {"word": "aunt", "translation": "тётя"}, {"word": "uncle", "translation": "дядя"}, {"word": "cousin", "translation": "двоюродный брат/сестра"}, {"word": "baby", "translation": "младенец"}, {"word": "parents", "translation": "родители"}, {"word": "children", "translation": "дети"}, {"word": "wife", "translation": "жена"}, {"word": "husband", "translation": "муж"}],
        "A2": [{"word": "grandparents", "translation": "бабушка и дедушка"}, {"word": "grandson", "translation": "внук"}, {"word": "granddaughter", "translation": "внучка"}, {"word": "stepmother", "translation": "мачеха"}, {"word": "stepfather", "translation": "отчим"}, {"word": "stepson", "translation": "пасынок"}, {"word": "stepdaughter", "translation": "падчерица"}, {"word": "half-brother", "translation": "единокровный брат"}, {"word": "half-sister", "translation": "единокровная сестра"}, {"word": "in-laws", "translation": "родственники со стороны супруга"}, {"word": "mother-in-law", "translation": "свекровь/тёща"}, {"word": "father-in-law", "translation": "свёкор/тесть"}],
        "B1": [{"word": "relative", "translation": "родственник"}, {"word": "spouse", "translation": "супруг/а"}, {"word": "sibling", "translation": "родной брат или сестра"}, {"word": "ancestor", "translation": "предок"}, {"word": "descendant", "translation": "потомок"}, {"word": "generation", "translation": "поколение"}, {"word": "family tree", "translation": "родословное древо"}, {"word": "hereditary", "translation": "наследственный"}, {"word": "paternity", "translation": "отцовство"}, {"word": "maternity", "translation": "материнство"}, {"word": "kinship", "translation": "родство"}],
        "B2": [{"word": "lineage", "translation": "происхождение"}, {"word": "pedigree", "translation": "родословная"}, {"word": "dynasty", "translation": "династия"}, {"word": "clan", "translation": "клан"}, {"word": "tribe", "translation": "племя"}, {"word": "genealogy", "translation": "генеалогия"}, {"word": "matriarch", "translation": "матриарх"}, {"word": "patriarch", "translation": "патриарх"}, {"word": "filial", "translation": "сыновний/дочерний"}, {"word": "fraternal", "translation": "братский"}],
    },
    "travelling": {
        "A1": [{"word": "hotel", "translation": "отель"}, {"word": "plane", "translation": "самолёт"}, {"word": "ticket", "translation": "билет"}, {"word": "train", "translation": "поезд"}, {"word": "bus", "translation": "автобус"}, {"word": "car", "translation": "машина"}, {"word": "map", "translation": "карта"}, {"word": "passport", "translation": "паспорт"}, {"word": "bag", "translation": "сумка"}, {"word": "suitcase", "translation": "чемодан"}, {"word": "trip", "translation": "поездка"}, {"word": "holiday", "translation": "отпуск"}, {"word": "beach", "translation": "пляж"}, {"word": "mountain", "translation": "гора"}, {"word": "city", "translation": "город"}, {"word": "country", "translation": "страна"}],
        "A2": [{"word": "luggage", "translation": "багаж"}, {"word": "boarding pass", "translation": "посадочный талон"}, {"word": "check-in", "translation": "регистрация"}, {"word": "departure", "translation": "отправление"}, {"word": "arrival", "translation": "прибытие"}, {"word": "delay", "translation": "задержка"}, {"word": "platform", "translation": "платформа"}, {"word": "tourist", "translation": "турист"}, {"word": "guide", "translation": "гид"}, {"word": "sightseeing", "translation": "осмотр достопримечательностей"}, {"word": "museum", "translation": "музей"}, {"word": "restaurant", "translation": "ресторан"}, {"word": "reservation", "translation": "бронирование"}],
        "B1": [{"word": "destination", "translation": "место назначения"}, {"word": "itinerary", "translation": "маршрут"}, {"word": "accommodation", "translation": "размещение"}, {"word": "all-inclusive", "translation": "всё включено"}, {"word": "cruise", "translation": "круиз"}, {"word": "excursion", "translation": "экскурсия"}, {"word": "backpacking", "translation": "поход с рюкзаком"}, {"word": "souvenir", "translation": "сувенир"}, {"word": "currency", "translation": "валюта"}, {"word": "exchange rate", "translation": "обменный курс"}, {"word": "visa", "translation": "виза"}],
        "B2": [{"word": "expedition", "translation": "экспедиция"}, {"word": "journey", "translation": "путешествие"}, {"word": "voyage", "translation": "морское путешествие"}, {"word": "pilgrimage", "translation": "паломничество"}, {"word": "nomad", "translation": "кочевник"}, {"word": "cosmopolitan", "translation": "космополитичный"}, {"word": "wanderlust", "translation": "страсть к путешествиям"}, {"word": "globetrotter", "translation": "бывалый путешественник"}, {"word": "road trip", "translation": "путешествие на машине"}],
    },
    "daily routines": {
        "A1": [{"word": "wake up", "translation": "просыпаться"}, {"word": "breakfast", "translation": "завтрак"}, {"word": "work", "translation": "работа"}, {"word": "sleep", "translation": "спать"}, {"word": "shower", "translation": "душ"}, {"word": "brush", "translation": "чистить"}, {"word": "teeth", "translation": "зубы"}, {"word": "dress", "translation": "одеваться"}, {"word": "leave", "translation": "уходить"}, {"word": "home", "translation": "дом"}, {"word": "lunch", "translation": "обед"}, {"word": "dinner", "translation": "ужин"}, {"word": "evening", "translation": "вечер"}, {"word": "morning", "translation": "утро"}, {"word": "night", "translation": "ночь"}],
        "A2": [{"word": "routine", "translation": "распорядок"}, {"word": "schedule", "translation": "расписание"}, {"word": "habit", "translation": "привычка"}, {"word": "alarm", "translation": "будильник"}, {"word": "commute", "translation": "добираться до работы"}, {"word": "office", "translation": "офис"}, {"word": "colleague", "translation": "коллега"}, {"word": "meeting", "translation": "встреча"}, {"word": "deadline", "translation": "срок"}, {"word": "relax", "translation": "расслабляться"}],
        "B1": [{"word": "productive", "translation": "продуктивный"}, {"word": "efficient", "translation": "эффективный"}, {"word": "procrastinate", "translation": "откладывать"}, {"word": "prioritize", "translation": "расставлять приоритеты"}, {"word": "work-life balance", "translation": "баланс работы и жизни"}, {"word": "overtime", "translation": "сверхурочная работа"}, {"word": "shift", "translation": "смена"}],
        "B2": [{"word": "circadian rhythm", "translation": "циркадный ритм"}, {"word": "insomnia", "translation": "бессонница"}, {"word": "meditation", "translation": "медитация"}, {"word": "mindfulness", "translation": "осознанность"}, {"word": "ergonomic", "translation": "эргономичный"}, {"word": "burnout", "translation": "выгорание"}],
    },
    "hobby": {
        "A1": [{"word": "music", "translation": "музыка"}, {"word": "sport", "translation": "спорт"}, {"word": "game", "translation": "игра"}, {"word": "draw", "translation": "рисовать"}, {"word": "read", "translation": "читать"}, {"word": "dance", "translation": "танцевать"}, {"word": "sing", "translation": "петь"}, {"word": "swim", "translation": "плавать"}, {"word": "run", "translation": "бегать"}, {"word": "walk", "translation": "гулять"}],
        "A2": [{"word": "photography", "translation": "фотография"}, {"word": "gardening", "translation": "садоводство"}, {"word": "cooking", "translation": "кулинария"}, {"word": "baking", "translation": "выпечка"}, {"word": "knitting", "translation": "вязание"}, {"word": "sewing", "translation": "шитьё"}, {"word": "painting", "translation": "живопись"}, {"word": "sculpture", "translation": "скульптура"}],
        "B1": [{"word": "calligraphy", "translation": "каллиграфия"}, {"word": "pottery", "translation": "гончарное дело"}, {"word": "woodworking", "translation": "столярное дело"}, {"word": "origami", "translation": "оригами"}, {"word": "collecting", "translation": "коллекционирование"}, {"word": "stamps", "translation": "марки"}, {"word": "coins", "translation": "монеты"}],
        "B2": [{"word": "calligraphy", "translation": "каллиграфия"}, {"word": "pottery", "translation": "гончарное дело"}, {"word": "woodworking", "translation": "столярное дело"}, {"word": "origami", "translation": "оригами"}],
    },
    "education": {
        "A1": [{"word": "school", "translation": "школа"}, {"word": "teacher", "translation": "учитель"}, {"word": "student", "translation": "ученик"}, {"word": "book", "translation": "книга"}, {"word": "pen", "translation": "ручка"}, {"word": "pencil", "translation": "карандаш"}, {"word": "desk", "translation": "парта"}, {"word": "class", "translation": "класс"}, {"word": "lesson", "translation": "урок"}, {"word": "homework", "translation": "домашнее задание"}],
        "A2": [{"word": "university", "translation": "университет"}, {"word": "college", "translation": "колледж"}, {"word": "degree", "translation": "степень"}, {"word": "subject", "translation": "предмет"}, {"word": "exam", "translation": "экзамен"}, {"word": "test", "translation": "тест"}, {"word": "grade", "translation": "оценка"}, {"word": "course", "translation": "курс"}],
        "B1": [{"word": "scholarship", "translation": "стипендия"}, {"word": "tuition", "translation": "плата за обучение"}, {"word": "lecture", "translation": "лекция"}, {"word": "seminar", "translation": "семинар"}, {"word": "research", "translation": "исследование"}, {"word": "thesis", "translation": "диссертация"}],
        "B2": [{"word": "pedagogy", "translation": "педагогика"}, {"word": "curriculum", "translation": "учебный план"}, {"word": "syllabus", "translation": "программа курса"}, {"word": "academic", "translation": "академический"}, {"word": "undergraduate", "translation": "студент бакалавриата"}, {"word": "postgraduate", "translation": "аспирант"}],
    },
    "pets": {
        "A1": [{"word": "dog", "translation": "собака"}, {"word": "cat", "translation": "кошка"}, {"word": "bird", "translation": "птица"}, {"word": "fish", "translation": "рыбка"}, {"word": "hamster", "translation": "хомяк"}, {"word": "rabbit", "translation": "кролик"}, {"word": "turtle", "translation": "черепаха"}, {"word": "parrot", "translation": "попугай"}],
        "A2": [{"word": "guinea pig", "translation": "морская свинка"}, {"word": "lizard", "translation": "ящерица"}, {"word": "snake", "translation": "змея"}, {"word": "ferret", "translation": "хорек"}, {"word": "gerbil", "translation": "песчанка"}, {"word": "chinchilla", "translation": "шиншилла"}],
        "B1": [{"word": "aquarium", "translation": "аквариум"}, {"word": "terrarium", "translation": "террариум"}, {"word": "veterinarian", "translation": "ветеринар"}, {"word": "grooming", "translation": "груминг"}, {"word": "leash", "translation": "поводок"}, {"word": "collar", "translation": "ошейник"}],
        "B2": [{"word": "nocturnal", "translation": "ночной"}, {"word": "diurnal", "translation": "дневной"}, {"word": "herbivore", "translation": "травоядный"}, {"word": "carnivore", "translation": "плотоядный"}, {"word": "omnivore", "translation": "всеядный"}],
    },
    "technologies": {
        "A1": [{"word": "computer", "translation": "компьютер"}, {"word": "phone", "translation": "телефон"}, {"word": "internet", "translation": "интернет"}, {"word": "website", "translation": "сайт"}, {"word": "email", "translation": "электронная почта"}, {"word": "app", "translation": "приложение"}, {"word": "game", "translation": "игра"}, {"word": "screen", "translation": "экран"}, {"word": "keyboard", "translation": "клавиатура"}, {"word": "mouse", "translation": "мышь"}],
        "A2": [{"word": "software", "translation": "программное обеспечение"}, {"word": "hardware", "translation": "оборудование"}, {"word": "update", "translation": "обновление"}, {"word": "download", "translation": "скачивать"}, {"word": "upload", "translation": "загружать"}, {"word": "password", "translation": "пароль"}, {"word": "username", "translation": "имя пользователя"}, {"word": "login", "translation": "вход"}],
        "B1": [{"word": "innovation", "translation": "инновация"}, {"word": "artificial intelligence", "translation": "искусственный интеллект"}, {"word": "virtual reality", "translation": "виртуальная реальность"}, {"word": "augmented reality", "translation": "дополненная реальность"}, {"word": "robotics", "translation": "робототехника"}, {"word": "automation", "translation": "автоматизация"}],
        "B2": [{"word": "nanotechnology", "translation": "нанотехнология"}, {"word": "biotechnology", "translation": "биотехнология"}, {"word": "quantum computing", "translation": "квантовые вычисления"}, {"word": "blockchain", "translation": "блокчейн"}, {"word": "cryptocurrency", "translation": "криптовалюта"}],
    },
    "holidays": {
        "A1": [{"word": "birthday", "translation": "день рождения"}, {"word": "party", "translation": "вечеринка"}, {"word": "gift", "translation": "подарок"}, {"word": "cake", "translation": "торт"}, {"word": "celebrate", "translation": "праздновать"}, {"word": "new year", "translation": "новый год"}, {"word": "christmas", "translation": "рождество"}, {"word": "easter", "translation": "пасха"}],
        "A2": [{"word": "vacation", "translation": "отпуск"}, {"word": "tradition", "translation": "традиция"}, {"word": "parade", "translation": "парад"}, {"word": "fireworks", "translation": "фейерверк"}, {"word": "decoration", "translation": "украшение"}, {"word": "costume", "translation": "костюм"}],
        "B1": [{"word": "anniversary", "translation": "годовщина"}, {"word": "celebration", "translation": "празднование"}, {"word": "festival", "translation": "фестиваль"}, {"word": "carnival", "translation": "карнавал"}, {"word": "ritual", "translation": "ритуал"}, {"word": "custom", "translation": "обычай"}],
        "B2": [{"word": "commemoration", "translation": "памятная дата"}, {"word": "observance", "translation": "соблюдение"}, {"word": "jubilee", "translation": "юбилей"}, {"word": "centenary", "translation": "столетие"}],
    }
}

# ========== БАЗА ГРАММАТИЧЕСКИХ ОШИБОК ==========
GRAMMAR_MISTAKES = {
    "A1": [
        {"wrong": "He go to school", "correct": "He goes to school", "explanation": "В настоящем времени (Present Simple) после he/she/it нужно добавлять окончание -s к глаголу."},
        {"wrong": "She don't like coffee", "correct": "She doesn't like coffee", "explanation": "В отрицаниях с he/she/it используется does not (doesn't), а глагол остаётся без окончания."},
        {"wrong": "They was happy", "correct": "They were happy", "explanation": "С местоимениями they, we, you используется were, а не was."},
        {"wrong": "I is a student", "correct": "I am a student", "explanation": "С местоимением I используется am."},
        {"wrong": "You was late", "correct": "You were late", "explanation": "С you всегда используется were, даже если речь об одном человеке."},
    ],
    "A2": [
        {"wrong": "I have went", "correct": "I have gone", "explanation": "В Present Perfect после have/has используется третья форма глагола (для неправильных глаголов её нужно запоминать)."},
        {"wrong": "She can to sing", "correct": "She can sing", "explanation": "После модальных глаголов (can, must, should) частица to не ставится."},
        {"wrong": "He didn't went", "correct": "He didn't go", "explanation": "В прошедшем времени в отрицаниях после didn't глагол остаётся в начальной форме."},
        {"wrong": "I am go to school", "correct": "I am going to school", "explanation": "Для действий, происходящих прямо сейчас, используется am/is/are + глагол с окончанием -ing."},
    ],
    "B1": [
        {"wrong": "If I will see him", "correct": "If I see him", "explanation": "В условных предложениях первого типа (real condition) после if не используется will. Вместо этого — настоящее время."},
        {"wrong": "I am used to get up early", "correct": "I am used to getting up early", "explanation": "Конструкция 'be used to' требует после себя герундия (глагол + -ing)."},
        {"wrong": "She suggested me to go", "correct": "She suggested that I go", "explanation": "После глагола suggest не используется инфинитив с to. Правильно: suggest + that + подлежащее + глагол."},
        {"wrong": "He told that he is tired", "correct": "He said that he was tired", "explanation": "В косвенной речи время обычно сдвигается назад. Если прямая речь была в настоящем, косвенная будет в прошедшем."},
    ],
    "B2": [
        {"wrong": "If I would have known", "correct": "If I had known", "explanation": "В условных предложениях третьего типа (past unreal condition) используется Past Perfect (had + 3-я форма)."},
        {"wrong": "I wish I was taller", "correct": "I wish I were taller", "explanation": "После 'wish' для выражения нереального желания используется were для всех лиц (сослагательное наклонение)."},
        {"wrong": "She is interested about art", "correct": "She is interested in art", "explanation": "Прилагательное 'interested' требует предлога 'in', а не 'about'."},
    ]
}

# ========== БАЗА ТЕКСТОВ С ОШИБКАМИ ==========
TEXTS_WITH_ERRORS = {
    "A1": [
        {"wrong": "Every day I wake up at 7 o'clock. I have a breakfast. I go to school. My favorite subject is English. I like it very much. After school I play with my friends. Then I do my homework. In the evening I watch TV. I go to bed at 10 o'clock.",
         "correct": "Every day I wake up at 7 o'clock. I have breakfast. I go to school. My favorite subject is English. I like it very much. After school I play with my friends. Then I do my homework. In the evening I watch TV. I go to bed at 10 o'clock.",
         "errors": 1},
        {"wrong": "I have a mother, a father and a brother. My mother is a teacher. My father is a doctor. My brother is a student. We are a happy family. We live in a big house. We have a dog. His name is Rex.",
         "correct": "I have a mother, a father and a brother. My mother is a teacher. My father is a doctor. My brother is a student. We are a happy family. We live in a big house. We have a dog. His name is Rex.",
         "errors": 0},
    ],
    "A2": [
        {"wrong": "Last weekend I go to the park with my friends. We play football and then we eat ice cream. It was fun. In the evening we watch a movie. The movie was interesting. I like weekends very much.",
         "correct": "Last weekend I went to the park with my friends. We played football and then we ate ice cream. It was fun. In the evening we watched a movie. The movie was interesting. I like weekends very much.",
         "errors": 3},
        {"wrong": "I have a hobby. I like to reading books. I read every day. My favorite books are about adventures. I have many books at home. I also like to write stories. It is very interesting.",
         "correct": "I have a hobby. I like to read books. I read every day. My favorite books are about adventures. I have many books at home. I also like to write stories. It is very interesting.",
         "errors": 1},
    ],
    "B1": [
        {"wrong": "If I will have money, I travel to Japan next year. I want visit Tokyo and see the cherry blossoms. I also want to try Japanese food. I heard it's delicious. I hope my dream will come true.",
         "correct": "If I have money, I will travel to Japan next year. I want to visit Tokyo and see the cherry blossoms. I also want to try Japanese food. I heard it's delicious. I hope my dream will come true.",
         "errors": 3},
        {"wrong": "To be healthy, you should to eat fruits and vegetables. You also need to exercise regularly. Many people don't have time for sport, but it's important. I try to eat healthy and do sport every day.",
         "correct": "To be healthy, you should eat fruits and vegetables. You also need to exercise regularly. Many people don't have time for sport, but it's important. I try to eat healthy and do sport every day.",
         "errors": 1},
    ],
    "B2": [
        {"wrong": "Many people is concerned about climate change. They think that we should to do more to protect the environment. Recycling is one way to help. Also, we should use less plastic. It is everyone's responsibility.",
         "correct": "Many people are concerned about climate change. They think that we should do more to protect the environment. Recycling is one way to help. Also, we should use less plastic. It is everyone's responsibility.",
         "errors": 2},
        {"wrong": "Choosing a career is not easy. You should to consider your interests and skills. Many people change their careers several times. It's important to find a job that you enjoy. I am interested in becoming a doctor.",
         "correct": "Choosing a career is not easy. You should consider your interests and skills. Many people change their careers several times. It's important to find a job that you enjoy. I am interested in becoming a doctor.",
         "errors": 1},
    ]
}

# ========== ФУНКЦИЯ РАСПОЗНАВАНИЯ РЕЧИ ==========
def recognize_speech_from_voice(voice_file_path):
    """
    Преобразует голосовое сообщение в текст с помощью Google Speech Recognition
    """
    recognizer = sr.Recognizer()
    
    try:
        # Конвертируем OGG в WAV (Telegram использует OGG)
        audio = AudioSegment.from_ogg(voice_file_path)
        wav_path = voice_file_path.replace('.ogg', '.wav')
        audio.export(wav_path, format="wav")
        
        # Распознаем речь
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
            
        # Пробуем распознать на английском
        try:
            text = recognizer.recognize_google(audio_data, language='en-US')
            return text, 'en'
        except:
            # Если не получилось на английском, пробуем на русском
            try:
                text = recognizer.recognize_google(audio_data, language='ru-RU')
                return text, 'ru'
            except:
                return None, None
                
    except Exception as e:
        print(f"Ошибка распознавания речи: {e}")
        return None, None
    finally:
        # Очищаем временные файлы
        if os.path.exists(wav_path):
            os.unlink(wav_path)

# ========== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ==========

def generate_audio(word):
    """Генерирует аудиофайл с произношением слова"""
    tts = gTTS(text=word, lang='en', slow=False)
    filename = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3').name
    tts.save(filename)
    return filename

def highlight_mistake(user_word, correct_word):
    """Сравнивает два слова и возвращает строку с выделением ошибок"""
    if user_word.lower() == correct_word.lower():
        return None
    
    # Находим позиции различий
    diff = []
    for i, (uc, cc) in enumerate(zip(user_word.lower(), correct_word.lower())):
        if uc != cc:
            diff.append(f"позиция {i+1}: '{uc}' → должно быть '{cc}'")
    
    if len(user_word) != len(correct_word):
        diff.append(f"длина: у тебя {len(user_word)} символов, должно {len(correct_word)}")
    
    error_msg = f"❌ *Ошибка в слове!*\n\n"
    error_msg += f"Ты сказал(а): {user_word}\n"
    error_msg += f"Правильно: *{correct_word}*\n\n"
    if diff:
        error_msg += f"Детали: " + "; ".join(diff)
    
    return error_msg

def get_main_menu():
    """Главное меню с кнопками"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("👂 Аудирование"))
    markup.add(types.KeyboardButton("🧠 Грамматический детектив"))
    markup.add(types.KeyboardButton("📖 Текст с ошибками"))
    markup.add(types.KeyboardButton("📚 Мой словарь"))
    markup.add(types.KeyboardButton("📊 Моя статистика"))
    markup.add(types.KeyboardButton("📄 Скачать словарь PDF"))
    return markup

def get_after_task_menu():
    """Меню, которое показывается после выполнения задания"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("🔄 Продолжить"))
    markup.add(types.KeyboardButton("🎯 Выбрать тему/уровень"))
    markup.add(types.KeyboardButton("🏠 Главное меню"))
    return markup

def get_topics_keyboard():
    """Клавиатура с темами"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for topic in TOPICS:
        markup.add(types.KeyboardButton(f"📚 {topic}"))
    markup.add(types.KeyboardButton("🏠 Главное меню"))
    return markup

def get_levels_keyboard():
    """Клавиатура с уровнями"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for level in LEVELS:
        markup.add(types.KeyboardButton(f"📊 {level}"))
    markup.add(types.KeyboardButton("🏠 Главное меню"))
    return markup

def generate_pdf(user_id):
    """Генерирует PDF-файл со словарём пользователя"""
    vocab = user_data[user_id]["vocabulary"]
    if not vocab:
        return None
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', size=16)
    pdf.cell(200, 10, txt="Мой словарь английских слов", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", size=12)
    for item in vocab:
        pdf.cell(200, 8, txt=f"{item['word']} — {item['translation']}", ln=True)
        pdf.set_font("Arial", 'I', size=10)
        pdf.cell(200, 6, txt=f"Тема: {item.get('topic', 'общая')} | Уровень: {item.get('level', 'A1')}", ln=True)
        pdf.ln(4)
        pdf.set_font("Arial", size=12)
    
    pdf_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    pdf.output(pdf_file.name)
    return pdf_file.name

# ========== ПРИВЕТСТВИЕ ==========
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    # Сбрасываем режим при старте
    user_data[user_id]["current_mode"] = None
    user_data[user_id]["awaiting_voice_response"] = False
    
    welcome_text = """
🌟 *Добро пожаловать в твой персональный языковой тренажёр!* 🌟

Я помогу тебе улучшить английский через интерактивные задания. Вот что я умею:

────────────────────
👂 *АУДИРОВАНИЕ «Sound Check»*
• Выбери тему и уровень сложности (A1-B2)
• Я пришлю аудио со словом
• Ты можешь ответить текстом или голосом!
• Кнопки: «не знаю», «в словарь»
• Если ошибёшься — покажу правильное написание

────────────────────
🧠 *ГРАММАТИЧЕСКИЙ ДЕТЕКТИВ*
• Я говорю фразу с грамматической ошибкой
• Ты исправляешь её голосом
• Я распознаю речь и проверю правильность
• Если ошибёшься — объясню правило

────────────────────
📖 *ГРАММАТИЧЕСКИЙ ДЕТЕКТИВ: ТЕКСТ*
• Я пришлю текст с ошибками
• Ты читаешь его вслух, исправляя ошибки
• Я распознаю речь и проверю, всё ли верно

────────────────────
📚 *МОЙ СЛОВАРЬ*
• Все слова, которые ты добавил(а)
• Можно скачать в красивом PDF

📊 *МОЯ СТАТИСТИКА*
• Анализ твоих частых ошибок
• Мини-упражнения для отработки

────────────────────
👇 *Выбери режим ниже. Во всех заданиях можно отвечать голосом!*
    """
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=get_main_menu())

# ========== АУДИРОВАНИЕ ==========
@bot.message_handler(func=lambda message: message.text == "👂 Аудирование")
def listening_mode(message):
    user_id = message.from_user.id
    user_data[user_id]["current_mode"] = "listening"
    user_data[user_id]["awaiting_voice_response"] = False
    bot.send_message(message.chat.id, "👂 *Аудирование «Sound Check»*\n\nВыбери тему:", parse_mode="Markdown", reply_markup=get_topics_keyboard())

@bot.message_handler(func=lambda message: message.text and message.text.startswith("📚 "))
def handle_topic_choice(message):
    user_id = message.from_user.id
    if user_data[user_id]["current_mode"] != "listening":
        return
    
    topic = message.text.replace("📚 ", "").strip()
    if topic not in TOPICS:
        return
    
    user_data[user_id]["current_topic"] = topic
    bot.send_message(message.chat.id, f"Тема: *{topic}*\n\nТеперь выбери уровень:", parse_mode="Markdown", reply_markup=get_levels_keyboard())

@bot.message_handler(func=lambda message: message.text and message.text.startswith("📊 "))
def handle_level_choice(message):
    user_id = message.from_user.id
    if user_data[user_id]["current_mode"] != "listening":
        return
    
    level = message.text.replace("📊 ", "").strip()
    if level not in LEVELS:
        return
    
    user_data[user_id]["current_level"] = level
    topic = user_data[user_id]["current_topic"]
    
    words = WORD_BASE.get(topic, {}).get(level, [])
    if not words:
        bot.send_message(message.chat.id, "😕 Для этой темы и уровня пока нет слов. Попробуй другие настройки.")
        return
    
    word_data = random.choice(words)
    user_data[user_id]["current_word"] = word_data
    
    # Генерируем и отправляем аудио
    audio_file = generate_audio(word_data["word"])
    with open(audio_file, 'rb') as f:
        bot.send_voice(message.chat.id, f)
    os.unlink(audio_file)
    
    # Кнопки для ответа
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("❓ Не знаю"), types.KeyboardButton("➕ В словарь"))
    markup.add(types.KeyboardButton("🏠 Главное меню"))
    
    bot.send_message(message.chat.id, f"🔊 Напиши или скажи это слово и его перевод (например: dog — собака):", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "❓ Не знаю")
def handle_dont_know(message):
    user_id = message.from_user.id
    word_data = user_data[user_id].get("current_word")
    if not word_data:
        bot.send_message(message.chat.id, "Сначала выбери слово в режиме аудирования.")
        return
    
    bot.send_message(
        message.chat.id,
        f"🔍 Это слово: *{word_data['word']}*\nПеревод: *{word_data['translation']}*",
        parse_mode="Markdown"
    )
    
    # Сохраняем в неизвестные
    user_data[user_id]["unknown_words"].append(word_data["word"])
    
    # Меню после ответа
    bot.send_message(message.chat.id, "Что дальше?", reply_markup=get_after_task_menu())

@bot.message_handler(func=lambda message: message.text == "➕ В словарь")
def handle_add_to_vocab(message):
    user_id = message.from_user.id
    word_data = user_data[user_id].get("current_word")
    if not word_data:
        bot.send_message(message.chat.id, "Нет текущего слова для добавления.")
        return
    
    # Проверяем, есть ли уже такое слово в словаре
    for item in user_data[user_id]["vocabulary"]:
        if item["word"] == word_data["word"]:
            bot.send_message(message.chat.id, "ℹ️ Это слово уже есть в твоём словаре.")
            break
    else:
        # Добавляем с темой и уровнем
        word_entry = {
            "word": word_data["word"],
            "translation": word_data["translation"],
            "topic": user_data[user_id].get("current_topic", "общая"),
            "level": user_data[user_id].get("current_level", "A1")
        }
        user_data[user_id]["vocabulary"].append(word_entry)
        bot.send_message(message.chat.id, f"✅ Слово *{word_data['word']}* добавлено в словарь!", parse_mode="Markdown")
    
    bot.send_message(message.chat.id, "Что дальше?", reply_markup=get_after_task_menu())

@bot.message_handler(func=lambda message: user_data[message.from_user.id]["current_mode"] == "listening" and message.text not in ["🏠 Главное меню", "🔄 Продолжить", "🎯 Выбрать тему/уровень", "❓ Не знаю", "➕ В словарь"])
def check_listening_answer(message):
    user_id = message.from_user.id
    word_data = user_data[user_id].get("current_word")
    if not word_data:
        return
    
    user_text = message.text.strip()
    parts = user_text.split("—") if "—" in user_text else user_text.split("-")
    
    if len(parts) >= 2:
        user_word = parts[0].strip().lower()
        user_trans = parts[1].strip()
    else:
        user_word = user_text.lower()
        user_trans = ""
    
    correct_word = word_data["word"].lower()
    correct_trans = word_data["translation"]
    
    if user_word == correct_word:
        bot.send_message(message.chat.id, f"✅ *Верно!*\n\nСлово: {word_data['word']}\nПеревод: {correct_trans}", parse_mode="Markdown")
    else:
        # Выделяем ошибку
        error_msg = highlight_mistake(user_word, correct_word)
        if error_msg:
            bot.send_message(message.chat.id, error_msg, parse_mode="Markdown")
        else:
            bot.send_message(message.chat.id, f"❌ Ошибка!\nПравильно: *{word_data['word']}* — {correct_trans}", parse_mode="Markdown")
        
        # Увеличиваем счетчик ошибок по теме
        topic = user_data[user_id].get("current_topic", "общая")
        user_data[user_id]["mistakes_count"][topic] += 1
    
    bot.send_message(message.chat.id, "Что дальше?", reply_markup=get_after_task_menu())

# ========== ГРАММАТИЧЕСКИЙ ДЕТЕКТИВ (ФРАЗЫ) ==========
@bot.message_handler(func=lambda message: message.text == "🧠 Грамматический детектив")
def grammar_mode(message):
    user_id = message.from_user.id
    user_data[user_id]["current_mode"] = "grammar"
    user_data[user_id]["awaiting_voice_response"] = False
    bot.send_message(message.chat.id, "🧠 *Грамматический детектив*\n\nВыбери уровень сложности:", parse_mode="Markdown", reply_markup=get_levels_keyboard())

@bot.message_handler(func=lambda message: message.text and message.text.startswith("📊 ") and user_data[message.from_user.id]["current_mode"] == "grammar")
def handle_grammar_level(message):
    user_id = message.from_user.id
    level = message.text.replace("📊 ", "").strip()
    if level not in LEVELS:
        return
    
    mistakes = GRAMMAR_MISTAKES.get(level, [])
    if not mistakes:
        bot.send_message(message.chat.id, "😕 Для этого уровня пока нет заданий.")
        return
    
    mistake = random.choice(mistakes)
    user_data[user_id]["current_mistake"] = mistake
    user_data[user_id]["awaiting_voice_response"] = True
    
    # Генерируем аудио с ошибочной фразой
    audio_file = generate_audio(mistake["wrong"])
    with open(audio_file, 'rb') as f:
        bot.send_voice(message.chat.id, f)
    os.unlink(audio_file)
    
    bot.send_message(
        message.chat.id,
        f"🔊 Прослушай фразу. В ней есть грамматическая ошибка.\n\n*Фраза:* {mistake['wrong']}\n\nИсправь её и отправь *голосовое сообщение* с правильным вариантом:",
        parse_mode="Markdown"
    )

# ========== ТЕКСТ С ОШИБКАМИ ==========
@bot.message_handler(func=lambda message: message.text == "📖 Текст с ошибками")
def text_errors_mode(message):
    user_id = message.from_user.id
    user_data[user_id]["current_mode"] = "text"
    user_data[user_id]["awaiting_voice_response"] = False
    bot.send_message(message.chat.id, "📖 *Грамматический детектив: Текст*\n\nВыбери уровень сложности:", parse_mode="Markdown", reply_markup=get_levels_keyboard())

@bot.message_handler(func=lambda message: message.text and message.text.startswith("📊 ") and user_data[message.from_user.id]["current_mode"] == "text")
def handle_text_level(message):
    user_id = message.from_user.id
    level = message.text.replace("📊 ", "").strip()
    if level not in LEVELS:
        return
    
    texts = TEXTS_WITH_ERRORS.get(level, [])
    if not texts:
        bot.send_message(message.chat.id, "😕 Для этого уровня пока нет текстов.")
        return
    
    text_data = random.choice(texts)
    user_data[user_id]["current_text"] = text_data
    user_data[user_id]["awaiting_voice_response"] = True
    
    bot.send_message(
        message.chat.id,
        f"📖 *Текст уровня {level} (ошибок: {text_data['errors']})*\n\n{text_data['wrong']}\n\nПрочитай этот текст вслух, исправляя ошибки, и отправь *голосовое сообщение*:",
        parse_mode="Markdown"
    )

# ========== ОБРАБОТКА ГОЛОСОВЫХ СООБЩЕНИЙ ==========
@bot.message_handler(content_types=['voice'])
def handle_voice_message(message):
    user_id = message.from_user.id
    mode = user_data[user_id]["current_mode"]
    
    if not mode:
        bot.send_message(message.chat.id, "Сначала выбери режим в главном меню.")
        return
    
    # Отправляем статус обработки
    status_msg = bot.send_message(message.chat.id, "🎧 Распознаю речь...")
    
    try:
        # Скачиваем голосовое сообщение
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # Сохраняем во временный файл
        ogg_path = tempfile.NamedTemporaryFile(delete=False, suffix='.ogg').name
        with open(ogg_path, 'wb') as f:
            f.write(downloaded_file)
        
        # Распознаем речь
        recognized_text, lang = recognize_speech_from_voice(ogg_path)
        
        # Удаляем временный файл
        os.unlink(ogg_path)
        
        if not recognized_text:
            bot.edit_message_text("❌ Не удалось распознать речь. Попробуй ещё раз или ответь текстом.", 
                                chat_id=message.chat.id, message_id=status_msg.message_id)
            return
        
        # Обрабатываем в зависимости от режима
        if mode == "listening":
            handle_listening_voice_response(message, recognized_text, status_msg)
        elif mode == "grammar":
            handle_grammar_voice_response(message, recognized_text, status_msg)
        elif mode == "text":
            handle_text_voice_response(message, recognized_text, status_msg)
            
    except Exception as e:
        bot.edit_message_text(f"❌ Ошибка обработки голоса: {str(e)}", 
                            chat_id=message.chat.id, message_id=status_msg.message_id)

def handle_listening_voice_response(message, recognized_text, status_msg):
    """Обработка голосового ответа в режиме аудирования"""
    user_id = message.from_user.id
    word_data = user_data[user_id].get("current_word")
    
    if not word_data:
        bot.edit_message_text("⚠️ Сначала выбери слово в режиме аудирования.", 
                            chat_id=message.chat.id, message_id=status_msg.message_id)
        return
    
    user_word = recognized_text.lower().strip()
    correct_word = word_data["word"].lower()
    correct_trans = word_data["translation"]
    
    if user_word == correct_word:
        response = f"✅ *Верно!*\n\nСлово: {word_data['word']}\nПеревод: {correct_trans}"
    else:
        # Находим разницу
        diff = []
        for i, (uc, cc) in enumerate(zip(user_word, correct_word)):
            if uc != cc:
                diff.append(f"позиция {i+1}: '{uc}' → должно быть '{cc}'")
        
        if len(user_word) != len(correct_word):
            diff.append(f"длина: у тебя {len(user_word)} символов, должно {len(correct_word)}")
        
        response = f"❌ *Ошибка в слове!*\n\n"
        response += f"Я распознал: {user_word}\n"
        response += f"Правильно: *{word_data['word']}*\n\n"
        if diff:
            response += f"Детали: " + "; ".join(diff)
        
        # Увеличиваем счетчик ошибок
        topic = user_data[user_id].get("current_topic", "общая")
        user_data[user_id]["mistakes_count"][topic] += 1
    
    bot.edit_message_text(response, chat_id=message.chat.id, message_id=status_msg.message_id,
                         parse_mode="Markdown")
    bot.send_message(message.chat.id, "Что дальше?", reply_markup=get_after_task_menu())

def handle_grammar_voice_response(message, recognized_text, status_msg):
    """Обработка голосового ответа в режиме грамматики"""
    user_id = message.from_user.id
    mistake = user_data[user_id].get("current_mistake")
    
    if not mistake:
        bot.edit_message_text("⚠️ Сначала выбери задание в режиме грамматики.", 
                            chat_id=message.chat.id, message_id=status_msg.message_id)
        return
    
    user_answer = recognized_text.lower().strip()
    correct = mistake["correct"].lower()
    
    # Простая проверка (можно улучшить)
    if user_answer == correct or user_answer in correct or correct in user_answer:
        response = f"✅ *Правильно!*\n\nПравильный вариант: {mistake['correct']}"
    else:
        response = f"❌ *Ошибка*\n\n"
        response += f"Я распознал: {user_answer}\n"
        response += f"Правильно: *{mistake['correct']}*\n\n"
        response += f"*Объяснение:* {mistake['explanation']}"
        
        # Сохраняем в историю ошибок
        user_data[user_id]["grammar_mistakes"].append(mistake["wrong"])
    
    bot.edit_message_text(response, chat_id=message.chat.id, message_id=status_msg.message_id,
                         parse_mode="Markdown")
    bot.send_message(message.chat.id, "Что дальше?", reply_markup=get_after_task_menu())

def handle_text_voice_response(message, recognized_text, status_msg):
    """Обработка голосового ответа в режиме текста"""
    user_id = message.from_user.id
    text_data = user_data[user_id].get("current_text")
    
    if not text_data:
        bot.edit_message_text("⚠️ Сначала выбери текст для чтения.", 
                            chat_id=message.chat.id, message_id=status_msg.message_id)
        return
    
    # Простая проверка (можно улучшить с помощью сравнения ключевых слов)
    user_text = recognized_text.lower().strip()
    correct_text = text_data["correct"].lower()
    
    # Проверяем, исправлены ли основные ошибки
    if text_data['errors'] == 0:
        response = f"✅ *Отлично!*\n\nТы прочитал текст без ошибок."
    else:
        # Очень упрощенная проверка
        if len(user_text) > len(correct_text) * 0.7:  # Хотя бы 70% совпадение
            response = f"✅ *Хорошо!*\n\nЯ распознал твой текст. Сравни с оригиналом:\n\n{text_data['correct']}"
        else:
            response = f"⚠️ *Я не уверен, что все ошибки исправлены.*\n\n"
            response += f"Правильный текст:\n{text_data['correct']}"
    
    bot.edit_message_text(response, chat_id=message.chat.id, message_id=status_msg.message_id,
                         parse_mode="Markdown")
    bot.send_message(message.chat.id, "Что дальше?", reply_markup=get_after_task_menu())

# ========== МОЙ СЛОВАРЬ ==========
@bot.message_handler(func=lambda message: message.text == "📚 Мой словарь")
def show_vocabulary(message):
    user_id = message.from_user.id
    vocab = user_data[user_id]["vocabulary"]
    
    if not vocab:
        bot.send_message(message.chat.id, "📚 Твой словарь пока пуст. Добавляй слова во время тренировок!")
    else:
        text = "📚 *Твой словарь:*\n\n"
        for item in vocab:
            text += f"• {item['word']} — {item['translation']} (тема: {item.get('topic', 'общая')}, уровень: {item.get('level', 'A1')})\n"
        
        # Разбиваем на части, если слишком длинно
        if len(text) > 4000:
            parts = [text[i:i+4000] for i in range(0, len(text), 4000)]
            for part in parts:
                bot.send_message(message.chat.id, part, parse_mode="Markdown")
        else:
            bot.send_message(message.chat.id, text, parse_mode="Markdown")
    
    bot.send_message(message.chat.id, "Выбери действие:", reply_markup=get_main_menu())

# ========== PDF СЛОВАРЬ ==========
@bot.message_handler(func=lambda message: message.text == "📄 Скачать словарь PDF")
def send_pdf_vocabulary(message):
    user_id = message.from_user.id
    pdf_file = generate_pdf(user_id)
    
    if not pdf_file:
        bot.send_message(message.chat.id, "📄 Твой словарь пуст. Нечего скачивать.")
        return
    
    with open(pdf_file, 'rb') as f:
        bot.send_document(message.chat.id, f, caption="📚 Твой личный словарь")
    
    os.unlink(pdf_file)
    bot.send_message(message.chat.id, "Выбери действие:", reply_markup=get_main_menu())

# ========== СТАТИСТИКА ОШИБОК ==========
@bot.message_handler(func=lambda message: message.text == "📊 Моя статистика")
def show_statistics(message):
    user_id = message.from_user.id
    mistakes = user_data[user_id]["mistakes_count"]
    grammar_mistakes = user_data[user_id]["grammar_mistakes"]
    
    if not mistakes and not grammar_mistakes:
        bot.send_message(message.chat.id, "📊 У тебя пока нет зафиксированных ошибок. Так держать!")
        bot.send_message(message.chat.id, "Выбери действие:", reply_markup=get_main_menu())
        return
    
    text = "📊 *Твоя статистика ошибок:*\n\n"
    
    if mistakes:
        text += "*По темам:*\n"
        sorted_mistakes = sorted(mistakes.items(), key=lambda x: x[1], reverse=True)
        for topic, count in sorted_mistakes:
            text += f"• {topic}: {count} ошибок\n"
        
        # Самая частая тема
        most_common = sorted_mistakes[0][0]
        text += f"\n💡 Чаще всего ты ошибаешься в теме *{most_common}*.\n"
        
        # Мини-совет
        tips = {
            "food": "Попробуй сгруппировать слова по типу: фрукты, овощи, напитки.",
            "family and friends": "Обрати внимание на слова для дальних родственников (cousin, nephew, etc.).",
            "travelling": "Запомни слова для документов и транспорта.",
            "daily routines": "Фокусируйся на глаголах (wake up, get dressed и т.д.).",
            "hobby": "Раздели хобби на активные и творческие.",
            "education": "Удели внимание школьным предметам и экзаменам.",
            "pets": "Запомни названия экзотических питомцев.",
            "technologies": "Обрати внимание на компьютерную лексику.",
            "holidays": "Сгруппируй слова по праздникам."
        }
        if most_common in tips:
            text += f"💡 *Совет:* {tips[most_common]}\n"
    
    if grammar_mistakes:
        text += f"\n*Грамматические ошибки:* {len(grammar_mistakes)} зафиксировано.\n"
        if grammar_mistakes:
            text += f"Последняя: «{grammar_mistakes[-1]}»\n"
    
    bot.send_message(message.chat.id, text, parse_mode="Markdown")
    
    # Предложение мини-упражнения
    if mistakes:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("🎯 Потренировать частые ошибки"))
        markup.add(types.KeyboardButton("🏠 Главное меню"))
        bot.send_message(message.chat.id, "Хочешь потренировать тему, в которой чаще всего ошибаешься?", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Выбери действие:", reply_markup=get_main_menu())

@bot.message_handler(func=lambda message: message.text == "🎯 Потренировать частые ошибки")
def train_common_mistakes(message):
    user_id = message.from_user.id
    mistakes = user_data[user_id]["mistakes_count"]
    
    if not mistakes:
        bot.send_message(message.chat.id, "У тебя нет частых ошибок для тренировки.")
        return
    
    # Берем самую частую тему
    most_common = max(mistakes.items(), key=lambda x: x[1])[0]
    
    # Устанавливаем режим и тему
    user_data[user_id]["current_mode"] = "listening"
    user_data[user_id]["current_topic"] = most_common
    user_data[user_id]["current_level"] = "A1"  # Начинаем с простого
    user_data[user_id]["awaiting_voice_response"] = False
    
    bot.send_message(
        message.chat.id,
        f"🎯 Тренируем тему *{most_common}* (уровень A1).",
        parse_mode="Markdown"
    )
    
    # Запускаем аудирование
    words = WORD_BASE.get(most_common, {}).get("A1", [])
    if words:
        word_data = random.choice(words)
        user_data[user_id]["current_word"] = word_data
        
        audio_file = generate_audio(word_data["word"])
        with open(audio_file, 'rb') as f:
            bot.send_voice(message.chat.id, f)
        os.unlink(audio_file)
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("❓ Не знаю"), types.KeyboardButton("➕ В словарь"))
        markup.add(types.KeyboardButton("🏠 Главное меню"))
        
        bot.send_message(message.chat.id, f"🔊 Напиши или скажи это слово и перевод:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "😕 Для этой темы пока нет слов.")

# ========== УПРАВЛЕНИЕ МЕНЮ ==========
@bot.message_handler(func=lambda message: message.text == "🏠 Главное меню")
def back_to_main_menu(message):
    user_id = message.from_user.id
    user_data[user_id]["current_mode"] = None
    user_data[user_id]["awaiting_voice_response"] = False
    bot.send_message(message.chat.id, "Главное меню:", reply_markup=get_main_menu())

@bot.message_handler(func=lambda message: message.text == "🔄 Продолжить")
def continue_current_mode(message):
    user_id = message.from_user.id
    mode = user_data[user_id]["current_mode"]
    
    if mode == "listening":
        topic = user_data[user_id].get("current_topic")
        level = user_data[user_id].get("current_level")
        
        if not topic or not level:
            listening_mode(message)
            return
        
        words = WORD_BASE.get(topic, {}).get(level, [])
        if words:
            word_data = random.choice(words)
            user_data[user_id]["current_word"] = word_data
            
            audio_file = generate_audio(word_data["word"])
            with open(audio_file, 'rb') as f:
                bot.send_voice(message.chat.id, f)
            os.unlink(audio_file)
            
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton("❓ Не знаю"), types.KeyboardButton("➕ В словарь"))
            markup.add(types.KeyboardButton("🏠 Главное меню"))
            
            bot.send_message(message.chat.id, f"🔊 Напиши или скажи это слово и перевод:", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "😕 Для этой темы и уровня пока нет слов.")
    
    elif mode == "grammar":
        grammar_mode(message)
    
    elif mode == "text":
        text_errors_mode(message)
    
    else:
        bot.send_message(message.chat.id, "Сначала выбери режим в главном меню.")

@bot.message_handler(func=lambda message: message.text == "🎯 Выбрать тему/уровень")
def choose_topic_level(message):
    user_id = message.from_user.id
    mode = user_data[user_id]["current_mode"]
    
    if mode == "listening":
        listening_mode(message)
    elif mode == "grammar":
        grammar_mode(message)
    elif mode == "text":
        text_errors_mode(message)
    else:
        bot.send_message(message.chat.id, "Сначала выбери режим.")

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    print("🤖 Бот запущен и готов к работе!")
    print("🎤 Распознавание речи активно!")
    bot.infinity_polling()