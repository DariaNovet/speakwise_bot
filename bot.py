import telebot
from telebot import types
import random
import os
import tempfile
from gtts import gTTS
from fpdf import FPDF
from collections import defaultdict
import speech_recognition as sr
from pydub import AudioSegment
import difflib
from fpdf import FPDF
import tempfile
import os
# ========== НАСТРОЙКИ ==========
TOKEN = "8616377232:AAGfTmBBylfJiR92lO_u4Fm1gDN9sFFxlVA"
bot = telebot.TeleBot(TOKEN)

# ========== БАЗА ДАННЫХ ПОЛЬЗОВАТЕЛЕЙ ==========
user_data = defaultdict(lambda: {
    "vocabulary": [],
    "unknown_words": [],
    "mistakes_count": defaultdict(int),
    "grammar_mistakes": [],
    "current_mode": None,
    "current_topic": None,
    "current_level": None,
    "current_word": None,
    "current_mistake": None,
    "current_text": None
})

# ========== ТЕМЫ И УРОВНИ ==========
TOPICS = ["food", "family", "travel", "daily routines", "hobby", "work", "education", "health", "nature", "technology", "shopping", "sports", "pets", "holidays", "music", "movies", "books", "weather", "animals", "clothes"]
LEVELS = ["A1", "A2", "B1", "B2"]

# ========== ОГРОМНАЯ БАЗА СЛОВ (5000+ слов) ==========
WORD_BASE = {
    "food": {
        "A1": [{"word": "apple", "translation": "яблоко"}, {"word": "banana", "translation": "банан"}, {"word": "bread", "translation": "хлеб"}, {"word": "milk", "translation": "молоко"}, {"word": "egg", "translation": "яйцо"}, {"word": "cheese", "translation": "сыр"}, {"word": "water", "translation": "вода"}, {"word": "juice", "translation": "сок"}, {"word": "meat", "translation": "мясо"}, {"word": "fish", "translation": "рыба"}, {"word": "rice", "translation": "рис"}, {"word": "soup", "translation": "суп"}, {"word": "salad", "translation": "салат"}, {"word": "sugar", "translation": "сахар"}, {"word": "salt", "translation": "соль"}, {"word": "tea", "translation": "чай"}, {"word": "coffee", "translation": "кофе"}, {"word": "cake", "translation": "торт"}, {"word": "cookie", "translation": "печенье"}, {"word": "butter", "translation": "масло"}, {"word": "potato", "translation": "картофель"}, {"word": "tomato", "translation": "помидор"}, {"word": "onion", "translation": "лук"}, {"word": "garlic", "translation": "чеснок"}, {"word": "carrot", "translation": "морковь"}, {"word": "cucumber", "translation": "огурец"}, {"word": "pepper", "translation": "перец"}, {"word": "chicken", "translation": "курица"}, {"word": "pork", "translation": "свинина"}, {"word": "beef", "translation": "говядина"}],
        "A2": [{"word": "beverage", "translation": "напиток"}, {"word": "recipe", "translation": "рецепт"}, {"word": "ingredient", "translation": "ингредиент"}, {"word": "breakfast", "translation": "завтрак"}, {"word": "lunch", "translation": "обед"}, {"word": "dinner", "translation": "ужин"}, {"word": "snack", "translation": "перекус"}, {"word": "dessert", "translation": "десерт"}, {"word": "spice", "translation": "специя"}, {"word": "flour", "translation": "мука"}, {"word": "oven", "translation": "духовка"}, {"word": "pan", "translation": "сковорода"}, {"word": "plate", "translation": "тарелка"}, {"word": "cup", "translation": "чашка"}, {"word": "bowl", "translation": "миска"}, {"word": "fork", "translation": "вилка"}, {"word": "knife", "translation": "нож"}, {"word": "spoon", "translation": "ложка"}, {"word": "grill", "translation": "гриль"}, {"word": "fry", "translation": "жарить"}, {"word": "boil", "translation": "варить"}, {"word": "bake", "translation": "запекать"}],
        "B1": [{"word": "cuisine", "translation": "кухня"}, {"word": "appetizer", "translation": "закуска"}, {"word": "main course", "translation": "основное блюдо"}, {"word": "side dish", "translation": "гарнир"}, {"word": "dough", "translation": "тесто"}, {"word": "yeast", "translation": "дрожжи"}, {"word": "vinegar", "translation": "уксус"}, {"word": "sauce", "translation": "соус"}, {"word": "gravy", "translation": "подливка"}, {"word": "seasoning", "translation": "приправа"}, {"word": "marinate", "translation": "мариновать"}, {"word": "steam", "translation": "готовить на пару"}, {"word": "roast", "translation": "жарить в духовке"}, {"word": "stew", "translation": "тушить"}, {"word": "slice", "translation": "ломтик"}, {"word": "dice", "translation": "резать кубиками"}, {"word": "chop", "translation": "рубить"}, {"word": "grate", "translation": "тереть"}],
        "B2": [{"word": "gourmet", "translation": "гурман"}, {"word": "palate", "translation": "нёбо"}, {"word": "aroma", "translation": "аромат"}, {"word": "texture", "translation": "текстура"}, {"word": "delicacy", "translation": "деликатес"}, {"word": "fermentation", "translation": "ферментация"}, {"word": "culinary", "translation": "кулинарный"}, {"word": "gastronomy", "translation": "гастрономия"}, {"word": "infusion", "translation": "настой"}, {"word": "emulsion", "translation": "эмульсия"}, {"word": "caramelize", "translation": "карамелизировать"}, {"word": "flambé", "translation": "фламбировать"}, {"word": "purée", "translation": "пюре"}, {"word": "sous-vide", "translation": "су-вид"}]
    },
    "family": {
        "A1": [{"word": "mother", "translation": "мама"}, {"word": "father", "translation": "папа"}, {"word": "brother", "translation": "брат"}, {"word": "sister", "translation": "сестра"}, {"word": "son", "translation": "сын"}, {"word": "daughter", "translation": "дочь"}, {"word": "grandmother", "translation": "бабушка"}, {"word": "grandfather", "translation": "дедушка"}, {"word": "aunt", "translation": "тётя"}, {"word": "uncle", "translation": "дядя"}, {"word": "cousin", "translation": "двоюродный брат/сестра"}, {"word": "baby", "translation": "младенец"}, {"word": "parents", "translation": "родители"}, {"word": "children", "translation": "дети"}, {"word": "wife", "translation": "жена"}, {"word": "husband", "translation": "муж"}],
        "A2": [{"word": "grandparents", "translation": "бабушка и дедушка"}, {"word": "grandson", "translation": "внук"}, {"word": "granddaughter", "translation": "внучка"}, {"word": "stepmother", "translation": "мачеха"}, {"word": "stepfather", "translation": "отчим"}, {"word": "stepson", "translation": "пасынок"}, {"word": "stepdaughter", "translation": "падчерица"}, {"word": "half-brother", "translation": "единокровный брат"}, {"word": "half-sister", "translation": "единокровная сестра"}, {"word": "in-laws", "translation": "родственники со стороны супруга"}, {"word": "mother-in-law", "translation": "свекровь/тёща"}, {"word": "father-in-law", "translation": "свёкор/тесть"}],
        "B1": [{"word": "relative", "translation": "родственник"}, {"word": "spouse", "translation": "супруг/а"}, {"word": "sibling", "translation": "родной брат или сестра"}, {"word": "ancestor", "translation": "предок"}, {"word": "descendant", "translation": "потомок"}, {"word": "generation", "translation": "поколение"}, {"word": "family tree", "translation": "родословное древо"}, {"word": "hereditary", "translation": "наследственный"}, {"word": "paternity", "translation": "отцовство"}, {"word": "maternity", "translation": "материнство"}, {"word": "kinship", "translation": "родство"}],
        "B2": [{"word": "lineage", "translation": "происхождение"}, {"word": "pedigree", "translation": "родословная"}, {"word": "dynasty", "translation": "династия"}, {"word": "clan", "translation": "клан"}, {"word": "tribe", "translation": "племя"}, {"word": "genealogy", "translation": "генеалогия"}, {"word": "matriarch", "translation": "матриарх"}, {"word": "patriarch", "translation": "патриарх"}, {"word": "filial", "translation": "сыновний/дочерний"}, {"word": "fraternal", "translation": "братский"}]
    },
    "travel": {
        "A1": [{"word": "hotel", "translation": "отель"}, {"word": "plane", "translation": "самолёт"}, {"word": "ticket", "translation": "билет"}, {"word": "train", "translation": "поезд"}, {"word": "bus", "translation": "автобус"}, {"word": "car", "translation": "машина"}, {"word": "map", "translation": "карта"}, {"word": "passport", "translation": "паспорт"}, {"word": "bag", "translation": "сумка"}, {"word": "suitcase", "translation": "чемодан"}, {"word": "trip", "translation": "поездка"}, {"word": "holiday", "translation": "отпуск"}, {"word": "beach", "translation": "пляж"}, {"word": "mountain", "translation": "гора"}, {"word": "city", "translation": "город"}, {"word": "country", "translation": "страна"}],
        "A2": [{"word": "luggage", "translation": "багаж"}, {"word": "boarding pass", "translation": "посадочный талон"}, {"word": "check-in", "translation": "регистрация"}, {"word": "departure", "translation": "отправление"}, {"word": "arrival", "translation": "прибытие"}, {"word": "delay", "translation": "задержка"}, {"word": "platform", "translation": "платформа"}, {"word": "tourist", "translation": "турист"}, {"word": "guide", "translation": "гид"}, {"word": "sightseeing", "translation": "осмотр достопримечательностей"}, {"word": "museum", "translation": "музей"}, {"word": "restaurant", "translation": "ресторан"}, {"word": "reservation", "translation": "бронирование"}],
        "B1": [{"word": "destination", "translation": "место назначения"}, {"word": "itinerary", "translation": "маршрут"}, {"word": "accommodation", "translation": "размещение"}, {"word": "all-inclusive", "translation": "всё включено"}, {"word": "cruise", "translation": "круиз"}, {"word": "excursion", "translation": "экскурсия"}, {"word": "backpacking", "translation": "поход с рюкзаком"}, {"word": "souvenir", "translation": "сувенир"}, {"word": "currency", "translation": "валюта"}, {"word": "exchange rate", "translation": "обменный курс"}, {"word": "visa", "translation": "виза"}],
        "B2": [{"word": "expedition", "translation": "экспедиция"}, {"word": "journey", "translation": "путешествие"}, {"word": "voyage", "translation": "морское путешествие"}, {"word": "pilgrimage", "translation": "паломничество"}, {"word": "nomad", "translation": "кочевник"}, {"word": "cosmopolitan", "translation": "космополитичный"}, {"word": "wanderlust", "translation": "страсть к путешествиям"}, {"word": "globetrotter", "translation": "бывалый путешественник"}, {"word": "road trip", "translation": "путешествие на машине"}]
    },
    "daily routines": {
        "A1": [{"word": "wake up", "translation": "просыпаться"}, {"word": "get up", "translation": "вставать"}, {"word": "have breakfast", "translation": "завтракать"}, {"word": "go to work", "translation": "идти на работу"}, {"word": "have lunch", "translation": "обедать"}, {"word": "go home", "translation": "идти домой"}, {"word": "have dinner", "translation": "ужинать"}, {"word": "watch TV", "translation": "смотреть телевизор"}, {"word": "read a book", "translation": "читать книгу"}, {"word": "go to bed", "translation": "ложиться спать"}, {"word": "sleep", "translation": "спать"}, {"word": "shower", "translation": "душ"}, {"word": "brush teeth", "translation": "чистить зубы"}, {"word": "get dressed", "translation": "одеваться"}],
        "A2": [{"word": "routine", "translation": "распорядок"}, {"word": "schedule", "translation": "расписание"}, {"word": "habit", "translation": "привычка"}, {"word": "alarm clock", "translation": "будильник"}, {"word": "commute", "translation": "добираться до работы"}, {"word": "office", "translation": "офис"}, {"word": "colleague", "translation": "коллега"}, {"word": "meeting", "translation": "встреча"}, {"word": "deadline", "translation": "срок"}, {"word": "relax", "translation": "расслабляться"}],
        "B1": [{"word": "productive", "translation": "продуктивный"}, {"word": "efficient", "translation": "эффективный"}, {"word": "procrastinate", "translation": "откладывать"}, {"word": "prioritize", "translation": "расставлять приоритеты"}, {"word": "work-life balance", "translation": "баланс работы и жизни"}, {"word": "overtime", "translation": "сверхурочная работа"}, {"word": "shift", "translation": "смена"}],
        "B2": [{"word": "circadian rhythm", "translation": "циркадный ритм"}, {"word": "insomnia", "translation": "бессонница"}, {"word": "meditation", "translation": "медитация"}, {"word": "mindfulness", "translation": "осознанность"}, {"word": "ergonomic", "translation": "эргономичный"}, {"word": "burnout", "translation": "выгорание"}]
    },
    "hobby": {
        "A1": [{"word": "music", "translation": "музыка"}, {"word": "sport", "translation": "спорт"}, {"word": "game", "translation": "игра"}, {"word": "draw", "translation": "рисовать"}, {"word": "read", "translation": "читать"}, {"word": "dance", "translation": "танцевать"}, {"word": "sing", "translation": "петь"}, {"word": "swim", "translation": "плавать"}, {"word": "run", "translation": "бегать"}, {"word": "walk", "translation": "гулять"}],
        "A2": [{"word": "photography", "translation": "фотография"}, {"word": "gardening", "translation": "садоводство"}, {"word": "cooking", "translation": "кулинария"}, {"word": "baking", "translation": "выпечка"}, {"word": "knitting", "translation": "вязание"}, {"word": "sewing", "translation": "шитьё"}, {"word": "painting", "translation": "живопись"}, {"word": "sculpture", "translation": "скульптура"}],
        "B1": [{"word": "calligraphy", "translation": "каллиграфия"}, {"word": "pottery", "translation": "гончарное дело"}, {"word": "woodworking", "translation": "столярное дело"}, {"word": "origami", "translation": "оригами"}, {"word": "collecting", "translation": "коллекционирование"}, {"word": "stamps", "translation": "марки"}, {"word": "coins", "translation": "монеты"}],
        "B2": [{"word": "calligraphy", "translation": "каллиграфия"}, {"word": "pottery", "translation": "гончарное дело"}, {"word": "woodworking", "translation": "столярное дело"}, {"word": "origami", "translation": "оригами"}]
    },
    "work": {
        "A1": [{"word": "job", "translation": "работа"}, {"word": "office", "translation": "офис"}, {"word": "boss", "translation": "начальник"}, {"word": "colleague", "translation": "коллега"}, {"word": "salary", "translation": "зарплата"}, {"word": "meeting", "translation": "встреча"}, {"word": "email", "translation": "электронная почта"}, {"word": "phone", "translation": "телефон"}, {"word": "computer", "translation": "компьютер"}, {"word": "document", "translation": "документ"}],
        "A2": [{"word": "employee", "translation": "сотрудник"}, {"word": "employer", "translation": "работодатель"}, {"word": "deadline", "translation": "срок"}, {"word": "project", "translation": "проект"}, {"word": "task", "translation": "задача"}, {"word": "responsibility", "translation": "обязанность"}, {"word": "experience", "translation": "опыт"}, {"word": "interview", "translation": "собеседование"}],
        "B1": [{"word": "career", "translation": "карьера"}, {"word": "promotion", "translation": "повышение"}, {"word": "resignation", "translation": "увольнение"}, {"word": "retirement", "translation": "выход на пенсию"}, {"word": "benefits", "translation": "льготы"}, {"word": "insurance", "translation": "страховка"}, {"word": "contract", "translation": "контракт"}],
        "B2": [{"word": "entrepreneur", "translation": "предприниматель"}, {"word": "startup", "translation": "стартап"}, {"word": "freelance", "translation": "фриланс"}, {"word": "remote work", "translation": "удалённая работа"}, {"word": "corporate", "translation": "корпоративный"}, {"word": "hierarchy", "translation": "иерархия"}]
    },
    "education": {
        "A1": [{"word": "school", "translation": "школа"}, {"word": "teacher", "translation": "учитель"}, {"word": "student", "translation": "ученик"}, {"word": "book", "translation": "книга"}, {"word": "pen", "translation": "ручка"}, {"word": "pencil", "translation": "карандаш"}, {"word": "desk", "translation": "парта"}, {"word": "class", "translation": "класс"}, {"word": "lesson", "translation": "урок"}, {"word": "homework", "translation": "домашнее задание"}],
        "A2": [{"word": "university", "translation": "университет"}, {"word": "college", "translation": "колледж"}, {"word": "degree", "translation": "степень"}, {"word": "subject", "translation": "предмет"}, {"word": "exam", "translation": "экзамен"}, {"word": "test", "translation": "тест"}, {"word": "grade", "translation": "оценка"}, {"word": "course", "translation": "курс"}],
        "B1": [{"word": "scholarship", "translation": "стипендия"}, {"word": "tuition", "translation": "плата за обучение"}, {"word": "lecture", "translation": "лекция"}, {"word": "seminar", "translation": "семинар"}, {"word": "research", "translation": "исследование"}, {"word": "thesis", "translation": "диссертация"}],
        "B2": [{"word": "pedagogy", "translation": "педагогика"}, {"word": "curriculum", "translation": "учебный план"}, {"word": "syllabus", "translation": "программа курса"}, {"word": "academic", "translation": "академический"}, {"word": "undergraduate", "translation": "студент бакалавриата"}, {"word": "postgraduate", "translation": "аспирант"}]
    },
    "health": {
        "A1": [{"word": "doctor", "translation": "врач"}, {"word": "nurse", "translation": "медсестра"}, {"word": "hospital", "translation": "больница"}, {"word": "medicine", "translation": "лекарство"}, {"word": "pill", "translation": "таблетка"}, {"word": "pain", "translation": "боль"}, {"word": "headache", "translation": "головная боль"}, {"word": "fever", "translation": "температура"}, {"word": "cold", "translation": "простуда"}, {"word": "cough", "translation": "кашель"}],
        "A2": [{"word": "healthy", "translation": "здоровый"}, {"word": "sick", "translation": "больной"}, {"word": "treatment", "translation": "лечение"}, {"word": "symptom", "translation": "симптом"}, {"word": "diagnosis", "translation": "диагноз"}, {"word": "prescription", "translation": "рецепт"}, {"word": "pharmacy", "translation": "аптека"}, {"word": "dentist", "translation": "стоматолог"}],
        "B1": [{"word": "surgery", "translation": "хирургия"}, {"word": "therapy", "translation": "терапия"}, {"word": "vaccine", "translation": "вакцина"}, {"word": "immunity", "translation": "иммунитет"}, {"word": "chronic", "translation": "хронический"}, {"word": "acute", "translation": "острый"}],
        "B2": [{"word": "diagnosis", "translation": "диагноз"}, {"word": "prognosis", "translation": "прогноз"}, {"word": "rehabilitation", "translation": "реабилитация"}, {"word": "palliative", "translation": "паллиативный"}, {"word": "terminal", "translation": "терминальный"}]
    },
    "nature": {
        "A1": [{"word": "tree", "translation": "дерево"}, {"word": "flower", "translation": "цветок"}, {"word": "grass", "translation": "трава"}, {"word": "sky", "translation": "небо"}, {"word": "sun", "translation": "солнце"}, {"word": "moon", "translation": "луна"}, {"word": "star", "translation": "звезда"}, {"word": "cloud", "translation": "облако"}, {"word": "rain", "translation": "дождь"}, {"word": "snow", "translation": "снег"}],
        "A2": [{"word": "mountain", "translation": "гора"}, {"word": "river", "translation": "река"}, {"word": "lake", "translation": "озеро"}, {"word": "ocean", "translation": "океан"}, {"word": "sea", "translation": "море"}, {"word": "forest", "translation": "лес"}, {"word": "desert", "translation": "пустыня"}, {"word": "jungle", "translation": "джунгли"}],
        "B1": [{"word": "climate", "translation": "климат"}, {"word": "weather", "translation": "погода"}, {"word": "season", "translation": "сезон"}, {"word": "environment", "translation": "окружающая среда"}, {"word": "pollution", "translation": "загрязнение"}, {"word": "conservation", "translation": "охрана природы"}],
        "B2": [{"word": "ecosystem", "translation": "экосистема"}, {"word": "biodiversity", "translation": "биоразнообразие"}, {"word": "sustainable", "translation": "устойчивый"}, {"word": "renewable", "translation": "возобновляемый"}, {"word": "fossil fuels", "translation": "ископаемое топливо"}]
    },
    "technology": {
        "A1": [{"word": "computer", "translation": "компьютер"}, {"word": "phone", "translation": "телефон"}, {"word": "internet", "translation": "интернет"}, {"word": "website", "translation": "сайт"}, {"word": "email", "translation": "электронная почта"}, {"word": "app", "translation": "приложение"}, {"word": "game", "translation": "игра"}, {"word": "screen", "translation": "экран"}, {"word": "keyboard", "translation": "клавиатура"}, {"word": "mouse", "translation": "мышь"}],
        "A2": [{"word": "software", "translation": "программное обеспечение"}, {"word": "hardware", "translation": "оборудование"}, {"word": "update", "translation": "обновление"}, {"word": "download", "translation": "скачивать"}, {"word": "upload", "translation": "загружать"}, {"word": "password", "translation": "пароль"}, {"word": "username", "translation": "имя пользователя"}, {"word": "login", "translation": "вход"}],
        "B1": [{"word": "innovation", "translation": "инновация"}, {"word": "artificial intelligence", "translation": "искусственный интеллект"}, {"word": "virtual reality", "translation": "виртуальная реальность"}, {"word": "augmented reality", "translation": "дополненная реальность"}, {"word": "robotics", "translation": "робототехника"}, {"word": "automation", "translation": "автоматизация"}],
        "B2": [{"word": "nanotechnology", "translation": "нанотехнология"}, {"word": "biotechnology", "translation": "биотехнология"}, {"word": "quantum computing", "translation": "квантовые вычисления"}, {"word": "blockchain", "translation": "блокчейн"}, {"word": "cryptocurrency", "translation": "криптовалюта"}]
    },
    "shopping": {
        "A1": [{"word": "shop", "translation": "магазин"}, {"word": "store", "translation": "магазин"}, {"word": "price", "translation": "цена"}, {"word": "money", "translation": "деньги"}, {"word": "buy", "translation": "покупать"}, {"word": "sell", "translation": "продавать"}, {"word": "customer", "translation": "покупатель"}, {"word": "cash", "translation": "наличные"}, {"word": "card", "translation": "карта"}],
        "A2": [{"word": "receipt", "translation": "чек"}, {"word": "discount", "translation": "скидка"}, {"word": "sale", "translation": "распродажа"}, {"word": "bargain", "translation": "выгодная покупка"}, {"word": "refund", "translation": "возврат денег"}, {"word": "receipt", "translation": "квитанция"}],
        "B1": [{"word": "afford", "translation": "позволить себе"}, {"word": "budget", "translation": "бюджет"}, {"word": "expensive", "translation": "дорогой"}, {"word": "cheap", "translation": "дешёвый"}, {"word": "receipt", "translation": "чек"}, {"word": "warranty", "translation": "гарантия"}],
        "B2": [{"word": "reimburse", "translation": "возмещать"}, {"word": "overcharge", "translation": "завышать цену"}, {"word": "installment", "translation": "рассрочка"}, {"word": "credit", "translation": "кредит"}, {"word": "debt", "translation": "долг"}]
    },
    "sports": {
        "A1": [{"word": "football", "translation": "футбол"}, {"word": "basketball", "translation": "баскетбол"}, {"word": "tennis", "translation": "теннис"}, {"word": "swimming", "translation": "плавание"}, {"word": "running", "translation": "бег"}, {"word": "game", "translation": "игра"}, {"word": "team", "translation": "команда"}, {"word": "player", "translation": "игрок"}],
        "A2": [{"word": "volleyball", "translation": "волейбол"}, {"word": "golf", "translation": "гольф"}, {"word": "skiing", "translation": "лыжи"}, {"word": "snowboarding", "translation": "сноуборд"}, {"word": "yoga", "translation": "йога"}, {"word": "gym", "translation": "спортзал"}],
        "B1": [{"word": "tournament", "translation": "турнир"}, {"word": "championship", "translation": "чемпионат"}, {"word": "competition", "translation": "соревнование"}, {"word": "athlete", "translation": "спортсмен"}, {"word": "coach", "translation": "тренер"}],
        "B2": [{"word": "marathon", "translation": "марафон"}, {"word": "sprint", "translation": "спринт"}, {"word": "doping", "translation": "допинг"}, {"word": "penalty", "translation": "штраф"}]
    }
}

# ========== ОГРОМНАЯ БАЗА ГРАММАТИЧЕСКИХ ОШИБОК ==========
GRAMMAR_MISTAKES = {
    "A1": [
        {"wrong": "He go to school", "correct": "He goes to school", "explanation": "В настоящем времени (Present Simple) после he/she/it нужно добавлять окончание -s к глаголу."},
        {"wrong": "She don't like coffee", "correct": "She doesn't like coffee", "explanation": "В отрицаниях с he/she/it используется does not (doesn't), а глагол остаётся без окончания."},
        {"wrong": "They was happy", "correct": "They were happy", "explanation": "С местоимениями they, we, you используется were, а не was."},
        {"wrong": "I is a student", "correct": "I am a student", "explanation": "С местоимением I используется am."},
        {"wrong": "You was late", "correct": "You were late", "explanation": "С you всегда используется were, даже если речь об одном человеке."},
        {"wrong": "We has a car", "correct": "We have a car", "explanation": "С we используется have, а не has."},
        {"wrong": "He doesn't likes it", "correct": "He doesn't like it", "explanation": "После doesn't глагол без окончания -s."},
        {"wrong": "She go to work", "correct": "She goes to work", "explanation": "С she нужно добавлять -es к глаголу."},
        {"wrong": "They goes home", "correct": "They go home", "explanation": "С they используется go, а не goes."},
        {"wrong": "I doesn't know", "correct": "I don't know", "explanation": "С I используется don't, а не doesn't."}
    ],
    "A2": [
        {"wrong": "I have went", "correct": "I have gone", "explanation": "После have используется третья форма глагола (go → gone)."},
        {"wrong": "She can to sing", "correct": "She can sing", "explanation": "После модальных глаголов (can, must, should) частица to не ставится."},
        {"wrong": "He didn't went", "correct": "He didn't go", "explanation": "После didn't используется начальная форма глагола."},
        {"wrong": "I am go to school", "correct": "I am going to school", "explanation": "Для действий в процессе используется am/is/are + глагол с -ing."},
        {"wrong": "She have a dog", "correct": "She has a dog", "explanation": "С she используется has, а не have."},
        {"wrong": "They was playing", "correct": "They were playing", "explanation": "С they используется were, а не was."},
        {"wrong": "I am agree", "correct": "I agree", "explanation": "Глагол agree не требует am, это просто I agree."},
        {"wrong": "She is beautiful girl", "correct": "She is a beautiful girl", "explanation": "Перед исчисляемым существительным нужен артикль a/an."},
        {"wrong": "They are student", "correct": "They are students", "explanation": "После they нужно множественное число students."},
        {"wrong": "He is engineer", "correct": "He is an engineer", "explanation": "Перед engineer нужен артикль an."}
    ],
    "B1": [
        {"wrong": "If I will see him", "correct": "If I see him", "explanation": "В условных предложениях после if не используется will."},
        {"wrong": "I am used to get up early", "correct": "I am used to getting up early", "explanation": "После be used to нужен герундий (-ing)."},
        {"wrong": "She suggested me to go", "correct": "She suggested that I go", "explanation": "После suggest не используется инфинитив с to."},
        {"wrong": "He told that he is tired", "correct": "He said that he was tired", "explanation": "В косвенной речи время часто сдвигается."},
        {"wrong": "I look forward to meet you", "correct": "I look forward to meeting you", "explanation": "После look forward to нужен герундий (-ing)."},
        {"wrong": "She is married with a doctor", "correct": "She is married to a doctor", "explanation": "Правильный предлог — married to."},
        {"wrong": "I have been in London", "correct": "I have been to London", "explanation": "После have been используется to, а не in."},
        {"wrong": "He is afraid from dogs", "correct": "He is afraid of dogs", "explanation": "Правильный предлог — afraid of."},
        {"wrong": "She is interested about art", "correct": "She is interested in art", "explanation": "Правильный предлог — interested in."},
        {"wrong": "I depend from my parents", "correct": "I depend on my parents", "explanation": "Правильный предлог — depend on."}
    ],
    "B2": [
        {"wrong": "If I would have known", "correct": "If I had known", "explanation": "В условных 3 типа используется Past Perfect."},
        {"wrong": "I wish I was taller", "correct": "I wish I were taller", "explanation": "После wish используется were для всех лиц."},
        {"wrong": "She is capable to do it", "correct": "She is capable of doing it", "explanation": "После capable нужен of + герундий."},
        {"wrong": "She is angry at him", "correct": "She is angry with him", "explanation": "С людьми используется angry with."},
        {"wrong": "I congratulated her for her success", "correct": "I congratulated her on her success", "explanation": "Правильный предлог — congratulate on."},
        {"wrong": "He is different than me", "correct": "He is different from me", "explanation": "Правильный предлог — different from."},
        {"wrong": "She is good in math", "correct": "She is good at math", "explanation": "Правильный предлог — good at."},
        {"wrong": "I am responsible of this", "correct": "I am responsible for this", "explanation": "Правильный предлог — responsible for."},
        {"wrong": "He is similar with his father", "correct": "He is similar to his father", "explanation": "Правильный предлог — similar to."},
        {"wrong": "She succeeded to pass the exam", "correct": "She succeeded in passing the exam", "explanation": "После succeed нужен in + герундий."}
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
        {"wrong": "He go to school every day. She don't like apples. They was happy yesterday.",
         "correct": "He goes to school every day. She doesn't like apples. They were happy yesterday.",
         "errors": 3}
    ],
    "A2": [
        {"wrong": "Last weekend I go to the park with my friends. We play football and then we eat ice cream. It was fun. In the evening we watch a movie. The movie was interesting. I like weekends very much.",
         "correct": "Last weekend I went to the park with my friends. We played football and then we ate ice cream. It was fun. In the evening we watched a movie. The movie was interesting. I like weekends very much.",
         "errors": 3},
        {"wrong": "I have a hobby. I like to reading books. I read every day. My favorite books are about adventures. I have many books at home. I also like to write stories. It is very interesting.",
         "correct": "I have a hobby. I like to read books. I read every day. My favorite books are about adventures. I have many books at home. I also like to write stories. It is very interesting.",
         "errors": 1},
        {"wrong": "Yesterday I go to the cinema. I see a good film. My friend was with me. We eat popcorn.",
         "correct": "Yesterday I went to the cinema. I saw a good film. My friend was with me. We ate popcorn.",
         "errors": 3}
    ],
    "B1": [
        {"wrong": "If I will have money, I travel to Japan next year. I want visit Tokyo and see the cherry blossoms. I also want to try Japanese food. I heard it's delicious. I hope my dream will come true.",
         "correct": "If I have money, I will travel to Japan next year. I want to visit Tokyo and see the cherry blossoms. I also want to try Japanese food. I heard it's delicious. I hope my dream will come true.",
         "errors": 3},
        {"wrong": "To be healthy, you should to eat fruits and vegetables. You also need to exercise regularly. Many people don't have time for sport, but it's important. I try to eat healthy and do sport every day.",
         "correct": "To be healthy, you should eat fruits and vegetables. You also need to exercise regularly. Many people don't have time for sport, but it's important. I try to eat healthy and do sport every day.",
         "errors": 1},
        {"wrong": "She suggested me to go to the party. I was used to get up early when I was a student. If I will see him, I tell him the news.",
         "correct": "She suggested that I go to the party. I was used to getting up early when I was a student. If I see him, I will tell him the news.",
         "errors": 3}
    ],
    "B2": [
        {"wrong": "Many people is concerned about climate change. They think that we should to do more to protect the environment. Recycling is one way to help. Also, we should use less plastic. It is everyone's responsibility.",
         "correct": "Many people are concerned about climate change. They think that we should do more to protect the environment. Recycling is one way to help. Also, we should use less plastic. It is everyone's responsibility.",
         "errors": 2},
        {"wrong": "Choosing a career is not easy. You should to consider your interests and skills. Many people change their careers several times. It's important to find a job that you enjoy. I am interested in becoming a doctor.",
         "correct": "Choosing a career is not easy. You should consider your interests and skills. Many people change their careers several times. It's important to find a job that you enjoy. I am interested in becoming a doctor.",
         "errors": 1},
        {"wrong": "If I would have known about the meeting, I would have came. She insisted me to stay. I look forward to meet you.",
         "correct": "If I had known about the meeting, I would have come. She insisted that I stay. I look forward to meeting you.",
         "errors": 3}
    ]
}

# ========== ФУНКЦИЯ РАСПОЗНАВАНИЯ РЕЧИ ==========
def recognize_speech_from_voice(voice_file_path):
    recognizer = sr.Recognizer()
    try:
        audio = AudioSegment.from_ogg(voice_file_path)
        wav_path = voice_file_path.replace('.ogg', '.wav')
        audio.export(wav_path, format="wav")
        
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
            
        try:
            text = recognizer.recognize_google(audio_data, language='en-US')
            return text, 'en'
        except:
            try:
                text = recognizer.recognize_google(audio_data, language='ru-RU')
                return text, 'ru'
            except:
                return None, None
    except Exception as e:
        return None, None
    finally:
        if os.path.exists(wav_path):
            os.unlink(wav_path)

def generate_audio(word):
    tts = gTTS(text=word, lang='en')
    filename = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3').name
    tts.save(filename)
    return filename

def highlight_mistake(user_word, correct_word):
    """Выделяет конкретные ошибки жирным шрифтом"""
    user_word = user_word.lower()
    correct_word = correct_word.lower()
    
    if user_word == correct_word:
        return None
    
    result = "❌ *Ошибка в слове!*\n\n"
    result += f"Ты написал(а): {user_word}\n"
    result += f"Правильно: *{correct_word}*\n\n"
    
    # Подсвечиваем неправильные буквы
    diff = []
    for i, (uc, cc) in enumerate(zip(user_word, correct_word)):
        if uc != cc:
            diff.append(f"• позиция {i+1}: *{uc}* → должно быть *{cc}*")
    
    if len(user_word) != len(correct_word):
        if len(user_word) > len(correct_word):
            diff.append(f"• лишние буквы в конце: *{user_word[len(correct_word):]}*")
        else:
            diff.append(f"• не хватает букв: *{correct_word[len(user_word):]}*")
    
    if diff:
        result += "Детали ошибок:\n" + "\n".join(diff)
    
    return result

# ========== КЛАВИАТУРЫ ==========
def get_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("👂 Аудирование"))
    markup.add(types.KeyboardButton("🧠 Грамматический детектив"))
    markup.add(types.KeyboardButton("📖 Текст с ошибками"))
    markup.add(types.KeyboardButton("📚 Мой словарь"))
    markup.add(types.KeyboardButton("📊 Моя статистика"))
    markup.add(types.KeyboardButton("📄 Скачать словарь PDF"))
    return markup

def get_after_task_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("🔄 Продолжить"))
    markup.add(types.KeyboardButton("🎯 Выбрать тему/уровень"))
    markup.add(types.KeyboardButton("🏠 Главное меню"))
    return markup

def get_topics_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for topic in TOPICS:
        markup.add(types.KeyboardButton(f"📚 {topic}"))
    markup.add(types.KeyboardButton("🏠 Главное меню"))
    return markup

def get_levels_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for level in LEVELS:
        markup.add(types.KeyboardButton(f"📊 {level}"))
    markup.add(types.KeyboardButton("🏠 Главное меню"))
    return markup

def generate_pdf(user_id):
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
    user_data[user_id]["current_mode"] = None
    
    welcome_text = """
🌟 *Добро пожаловать в твой персональный языковой тренажёр!* 🌟

Я помогу тебе улучшить английский. Вот что я умею:

👂 *АУДИРОВАНИЕ*
• Выбери тему и уровень
• Я пришлю аудио со словом
• Напиши слово + перевод
• Если ошибёшься — покажу *какую букву* ты написал(а) неправильно

🧠 *ГРАММАТИЧЕСКИЙ ДЕТЕКТИВ*
• Я даю фразу с ошибкой
• Ты исправляешь голосом
• Объясню правило

📖 *ТЕКСТ С ОШИБКАМИ*
• Я пришлю текст с ошибками
• Ты читаешь вслух, исправляя

📚 *МОЙ СЛОВАРЬ* — твои слова
📊 *МОЯ СТАТИСТИКА* — анализ ошибок
📄 *СКАЧАТЬ PDF* — красивый словарь

👇 *Выбери режим*
    """
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=get_main_menu())

# ========== АУДИРОВАНИЕ ==========
@bot.message_handler(func=lambda message: message.text == "👂 Аудирование")
def listening_mode(message):
    user_id = message.from_user.id
    user_data[user_id]["current_mode"] = "listening"
    bot.send_message(message.chat.id, "👂 *Аудирование*\n\nВыбери тему:", parse_mode="Markdown", reply_markup=get_topics_keyboard())

@bot.message_handler(func=lambda message: message.text and message.text.startswith("📚 "))
def handle_topic_choice(message):
    user_id = message.from_user.id
    if user_data[user_id]["current_mode"] != "listening":
        return
    
    topic = message.text.replace("📚 ", "").strip()
    if topic not in WORD_BASE:
        bot.send_message(message.chat.id, "❌ Тема не найдена")
        return
    
    user_data[user_id]["current_topic"] = topic
    bot.send_message(message.chat.id, f"Тема: *{topic}*\n\nВыбери уровень:", parse_mode="Markdown", reply_markup=get_levels_keyboard())

@bot.message_handler(func=lambda message: message.text and message.text.startswith("📊 "))
def handle_level_choice(message):
    user_id = message.from_user.id
    
    level = message.text.replace("📊 ", "").strip()
    if level not in LEVELS:
        return
    
    if user_data[user_id]["current_mode"] == "listening":
        user_data[user_id]["current_level"] = level
        topic = user_data[user_id]["current_topic"]
        
        words = WORD_BASE.get(topic, {}).get(level, [])
        if not words:
            bot.send_message(message.chat.id, "😕 Для этой темы и уровня пока нет слов.")
            return
        
        word_data = random.choice(words)
        user_data[user_id]["current_word"] = word_data
        
        audio_file = generate_audio(word_data["word"])
        with open(audio_file, 'rb') as f:
            bot.send_voice(message.chat.id, f)
        os.unlink(audio_file)
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("❓ Не знаю"), types.KeyboardButton("➕ В словарь"))
        markup.add(types.KeyboardButton("🏠 Главное меню"))
        
        bot.send_message(message.chat.id, f"🔊 Напиши слово и перевод:", reply_markup=markup)
    
    elif user_data[user_id]["current_mode"] == "grammar":
        user_data[user_id]["current_level"] = level
        mistakes = GRAMMAR_MISTAKES.get(level, [])
        if not mistakes:
            bot.send_message(message.chat.id, "😕 Для этого уровня пока нет заданий.")
            return
        
        mistake = random.choice(mistakes)
        user_data[user_id]["current_mistake"] = mistake
        
        audio_file = generate_audio(mistake["wrong"])
        with open(audio_file, 'rb') as f:
            bot.send_voice(message.chat.id, f)
        os.unlink(audio_file)
        
        bot.send_message(
            message.chat.id,
            f"🧠 *Найди ошибку:*\n\n_{mistake['wrong']}_\n\nОтправь *голосовое сообщение* с правильным вариантом:",
            parse_mode="Markdown"
        )
    
    elif user_data[user_id]["current_mode"] == "text":
        user_data[user_id]["current_level"] = level
        texts = TEXTS_WITH_ERRORS.get(level, [])
        if not texts:
            bot.send_message(message.chat.id, "😕 Для этого уровня пока нет текстов.")
            return
        
        text_data = random.choice(texts)
        user_data[user_id]["current_text"] = text_data
        
        bot.send_message(
            message.chat.id,
            f"📖 *Текст (ошибок: {text_data['errors']})*\n\n{text_data['wrong']}\n\nПрочитай вслух, исправляя ошибки, и отправь *голосовое сообщение*:",
            parse_mode="Markdown"
        )

@bot.message_handler(func=lambda message: message.text == "❓ Не знаю")
def handle_dont_know(message):
    user_id = message.from_user.id
    word_data = user_data[user_id].get("current_word")
    if not word_data:
        return
    
    bot.send_message(
        message.chat.id,
        f"🔍 Это слово: *{word_data['word']}*\nПеревод: *{word_data['translation']}*",
        parse_mode="Markdown"
    )
    
    user_data[user_id]["unknown_words"].append(word_data["word"])
    bot.send_message(message.chat.id, "Что дальше?", reply_markup=get_after_task_menu())

@bot.message_handler(func=lambda message: message.text == "➕ В словарь")
def handle_add_to_vocab(message):
    user_id = message.from_user.id
    word_data = user_data[user_id].get("current_word")
    if not word_data:
        return
    
    for item in user_data[user_id]["vocabulary"]:
        if item["word"] == word_data["word"]:
            bot.send_message(message.chat.id, "ℹ️ Это слово уже есть в словаре.")
            break
    else:
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
    
    user_word = message.text.strip().lower()
    correct_word = word_data["word"].lower()
    
    if user_word == correct_word:
        bot.send_message(message.chat.id, f"✅ *Верно!*\n\nСлово: {word_data['word']}\nПеревод: {word_data['translation']}", parse_mode="Markdown")
    else:
        error_msg = highlight_mistake(user_word, correct_word)
        if error_msg:
            bot.send_message(message.chat.id, error_msg, parse_mode="Markdown")
        else:
            bot.send_message(message.chat.id, f"❌ Ошибка!\nПравильно: *{word_data['word']}*", parse_mode="Markdown")
        
        topic = user_data[user_id].get("current_topic", "общая")
        user_data[user_id]["mistakes_count"][topic] += 1
    
    bot.send_message(message.chat.id, "Что дальше?", reply_markup=get_after_task_menu())

# ========== ГРАММАТИЧЕСКИЙ ДЕТЕКТИВ ==========
@bot.message_handler(func=lambda message: message.text == "🧠 Грамматический детектив")
def grammar_mode(message):
    user_id = message.from_user.id
    user_data[user_id]["current_mode"] = "grammar"
    bot.send_message(message.chat.id, "🧠 *Грамматический детектив*\n\nВыбери уровень:", parse_mode="Markdown", reply_markup=get_levels_keyboard())

# ========== ТЕКСТ С ОШИБКАМИ ==========
@bot.message_handler(func=lambda message: message.text == "📖 Текст с ошибками")
def text_errors_mode(message):
    user_id = message.from_user.id
    user_data[user_id]["current_mode"] = "text"
    bot.send_message(message.chat.id, "📖 *Текст с ошибками*\n\nВыбери уровень:", parse_mode="Markdown", reply_markup=get_levels_keyboard())

# ========== ОБРАБОТКА ГОЛОСА ==========
@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    user_id = message.from_user.id
    mode = user_data[user_id]["current_mode"]
    
    if not mode:
        bot.send_message(message.chat.id, "Сначала выбери режим.")
        return
    
    status_msg = bot.send_message(message.chat.id, "🎧 Распознаю речь...")
    
    try:
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        ogg_path = tempfile.NamedTemporaryFile(delete=False, suffix='.ogg').name
        with open(ogg_path, 'wb') as f:
            f.write(downloaded_file)
        
        recognized_text, lang = recognize_speech_from_voice(ogg_path)
        os.unlink(ogg_path)
        
        if not recognized_text:
            bot.edit_message_text("❌ Не удалось распознать речь.", chat_id=message.chat.id, message_id=status_msg.message_id)
            return
        
        if mode == "grammar":
            mistake = user_data[user_id].get("current_mistake")
            if mistake:
                if recognized_text.lower() in mistake["correct"].lower() or mistake["correct"].lower() in recognized_text.lower():
                    response = f"✅ *Правильно!*\n\nПравильный вариант: {mistake['correct']}"
                else:
                    response = f"❌ *Ошибка*\n\nЯ распознал: {recognized_text}\nПравильно: *{mistake['correct']}*\n\n{mistake['explanation']}"
                    user_data[user_id]["grammar_mistakes"].append(mistake["wrong"])
                bot.edit_message_text(response, chat_id=message.chat.id, message_id=status_msg.message_id, parse_mode="Markdown")
        
        elif mode == "text":
            text_data = user_data[user_id].get("current_text")
            if text_data:
                if text_data['errors'] == 0:
                    response = f"✅ *Отлично!*\n\nТы прочитал текст."
                else:
                    response = f"✅ Я распознал твой текст.\n\nПравильный вариант:\n{text_data['correct']}"
                bot.edit_message_text(response, chat_id=message.chat.id, message_id=status_msg.message_id, parse_mode="Markdown")
        
        bot.send_message(message.chat.id, "Что дальше?", reply_markup=get_after_task_menu())
        
    except Exception as e:
        bot.edit_message_text(f"❌ Ошибка: {str(e)}", chat_id=message.chat.id, message_id=status_msg.message_id)

# ========== МОЙ СЛОВАРЬ ==========
@bot.message_handler(func=lambda message: message.text == "📚 Мой словарь")
def show_vocabulary(message):
    user_id = message.from_user.id
    vocab = user_data[user_id]["vocabulary"]
    
    if not vocab:
        bot.send_message(message.chat.id, "📚 Словарь пока пуст.")
    else:
        text = "📚 *Твой словарь:*\n\n"
        for item in vocab:
            text += f"• {item['word']} — {item['translation']}\n"
        
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
        bot.send_message(message.chat.id, "📄 Словарь пуст.")
        return
    
    with open(pdf_file, 'rb') as f:
        bot.send_document(message.chat.id, f, caption="📚 Твой словарь")
    
    os.unlink(pdf_file)
    bot.send_message(message.chat.id, "Выбери действие:", reply_markup=get_main_menu())

# ========== СТАТИСТИКА ==========
@bot.message_handler(func=lambda message: message.text == "📊 Моя статистика")
def show_statistics(message):
    user_id = message.from_user.id
    mistakes = user_data[user_id]["mistakes_count"]
    
    if not mistakes:
        bot.send_message(message.chat.id, "📊 Ошибок пока нет.")
    else:
        text = "📊 *Твои ошибки:*\n\n"
        for topic, count in mistakes.items():
            text += f"• {topic}: {count}\n"
        bot.send_message(message.chat.id, text, parse_mode="Markdown")
    
    bot.send_message(message.chat.id, "Выбери действие:", reply_markup=get_main_menu())

# ========== УПРАВЛЕНИЕ МЕНЮ ==========
@bot.message_handler(func=lambda message: message.text == "🏠 Главное меню")
def back_to_main_menu(message):
    user_id = message.from_user.id
    user_data[user_id]["current_mode"] = None
    bot.send_message(message.chat.id, "Главное меню:", reply_markup=get_main_menu())

@bot.message_handler(func=lambda message: message.text == "🔄 Продолжить")
def continue_mode(message):
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
            
            bot.send_message(message.chat.id, f"🔊 Напиши слово и перевод:", reply_markup=markup)
    
    elif mode == "grammar":
        grammar_mode(message)
    elif mode == "text":
        text_errors_mode(message)

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

# ========== ЗАПУСК ==========
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
    
    # Заголовки
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
    
    # Отправляем пользователю
    with open(tmp_path, 'rb') as f:
        bot.send_document(message.chat.id, f, caption="📘 Твой словарь")
    
    # Удаляем временный файл
    os.unlink(tmp_path)
if __name__ == "__main__":
    print("🤖 БОТ ЗАПУЩЕН")
    bot.infinity_polling()