import telebot
import random
import tempfile
import os
from telebot import types
from gtts import gTTS

TOKEN = "8616377232:AAGfTmBVjfJIR92lO_u4Fm1gDN9sFFxIVA"
bot = telebot.TeleBot(TOKEN)

user_data = {}

TOPICS = ["food", "travel", "daily routines", "family", "education"]
LEVELS = ["A1", "A2", "B1", "B2"]

# ========== УНИКАЛЬНЫЕ СЛОВА ПО ТЕМАМ (100+ НА УРОВЕНЬ) ==========
WORD_BASE = {
    "food": {
        "A1": [
            {"word": "apple", "translation": "яблоко"}, {"word": "banana", "translation": "банан"},
            {"word": "bread", "translation": "хлеб"}, {"word": "milk", "translation": "молоко"},
            {"word": "egg", "translation": "яйцо"}, {"word": "cheese", "translation": "сыр"},
            {"word": "butter", "translation": "масло"}, {"word": "meat", "translation": "мясо"},
            {"word": "fish", "translation": "рыба"}, {"word": "chicken", "translation": "курица"},
            {"word": "rice", "translation": "рис"}, {"word": "pasta", "translation": "паста"},
            {"word": "soup", "translation": "суп"}, {"word": "salad", "translation": "салат"},
            {"word": "water", "translation": "вода"}, {"word": "juice", "translation": "сок"},
            {"word": "coffee", "translation": "кофе"}, {"word": "tea", "translation": "чай"},
            {"word": "sugar", "translation": "сахар"}, {"word": "salt", "translation": "соль"},
            {"word": "pepper", "translation": "перец"}, {"word": "oil", "translation": "масло растительное"},
            {"word": "flour", "translation": "мука"}, {"word": "potato", "translation": "картофель"},
            {"word": "tomato", "translation": "помидор"}, {"word": "onion", "translation": "лук"},
            {"word": "carrot", "translation": "морковь"}, {"word": "cabbage", "translation": "капуста"},
            {"word": "cucumber", "translation": "огурец"}, {"word": "garlic", "translation": "чеснок"},
            {"word": "lemon", "translation": "лимон"}, {"word": "orange", "translation": "апельсин"},
            {"word": "strawberry", "translation": "клубника"}, {"word": "grape", "translation": "виноград"},
            {"word": "watermelon", "translation": "арбуз"}, {"word": "melon", "translation": "дыня"},
            {"word": "peach", "translation": "персик"}, {"word": "pear", "translation": "груша"},
            {"word": "cake", "translation": "торт"}, {"word": "pie", "translation": "пирог"},
            {"word": "cookie", "translation": "печенье"}, {"word": "chocolate", "translation": "шоколад"},
            {"word": "ice cream", "translation": "мороженое"}, {"word": "yogurt", "translation": "йогурт"},
            {"word": "honey", "translation": "мед"}, {"word": "jam", "translation": "варенье"},
            {"word": "sausage", "translation": "колбаса"}, {"word": "bacon", "translation": "бекон"},
            {"word": "ham", "translation": "ветчина"}, {"word": "pork", "translation": "свинина"},
            {"word": "beef", "translation": "говядина"}, {"word": "lamb", "translation": "баранина"},
            {"word": "turkey", "translation": "индейка"}, {"word": "duck", "translation": "утка"},
            {"word": "shrimp", "translation": "креветка"}, {"word": "crab", "translation": "краб"},
            {"word": "lobster", "translation": "лобстер"}, {"word": "mushroom", "translation": "гриб"},
            {"word": "bean", "translation": "фасоль"}, {"word": "pea", "translation": "горох"},
            {"word": "corn", "translation": "кукуруза"}, {"word": "nuts", "translation": "орехи"},
            {"word": "almond", "translation": "миндаль"}, {"word": "walnut", "translation": "грецкий орех"},
            {"word": "peanut", "translation": "арахис"}, {"word": "raisin", "translation": "изюм"},
            {"word": "prune", "translation": "чернослив"}, {"word": "date", "translation": "финик"},
            {"word": "fig", "translation": "инжир"}, {"word": "cereal", "translation": "хлопья"},
            {"word": "oatmeal", "translation": "овсянка"}, {"word": "pancake", "translation": "блин"},
            {"word": "waffle", "translation": "вафля"}, {"word": "muffin", "translation": "кекс"},
            {"word": "bagel", "translation": "бублик"}, {"word": "toast", "translation": "тост"},
            {"word": "sandwich", "translation": "бутерброд"}, {"word": "burger", "translation": "бургер"},
            {"word": "pizza", "translation": "пицца"}, {"word": "taco", "translation": "тако"},
            {"word": "burrito", "translation": "буррито"}, {"word": "noodles", "translation": "лапша"},
            {"word": "spaghetti", "translation": "спагетти"}, {"word": "lasagna", "translation": "лазанья"},
            {"word": "risotto", "translation": "ризотто"}, {"word": "curry", "translation": "карри"},
            {"word": "stew", "translation": "рагу"}, {"word": "casserole", "translation": "запеканка"},
            {"word": "omelette", "translation": "омлет"}, {"word": "scrambled eggs", "translation": "яичница"},
            {"word": "fried eggs", "translation": "яичница глазунья"}, {"word": "boiled eggs", "translation": "варёные яйца"},
            {"word": "pudding", "translation": "пудинг"}, {"word": "custard", "translation": "заварной крем"},
            {"word": "sorbet", "translation": "сорбет"}, {"word": "sherbet", "translation": "щербет"},
            {"word": "milkshake", "translation": "молочный коктейль"}, {"word": "smoothie", "translation": "смузи"},
            {"word": "lemonade", "translation": "лимонад"}, {"word": "soda", "translation": "газировка"},
            {"word": "cola", "translation": "кола"}, {"word": "beer", "translation": "пиво"},
            {"word": "wine", "translation": "вино"}, {"word": "vodka", "translation": "водка"},
            {"word": "whiskey", "translation": "виски"}, {"word": "rum", "translation": "ром"},
            {"word": "gin", "translation": "джин"}, {"word": "champagne", "translation": "шампанское"}
        ],
        "A2": [
            {"word": "breakfast", "translation": "завтрак"}, {"word": "lunch", "translation": "обед"},
            {"word": "dinner", "translation": "ужин"}, {"word": "supper", "translation": "ужин (поздний)"},
            {"word": "snack", "translation": "перекус"}, {"word": "meal", "translation": "приём пищи"},
            {"word": "course", "translation": "блюдо"}, {"word": "appetizer", "translation": "закуска"},
            {"word": "starter", "translation": "первое блюдо"}, {"word": "main course", "translation": "основное блюдо"},
            {"word": "side dish", "translation": "гарнир"}, {"word": "dessert", "translation": "десерт"},
            {"word": "beverage", "translation": "напиток"}, {"word": "drink", "translation": "напиток"},
            {"word": "ingredient", "translation": "ингредиент"}, {"word": "recipe", "translation": "рецепт"},
            {"word": "menu", "translation": "меню"}, {"word": "waiter", "translation": "официант"},
            {"word": "waitress", "translation": "официантка"}, {"word": "chef", "translation": "шеф-повар"},
            {"word": "cook", "translation": "повар"}, {"word": "restaurant", "translation": "ресторан"},
            {"word": "cafe", "translation": "кафе"}, {"word": "cafeteria", "translation": "столовая"},
            {"word": "bakery", "translation": "пекарня"}, {"word": "butcher", "translation": "мясная лавка"},
            {"word": "market", "translation": "рынок"}, {"word": "supermarket", "translation": "супермаркет"},
            {"word": "grocery", "translation": "продуктовый магазин"}, {"word": "delicatessen", "translation": "деликатесы"},
            {"word": "fresh", "translation": "свежий"}, {"word": "frozen", "translation": "замороженный"},
            {"word": "canned", "translation": "консервированный"}, {"word": "dried", "translation": "сушеный"},
            {"word": "smoked", "translation": "копченый"}, {"word": "pickled", "translation": "маринованный"},
            {"word": "raw", "translation": "сырой"}, {"word": "ripe", "translation": "спелый"},
            {"word": "unripe", "translation": "незрелый"}, {"word": "sweet", "translation": "сладкий"},
            {"word": "sour", "translation": "кислый"}, {"word": "bitter", "translation": "горький"},
            {"word": "salty", "translation": "соленый"}, {"word": "spicy", "translation": "острый"},
            {"word": "bland", "translation": "пресный"}, {"word": "tasty", "translation": "вкусный"},
            {"word": "delicious", "translation": "очень вкусный"}, {"word": "disgusting", "translation": "отвратительный"},
            {"word": "appetizing", "translation": "аппетитный"}, {"word": "flavor", "translation": "вкус"},
            {"word": "taste", "translation": "вкус"}, {"word": "smell", "translation": "запах"},
            {"word": "aroma", "translation": "аромат"}, {"word": "texture", "translation": "текстура"},
            {"word": "crispy", "translation": "хрустящий"}, {"word": "crunchy", "translation": "хрустящий"},
            {"word": "chewy", "translation": "жевательный"}, {"word": "tender", "translation": "нежный"},
            {"word": "tough", "translation": "жесткий"}, {"word": "juicy", "translation": "сочный"},
            {"word": "greasy", "translation": "жирный"}, {"word": "oily", "translation": "маслянистый"},
            {"word": "creamy", "translation": "сливочный"}, {"word": "spicy", "translation": "пряный"},
            {"word": "herbs", "translation": "травы"}, {"word": "spices", "translation": "специи"},
            {"word": "salt", "translation": "соль"}, {"word": "pepper", "translation": "перец"},
            {"word": "sugar", "translation": "сахар"}, {"word": "honey", "translation": "мед"},
            {"word": "vinegar", "translation": "уксус"}, {"word": "oil", "translation": "масло"},
            {"word": "butter", "translation": "сливочное масло"}, {"word": "margarine", "translation": "маргарин"},
            {"word": "mayonnaise", "translation": "майонез"}, {"word": "ketchup", "translation": "кетчуп"},
            {"word": "mustard", "translation": "горчица"}, {"word": "sauce", "translation": "соус"},
            {"word": "gravy", "translation": "подливка"}, {"word": "dressing", "translation": "заправка"},
            {"word": "marinade", "translation": "маринад"}, {"word": "syrup", "translation": "сироп"},
            {"word": "jam", "translation": "варенье"}, {"word": "jelly", "translation": "желе"},
            {"word": "marmalade", "translation": "мармелад"}, {"word": "peanut butter", "translation": "арахисовое масло"},
            {"word": "chocolate spread", "translation": "шоколадная паста"}, {"word": "nutella", "translation": "нутелла"},
            {"word": "dough", "translation": "тесто"}, {"word": "batter", "translation": "жидкое тесто"},
            {"word": "yeast", "translation": "дрожжи"}, {"word": "baking powder", "translation": "разрыхлитель"},
            {"word": "baking soda", "translation": "сода"}, {"word": "flour", "translation": "мука"},
            {"word": "cornstarch", "translation": "кукурузный крахмал"}, {"word": "breadcrumbs", "translation": "панировочные сухари"}
        ]
    },
    "travel": {
        "A1": [
            {"word": "travel", "translation": "путешествовать"}, {"word": "trip", "translation": "поездка"},
            {"word": "journey", "translation": "путешествие"}, {"word": "tour", "translation": "тур"},
            {"word": "visit", "translation": "посещать"}, {"word": "go", "translation": "идти"},
            {"word": "come", "translation": "приходить"}, {"word": "arrive", "translation": "прибывать"},
            {"word": "leave", "translation": "уезжать"}, {"word": "depart", "translation": "отправляться"},
            {"word": "return", "translation": "возвращаться"}, {"word": "stay", "translation": "останавливаться"},
            {"word": "hotel", "translation": "отель"}, {"word": "hostel", "translation": "хостел"},
            {"word": "motel", "translation": "мотель"}, {"word": "inn", "translation": "гостиница"},
            {"word": "guesthouse", "translation": "гостевой дом"}, {"word": "bed and breakfast", "translation": "ночлег и завтрак"},
            {"word": "room", "translation": "комната"}, {"word": "single room", "translation": "одноместный номер"},
            {"word": "double room", "translation": "двухместный номер"}, {"word": "suite", "translation": "люкс"},
            {"word": "book", "translation": "бронировать"}, {"word": "reserve", "translation": "резервировать"},
            {"word": "cancel", "translation": "отменять"}, {"word": "change", "translation": "менять"},
            {"word": "ticket", "translation": "билет"}, {"word": "passport", "translation": "паспорт"},
            {"word": "visa", "translation": "виза"}, {"word": "id", "translation": "удостоверение личности"},
            {"word": "bag", "translation": "сумка"}, {"word": "backpack", "translation": "рюкзак"},
            {"word": "suitcase", "translation": "чемодан"}, {"word": "luggage", "translation": "багаж"},
            {"word": "map", "translation": "карта"}, {"word": "guide", "translation": "гид"},
            {"word": "guidebook", "translation": "путеводитель"}, {"word": "tourist", "translation": "турист"},
            {"word": "traveler", "translation": "путешественник"}, {"word": "plane", "translation": "самолет"},
            {"word": "airplane", "translation": "самолет"}, {"word": "train", "translation": "поезд"},
            {"word": "bus", "translation": "автобус"}, {"word": "car", "translation": "машина"},
            {"word": "taxi", "translation": "такси"}, {"word": "bike", "translation": "велосипед"},
            {"word": "motorcycle", "translation": "мотоцикл"}, {"word": "ship", "translation": "корабль"},
            {"word": "boat", "translation": "лодка"}, {"word": "ferry", "translation": "паром"},
            {"word": "airport", "translation": "аэропорт"}, {"word": "station", "translation": "вокзал"},
            {"word": "bus stop", "translation": "автобусная остановка"}, {"word": "port", "translation": "порт"},
            {"word": "beach", "translation": "пляж"}, {"word": "mountain", "translation": "гора"},
            {"word": "lake", "translation": "озеро"}, {"word": "river", "translation": "река"},
            {"word": "forest", "translation": "лес"}, {"word": "desert", "translation": "пустыня"},
            {"word": "island", "translation": "остров"}, {"word": "city", "translation": "город"},
            {"word": "town", "translation": "городок"}, {"word": "village", "translation": "деревня"},
            {"word": "capital", "translation": "столица"}, {"word": "country", "translation": "страна"},
            {"word": "abroad", "translation": "за границей"}, {"word": "overseas", "translation": "за морем"},
            {"word": "sight", "translation": "достопримечательность"}, {"word": "attraction", "translation": "аттракцион"},
            {"word": "museum", "translation": "музей"}, {"word": "gallery", "translation": "галерея"},
            {"word": "church", "translation": "церковь"}, {"word": "cathedral", "translation": "собор"},
            {"word": "castle", "translation": "замок"}, {"word": "palace", "translation": "дворец"},
            {"word": "monument", "translation": "памятник"}, {"word": "statue", "translation": "статуя"},
            {"word": "bridge", "translation": "мост"}, {"word": "square", "translation": "площадь"},
            {"word": "park", "translation": "парк"}, {"word": "garden", "translation": "сад"},
            {"word": "zoo", "translation": "зоопарк"}, {"word": "aquarium", "translation": "аквариум"},
            {"word": "amusement park", "translation": "парк развлечений"}, {"word": "souvenir", "translation": "сувенир"},
            {"word": "gift", "translation": "подарок"}, {"word": "postcard", "translation": "открытка"},
            {"word": "photo", "translation": "фото"}, {"word": "picture", "translation": "картинка"},
            {"word": "camera", "translation": "камера"}, {"word": "money", "translation": "деньги"},
            {"word": "currency", "translation": "валюта"}, {"word": "cash", "translation": "наличные"},
            {"word": "card", "translation": "карта"}, {"word": "credit card", "translation": "кредитная карта"},
            {"word": "exchange", "translation": "обмен"}, {"word": "rate", "translation": "курс"},
            {"word": "language", "translation": "язык"}, {"word": "phrase", "translation": "фраза"},
            {"word": "word", "translation": "слово"}, {"word": "hello", "translation": "привет"},
            {"word": "goodbye", "translation": "пока"}, {"word": "please", "translation": "пожалуйста"},
            {"word": "thank you", "translation": "спасибо"}, {"word": "sorry", "translation": "извините"},
            {"word": "excuse me", "translation": "извините"}, {"word": "help", "translation": "помощь"},
            {"word": "information", "translation": "информация"}, {"word": "directions", "translation": "направления"}
        ],
        "A2": [
            {"word": "adventure", "translation": "приключение"}, {"word": "explore", "translation": "исследовать"},
            {"word": "discover", "translation": "открывать"}, {"word": "experience", "translation": "опыт"},
            {"word": "culture", "translation": "культура"}, {"word": "tradition", "translation": "традиция"},
            {"word": "custom", "translation": "обычай"}, {"word": "local", "translation": "местный"},
            {"word": "native", "translation": "родной"}, {"word": "foreign", "translation": "иностранный"},
            {"word": "international", "translation": "международный"}, {"word": "domestic", "translation": "внутренний"},
            {"word": "package tour", "translation": "пакетный тур"}, {"word": "guided tour", "translation": "экскурсия с гидом"},
            {"word": "self-guided tour", "translation": "самостоятельная экскурсия"}, {"word": "day trip", "translation": "однодневная поездка"},
            {"word": "weekend trip", "translation": "поездка на выходные"}, {"word": "road trip", "translation": "путешествие на машине"},
            {"word": "backpacking", "translation": "путешествие с рюкзаком"}, {"word": "camping", "translation": "кемпинг"},
            {"word": "glamping", "translation": "глэмпинг"}, {"word": "hiking", "translation": "поход"},
            {"word": "trekking", "translation": "треккинг"}, {"word": "climbing", "translation": "скалолазание"},
            {"word": "skiing", "translation": "лыжи"}, {"word": "snowboarding", "translation": "сноуборд"},
            {"word": "surfing", "translation": "серфинг"}, {"word": "diving", "translation": "дайвинг"},
            {"word": "snorkeling", "translation": "снорклинг"}, {"word": "fishing", "translation": "рыбалка"},
            {"word": "hunting", "translation": "охота"}, {"word": "safari", "translation": "сафари"},
            {"word": "cruise", "translation": "круиз"}, {"word": "yacht", "translation": "яхта"},
            {"word": "sail", "translation": "парус"}, {"word": "row", "translation": "грести"},
            {"word": "paddle", "translation": "грести веслом"}, {"word": "kayak", "translation": "каяк"},
            {"word": "canoe", "translation": "каноэ"}, {"word": "raft", "translation": "плот"},
            {"word": "rafting", "translation": "рафтинг"}, {"word": "canyoning", "translation": "каньонинг"},
            {"word": "paragliding", "translation": "параглайдинг"}, {"word": "hang gliding", "translation": "дельтапланеризм"},
            {"word": "skydiving", "translation": "парашютный спорт"}, {"word": "bungee jumping", "translation": "прыжки с тарзанкой"},
            {"word": "ziplining", "translation": "троллей"}, {"word": "hot air balloon", "translation": "воздушный шар"},
            {"word": "helicopter", "translation": "вертолет"}, {"word": "private jet", "translation": "частный самолет"},
            {"word": "first class", "translation": "первый класс"}, {"word": "business class", "translation": "бизнес-класс"},
            {"word": "economy class", "translation": "эконом-класс"}, {"word": "boarding pass", "translation": "посадочный талон"},
            {"word": "check-in", "translation": "регистрация"}, {"word": "check-out", "translation": "выезд"},
            {"word": "departure", "translation": "отправление"}, {"word": "arrival", "translation": "прибытие"},
            {"word": "delay", "translation": "задержка"}, {"word": "cancellation", "translation": "отмена"},
            {"word": "overbooking", "translation": "овербукинг"}, {"word": "upgrade", "translation": "повышение класса"},
            {"word": "downgrade", "translation": "понижение класса"}, {"word": "gate", "translation": "выход"},
            {"word": "terminal", "translation": "терминал"}, {"word": "runway", "translation": "взлетная полоса"},
            {"word": "takeoff", "translation": "взлет"}, {"word": "landing", "translation": "посадка"},
            {"word": "flight attendant", "translation": "бортпроводник"}, {"word": "pilot", "translation": "пилот"},
            {"word": "captain", "translation": "капитан"}, {"word": "crew", "translation": "экипаж"},
            {"word": "passenger", "translation": "пассажир"}, {"word": "seat", "translation": "место"},
            {"word": "aisle seat", "translation": "место у прохода"}, {"word": "window seat", "translation": "место у окна"},
            {"word": "row", "translation": "ряд"}, {"word": "baggage claim", "translation": "выдача багажа"},
            {"word": "lost and found", "translation": "бюро находок"}, {"word": "customs", "translation": "таможня"},
            {"word": "immigration", "translation": "иммиграция"}, {"word": "passport control", "translation": "паспортный контроль"},
            {"word": "security check", "translation": "проверка безопасности"}, {"word": "duty-free", "translation": "беспошлинный"},
            {"word": "currency exchange", "translation": "обмен валюты"}, {"word": "atm", "translation": "банкомат"},
            {"word": "travel insurance", "translation": "туристическая страховка"}, {"word": "health insurance", "translation": "медицинская страховка"},
            {"word": "vaccination", "translation": "вакцинация"}, {"word": "medicine", "translation": "лекарство"},
            {"word": "pharmacy", "translation": "аптека"}, {"word": "hospital", "translation": "больница"},
            {"word": "clinic", "translation": "клиника"}, {"word": "doctor", "translation": "врач"},
            {"word": "dentist", "translation": "стоматолог"}, {"word": "emergency", "translation": "чрезвычайная ситуация"}
        ]
    },
    "daily routines": {
        "A1": [
            {"word": "wake up", "translation": "просыпаться"}, {"word": "get up", "translation": "вставать"},
            {"word": "make bed", "translation": "заправлять постель"}, {"word": "wash face", "translation": "умываться"},
            {"word": "brush teeth", "translation": "чистить зубы"}, {"word": "take shower", "translation": "принимать душ"},
            {"word": "take bath", "translation": "принимать ванну"}, {"word": "get dressed", "translation": "одеваться"},
            {"word": "have breakfast", "translation": "завтракать"}, {"word": "have lunch", "translation": "обедать"},
            {"word": "have dinner", "translation": "ужинать"}, {"word": "go to school", "translation": "идти в школу"},
            {"word": "go to work", "translation": "идти на работу"}, {"word": "go home", "translation": "идти домой"},
            {"word": "come home", "translation": "приходить домой"}, {"word": "do homework", "translation": "делать домашнее задание"},
            {"word": "study", "translation": "учиться"}, {"word": "work", "translation": "работать"},
            {"word": "cook", "translation": "готовить"}, {"word": "clean", "translation": "убирать"},
            {"word": "tidy up", "translation": "прибираться"}, {"word": "wash dishes", "translation": "мыть посуду"},
            {"word": "do laundry", "translation": "стирать"}, {"word": "iron clothes", "translation": "гладить одежду"},
            {"word": "fold clothes", "translation": "складывать одежду"}, {"word": "water plants", "translation": "поливать растения"},
            {"word": "feed pet", "translation": "кормить питомца"}, {"word": "walk dog", "translation": "гулять с собакой"},
            {"word": "play", "translation": "играть"}, {"word": "watch TV", "translation": "смотреть телевизор"},
            {"word": "listen to music", "translation": "слушать музыку"}, {"word": "read", "translation": "читать"},
            {"word": "write", "translation": "писать"}, {"word": "draw", "translation": "рисовать"},
            {"word": "paint", "translation": "красить"}, {"word": "take photos", "translation": "фотографировать"},
            {"word": "use computer", "translation": "пользоваться компьютером"}, {"word": "surf internet", "translation": "сидеть в интернете"},
            {"word": "check email", "translation": "проверять почту"}, {"word": "call", "translation": "звонить"},
            {"word": "text", "translation": "писать смс"}, {"word": "meet friends", "translation": "встречаться с друзьями"},
            {"word": "visit family", "translation": "навещать семью"}, {"word": "go out", "translation": "выходить"},
            {"word": "stay in", "translation": "оставаться дома"}, {"word": "relax", "translation": "расслабляться"},
            {"word": "rest", "translation": "отдыхать"}, {"word": "sleep", "translation": "спать"},
            {"word": "nap", "translation": "дремать"}, {"word": "dream", "translation": "мечтать"},
            {"word": "morning", "translation": "утро"}, {"word": "afternoon", "translation": "день"},
            {"word": "evening", "translation": "вечер"}, {"word": "night", "translation": "ночь"},
            {"word": "midnight", "translation": "полночь"}, {"word": "dawn", "translation": "рассвет"},
            {"word": "dusk", "translation": "сумерки"}, {"word": "sunrise", "translation": "восход"},
            {"word": "sunset", "translation": "закат"}, {"word": "today", "translation": "сегодня"},
            {"word": "tomorrow", "translation": "завтра"}, {"word": "yesterday", "translation": "вчера"},
            {"word": "now", "translation": "сейчас"}, {"word": "later", "translation": "позже"},
            {"word": "soon", "translation": "скоро"}, {"word": "early", "translation": "рано"},
            {"word": "late", "translation": "поздно"}, {"word": "always", "translation": "всегда"},
            {"word": "often", "translation": "часто"}, {"word": "sometimes", "translation": "иногда"},
            {"word": "rarely", "translation": "редко"}, {"word": "never", "translation": "никогда"},
            {"word": "every day", "translation": "каждый день"}, {"word": "every week", "translation": "каждую неделю"},
            {"word": "every month", "translation": "каждый месяц"}, {"word": "every year", "translation": "каждый год"},
            {"word": "on weekdays", "translation": "по будням"}, {"word": "on weekends", "translation": "по выходным"},
            {"word": "in the morning", "translation": "утром"}, {"word": "in the afternoon", "translation": "днем"},
            {"word": "in the evening", "translation": "вечером"}, {"word": "at night", "translation": "ночью"},
            {"word": "at midnight", "translation": "в полночь"}, {"word": "at noon", "translation": "в полдень"},
            {"word": "bedtime", "translation": "время ложиться спать"}, {"word": "wake-up time", "translation": "время просыпаться"},
            {"word": "alarm clock", "translation": "будильник"}, {"word": "clock", "translation": "часы"},
            {"word": "watch", "translation": "наручные часы"}, {"word": "time", "translation": "время"},
            {"word": "hour", "translation": "час"}, {"word": "minute", "translation": "минута"},
            {"word": "second", "translation": "секунда"}, {"word": "daily", "translation": "ежедневный"},
            {"word": "weekly", "translation": "еженедельный"}, {"word": "monthly", "translation": "ежемесячный"},
            {"word": "yearly", "translation": "ежегодный"}, {"word": "routine", "translation": "распорядок"},
            {"word": "schedule", "translation": "расписание"}, {"word": "habit", "translation": "привычка"},
            {"word": "regular", "translation": "регулярный"}, {"word": "usual", "translation": "обычный"},
            {"word": "typical", "translation": "типичный"}, {"word": "ordinary", "translation": "обыкновенный"}
        ]

    "family": {
        "A1": [
            {"word": "mother", "translation": "мама"}, {"word": "father", "translation": "папа"},
            {"word": "parent", "translation": "родитель"}, {"word": "brother", "translation": "брат"},
            {"word": "sister", "translation": "сестра"}, {"word": "son", "translation": "сын"},
            {"word": "daughter", "translation": "дочь"}, {"word": "baby", "translation": "младенец"},
            {"word": "child", "translation": "ребенок"}, {"word": "children", "translation": "дети"},
            {"word": "grandmother", "translation": "бабушка"}, {"word": "grandfather", "translation": "дедушка"},
            {"word": "grandparent", "translation": "дедушка и бабушка"}, {"word": "grandson", "translation": "внук"},
            {"word": "granddaughter", "translation": "внучка"}, {"word": "aunt", "translation": "тетя"},
            {"word": "uncle", "translation": "дядя"}, {"word": "cousin", "translation": "двоюродный брат/сестра"},
            {"word": "nephew", "translation": "племянник"}, {"word": "niece", "translation": "племянница"},
            {"word": "husband", "translation": "муж"}, {"word": "wife", "translation": "жена"},
            {"word": "family", "translation": "семья"}, {"word": "relatives", "translation": "родственники"},
            {"word": "twin", "translation": "близнец"}, {"word": "only child", "translation": "единственный ребенок"},
            {"word": "eldest", "translation": "старший"}, {"word": "youngest", "translation": "младший"},
            {"word": "middle child", "translation": "средний ребенок"}, {"word": "stepmother", "translation": "мачеха"},
            {"word": "stepfather", "translation": "отчим"}, {"word": "stepson", "translation": "пасынок"},
            {"word": "stepdaughter", "translation": "падчерица"}, {"word": "stepbrother", "translation": "сводный брат"},
            {"word": "stepsister", "translation": "сводная сестра"}, {"word": "half-brother", "translation": "единокровный брат"},
            {"word": "half-sister", "translation": "единокровная сестра"}, {"word": "godmother", "translation": "крестная мать"},
            {"word": "godfather", "translation": "крестный отец"}, {"word": "godson", "translation": "крестник"},
            {"word": "goddaughter", "translation": "крестница"}, {"word": "in-laws", "translation": "родственники со стороны супруга"},
            {"word": "mother-in-law", "translation": "свекровь/теща"}, {"word": "father-in-law", "translation": "свекор/тесть"},
            {"word": "sister-in-law", "translation": "золовка/невестка"}, {"word": "brother-in-law", "translation": "шурин/деверь"},
            {"word": "fiancé", "translation": "жених"}, {"word": "fiancée", "translation": "невеста"},
            {"word": "bride", "translation": "невеста (на свадьбе)"}, {"word": "groom", "translation": "жених (на свадьбе)"},
            {"word": "newlyweds", "translation": "молодожены"}, {"word": "divorce", "translation": "развод"},
            {"word": "separated", "translation": "в разводе"}, {"word": "widow", "translation": "вдова"},
            {"word": "widower", "translation": "вдовец"}, {"word": "single parent", "translation": "одинокий родитель"},
            {"word": "adopt", "translation": "усыновлять"}, {"word": "adopted child", "translation": "приемный ребенок"},
            {"word": "foster child", "translation": "приемный ребенок"}, {"word": "foster family", "translation": "приемная семья"},
            {"word": "biological parent", "translation": "биологический родитель"}, {"word": "birth mother", "translation": "родная мать"},
            {"word": "birth father", "translation": "родной отец"}, {"word": "sibling", "translation": "родной брат или сестра"},
            {"word": "ancestor", "translation": "предок"}, {"word": "descendant", "translation": "потомок"},
            {"word": "generation", "translation": "поколение"}, {"word": "family tree", "translation": "родословное древо"},
            {"word": "heritage", "translation": "наследие"}, {"word": "lineage", "translation": "происхождение"},
            {"word": "blood relative", "translation": "кровный родственник"}, {"word": "distant relative", "translation": "дальний родственник"},
            {"word": "close family", "translation": "близкие родственники"}, {"word": "immediate family", "translation": "ближайшие родственники"},
            {"word": "extended family", "translation": "родня"}, {"word": "family gathering", "translation": "семейная встреча"},
            {"word": "family reunion", "translation": "воссоединение семьи"}, {"word": "family dinner", "translation": "семейный ужин"},
            {"word": "family tradition", "translation": "семейная традиция"}, {"word": "family values", "translation": "семейные ценности"},
            {"word": "family portrait", "translation": "семейный портрет"}, {"word": "family photo", "translation": "семейное фото"},
            {"word": "family album", "translation": "семейный альбом"}, {"word": "family history", "translation": "история семьи"},
            {"word": "family name", "translation": "фамилия"}, {"word": "last name", "translation": "фамилия"},
            {"word": "surname", "translation": "фамилия"}, {"word": "maiden name", "translation": "девичья фамилия"},
            {"word": "married name", "translation": "фамилия после замужества"}, {"word": "family business", "translation": "семейный бизнес"},
            {"word": "family home", "translation": "родовой дом"}, {"word": "family estate", "translation": "семейное поместье"},
            {"word": "family heirloom", "translation": "семейная реликвия"}, {"word": "family secret", "translation": "семейная тайна"},
            {"word": "family feud", "translation": "семейная вражда"}, {"word": "family drama", "translation": "семейная драма"},
            {"word": "family crisis", "translation": "семейный кризис"}, {"word": "family support", "translation": "поддержка семьи"},
            {"word": "family bond", "translation": "семейная связь"}, {"word": "family tie", "translation": "семейные узы"},
            {"word": "family love", "translation": "семейная любовь"}, {"word": "family happiness", "translation": "семейное счастье"}
        ],
        "A2": [
            {"word": "parenthood", "translation": "родительство"}, {"word": "motherhood", "translation": "материнство"},
            {"word": "fatherhood", "translation": "отцовство"}, {"word": "childhood", "translation": "детство"},
            {"word": "babyhood", "translation": "младенчество"}, {"word": "infancy", "translation": "младенчество"},
            {"word": "toddler", "translation": "малыш"}, {"word": "preschooler", "translation": "дошкольник"},
            {"word": "schoolchild", "translation": "школьник"}, {"word": "teenager", "translation": "подросток"},
            {"word": "adolescent", "translation": "подросток"}, {"word": "youth", "translation": "юность"},
            {"word": "adulthood", "translation": "взрослая жизнь"}, {"word": "middle age", "translation": "средний возраст"},
            {"word": "old age", "translation": "старость"}, {"word": "senior citizen", "translation": "пожилой человек"},
            {"word": "elderly", "translation": "пожилой"}, {"word": "aged", "translation": "престарелый"},
            {"word": "grandmotherly", "translation": "по-бабушкиному"}, {"word": "grandfatherly", "translation": "по-дедушкиному"},
            {"word": "parental", "translation": "родительский"}, {"word": "maternal", "translation": "материнский"},
            {"word": "paternal", "translation": "отцовский"}, {"word": "fraternal", "translation": "братский"},
            {"word": "sororal", "translation": "сестринский"}, {"word": "filial", "translation": "сыновний/дочерний"},
            {"word": "conjugal", "translation": "супружеский"}, {"word": "marital", "translation": "брачный"},
            {"word": "prenuptial", "translation": "добрачный"}, {"word": "postnuptial", "translation": "послебрачный"},
            {"word": "wedding", "translation": "свадьба"}, {"word": "marriage", "translation": "брак"},
            {"word": "engagement", "translation": "помолвка"}, {"word": "honeymoon", "translation": "медовый месяц"},
            {"word": "anniversary", "translation": "годовщина"}, {"word": "golden anniversary", "translation": "золотая свадьба"},
            {"word": "silver anniversary", "translation": "серебряная свадьба"}, {"word": "diamond anniversary", "translation": "бриллиантовая свадьба"},
            {"word": "birth", "translation": "рождение"}, {"word": "birthday", "translation": "день рождения"},
            {"word": "christening", "translation": "крещение"}, {"word": "baptism", "translation": "крещение"},
            {"word": "coming of age", "translation": "совершеннолетие"}, {"word": "funeral", "translation": "похороны"},
            {"word": "wake", "translation": "поминки"}, {"word": "mourning", "translation": "траур"},
            {"word": "inheritance", "translation": "наследство"}, {"word": "heir", "translation": "наследник"},
            {"word": "heiress", "translation": "наследница"}, {"word": "will", "translation": "завещание"},
            {"word": "estate", "translation": "имущество"}, {"word": "legacy", "translation": "наследие"},
            {"word": "genealogy", "translation": "генеалогия"}, {"word": "family history", "translation": "история семьи"},
            {"word": "family tree", "translation": "родословное древо"}, {"word": "pedigree", "translation": "родословная"},
            {"word": "bloodline", "translation": "кровная линия"}, {"word": "dynasty", "translation": "династия"},
            {"word": "clan", "translation": "клан"}, {"word": "tribe", "translation": "племя"},
            {"word": "kinship", "translation": "родство"}, {"word": "family connection", "translation": "семейная связь"},
            {"word": "family relationship", "translation": "семейные отношения"}, {"word": "family dynamics", "translation": "семейная динамика"},
            {"word": "family role", "translation": "семейная роль"}, {"word": "family responsibility", "translation": "семейная ответственность"},
            {"word": "family duty", "translation": "семейный долг"}, {"word": "family obligation", "translation": "семейное обязательство"},
            {"word": "family care", "translation": "забота о семье"}, {"word": "family time", "translation": "семейное время"},
            {"word": "family outing", "translation": "семейный выход"}, {"word": "family vacation", "translation": "семейный отпуск"},
            {"word": "family trip", "translation": "семейная поездка"}, {"word": "family holiday", "translation": "семейный праздник"},
            {"word": "family celebration", "translation": "семейное празднование"}, {"word": "family party", "translation": "семейная вечеринка"},
            {"word": "family meal", "translation": "семейная трапеза"}, {"word": "family dinner", "translation": "семейный ужин"},
            {"word": "family lunch", "translation": "семейный обед"}, {"word": "family breakfast", "translation": "семейный завтрак"},
            {"word": "family recipe", "translation": "семейный рецепт"}, {"word": "family tradition", "translation": "семейная традиция"},
            {"word": "family custom", "translation": "семейный обычай"}, {"word": "family ritual", "translation": "семейный ритуал"},
            {"word": "family value", "translation": "семейная ценность"}, {"word": "family principle", "translation": "семейный принцип"},
            {"word": "family belief", "translation": "семейное убеждение"}, {"word": "family faith", "translation": "семейная вера"},
            {"word": "family religion", "translation": "семейная религия"}, {"word": "family culture", "translation": "семейная культура"},
            {"word": "family heritage", "translation": "семейное наследие"}, {"word": "family background", "translation": "семейное прошлое"},
            {"word": "family origin", "translation": "семейное происхождение"}, {"word": "family roots", "translation": "семейные корни"}
        ],
        "B1": [
            {"word": "matriarch", "translation": "матриарх"}, {"word": "patriarch", "translation": "патриарх"},
            {"word": "matrilineal", "translation": "матрилинейный"}, {"word": "patrilineal", "translation": "патрилинейный"},
            {"word": "primogeniture", "translation": "первородство"}, {"word": "birthright", "translation": "право первородства"},
            {"word": "kinship", "translation": "родство"}, {"word": "consanguinity", "translation": "кровное родство"},
            {"word": "affinity", "translation": "свойство (родство по браку)"}, {"word": "family of origin", "translation": "родная семья"},
            {"word": "family of choice", "translation": "выбранная семья"}, {"word": "blended family", "translation": "смешанная семья"},
            {"word": "nuclear family", "translation": "нуклеарная семья"}, {"word": "extended family", "translation": "расширенная семья"},
            {"word": "multigenerational", "translation": "многопоколенный"}, {"word": "intergenerational", "translation": "межпоколенный"},
            {"word": "family unit", "translation": "семейная ячейка"}, {"word": "household", "translation": "домохозяйство"},
            {"word": "domestic", "translation": "домашний"}, {"word": "familial", "translation": "семейный"},
            {"word": "filial piety", "translation": "сыновья почтительность"}, {"word": "family loyalty", "translation": "семейная верность"},
            {"word": "family honor", "translation": "семейная честь"}, {"word": "family pride", "translation": "семейная гордость"},
            {"word": "family reputation", "translation": "семейная репутация"}, {"word": "family name", "translation": "фамилия"},
            {"word": "family legacy", "translation": "семейное наследие"}, {"word": "family fortune", "translation": "семейное состояние"},
            {"word": "family wealth", "translation": "семейное богатство"}, {"word": "family property", "translation": "семейная собственность"},
            {"word": "family business", "translation": "семейный бизнес"}, {"word": "family enterprise", "translation": "семейное предприятие"},
            {"word": "family firm", "translation": "семейная фирма"}, {"word": "family company", "translation": "семейная компания"},
            {"word": "family corporation", "translation": "семейная корпорация"}, {"word": "family partnership", "translation": "семейное партнерство"},
            {"word": "family farm", "translation": "семейная ферма"}, {"word": "family ranch", "translation": "семейное ранчо"},
            {"word": "family estate", "translation": "семейное поместье"}, {"word": "family mansion", "translation": "семейный особняк"},
            {"word": "family home", "translation": "родовой дом"}, {"word": "family house", "translation": "семейный дом"},
            {"word": "family cottage", "translation": "семейный коттедж"}, {"word": "family villa", "translation": "семейная вилла"},
            {"word": "family castle", "translation": "семейный замок"}, {"word": "family seat", "translation": "родовое поместье"},
            {"word": "family vault", "translation": "семейный склеп"}, {"word": "family tomb", "translation": "семейная гробница"},
            {"word": "family cemetery", "translation": "семейное кладбище"}, {"word": "family plot", "translation": "семейный участок"},
            {"word": "family grave", "translation": "семейная могила"}, {"word": "family burial", "translation": "семейное захоронение"},
            {"word": "family reunion", "translation": "воссоединение семьи"}, {"word": "family gathering", "translation": "семейная встреча"},
            {"word": "family get-together", "translation": "семейная встреча"}, {"word": "family celebration", "translation": "семейное празднование"},
            {"word": "family occasion", "translation": "семейное событие"}, {"word": "family event", "translation": "семейное мероприятие"},
            {"word": "family function", "translation": "семейное мероприятие"}, {"word": "family party", "translation": "семейная вечеринка"},
            {"word": "family dinner", "translation": "семейный ужин"}, {"word": "family lunch", "translation": "семейный обед"},
            {"word": "family breakfast", "translation": "семейный завтрак"}, {"word": "family meal", "translation": "семейная трапеза"},
            {"word": "family feast", "translation": "семейное застолье"}, {"word": "family banquet", "translation": "семейный банкет"},
            {"word": "family barbecue", "translation": "семейный пикник"}, {"word": "family picnic", "translation": "семейный пикник"},
            {"word": "family outing", "translation": "семейный выход"}, {"word": "family excursion", "translation": "семейная экскурсия"},
            {"word": "family trip", "translation": "семейная поездка"}, {"word": "family vacation", "translation": "семейный отпуск"},
            {"word": "family holiday", "translation": "семейный праздник"}, {"word": "family tradition", "translation": "семейная традиция"},
            {"word": "family custom", "translation": "семейный обычай"}, {"word": "family ritual", "translation": "семейный ритуал"},
            {"word": "family practice", "translation": "семейная практика"}, {"word": "family habit", "translation": "семейная привычка"},
            {"word": "family pattern", "translation": "семейная модель"}, {"word": "family dynamic", "translation": "семейная динамика"},
            {"word": "family interaction", "translation": "семейное взаимодействие"}, {"word": "family relationship", "translation": "семейные отношения"},
            {"word": "family bond", "translation": "семейная связь"}, {"word": "family tie", "translation": "семейные узы"},
            {"word": "family connection", "translation": "семейная связь"}, {"word": "family link", "translation": "семейная связь"}
        ],
        "B2": [
            {"word": "genealogy", "translation": "генеалогия"}, {"word": "genealogist", "translation": "генеалог"},
            {"word": "family historian", "translation": "семейный историк"}, {"word": "family chronicle", "translation": "семейная хроника"},
            {"word": "family saga", "translation": "семейная сага"}, {"word": "family epic", "translation": "семейная эпопея"},
            {"word": "family narrative", "translation": "семейное повествование"}, {"word": "family story", "translation": "семейная история"},
            {"word": "family lore", "translation": "семейные предания"}, {"word": "family legend", "translation": "семейная легенда"},
            {"word": "family myth", "translation": "семейный миф"}, {"word": "family folklore", "translation": "семейный фольклор"},
            {"word": "family anecdote", "translation": "семейный анекдот"}, {"word": "family memory", "translation": "семейная память"},
            {"word": "family recollection", "translation": "семейное воспоминание"}, {"word": "family archive", "translation": "семейный архив"},
            {"word": "family record", "translation": "семейная запись"}, {"word": "family document", "translation": "семейный документ"},
            {"word": "family letter", "translation": "семейное письмо"}, {"word": "family correspondence", "translation": "семейная переписка"},
            {"word": "family diary", "translation": "семейный дневник"}, {"word": "family journal", "translation": "семейный журнал"},
            {"word": "family photograph", "translation": "семейная фотография"}, {"word": "family portrait", "translation": "семейный портрет"},
            {"word": "family painting", "translation": "семейная картина"}, {"word": "family drawing", "translation": "семейный рисунок"},
            {"word": "family silhouette", "translation": "семейный силуэт"}, {"word": "family miniature", "translation": "семейная миниатюра"},
            {"word": "family album", "translation": "семейный альбом"}, {"word": "family scrapbook", "translation": "семейный альбом для вырезок"},
            {"word": "family tree", "translation": "родословное древо"}, {"word": "family pedigree", "translation": "семейная родословная"},
            {"word": "family lineage", "translation": "семейное происхождение"}, {"word": "family ancestry", "translation": "семейные предки"},
            {"word": "family descent", "translation": "семейное происхождение"}, {"word": "family extraction", "translation": "семейное происхождение"},
            {"word": "family origin", "translation": "семейное происхождение"}, {"word": "family roots", "translation": "семейные корни"},
            {"word": "family background", "translation": "семейное прошлое"}, {"word": "family heritage", "translation": "семейное наследие"},
            {"word": "family inheritance", "translation": "семейное наследство"}, {"word": "family legacy", "translation": "семейное наследие"},
            {"word": "family bequest", "translation": "семейное завещание"}, {"word": "family endowment", "translation": "семейный дар"},
            {"word": "family trust", "translation": "семейный траст"}, {"word": "family foundation", "translation": "семейный фонд"},
            {"word": "family charity", "translation": "семейная благотворительность"}, {"word": "family philanthropy", "translation": "семейная филантропия"},
            {"word": "family patronage", "translation": "семейное покровительство"}, {"word": "family sponsorship", "translation": "семейное спонсорство"},
            {"word": "family support", "translation": "семейная поддержка"}, {"word": "family assistance", "translation": "семейная помощь"},
            {"word": "family aid", "translation": "семейная помощь"}, {"word": "family care", "translation": "семейная забота"},
            {"word": "family nurturing", "translation": "семейное воспитание"}, {"word": "family upbringing", "translation": "семейное воспитание"},
            {"word": "family education", "translation": "семейное образование"}, {"word": "family schooling", "translation": "семейное обучение"},
            {"word": "family tutoring", "translation": "семейное репетиторство"}, {"word": "family mentoring", "translation": "семейное наставничество"},
            {"word": "family guidance", "translation": "семейное руководство"}, {"word": "family direction", "translation": "семейное направление"},
            {"word": "family advice", "translation": "семейный совет"}, {"word": "family counsel", "translation": "семейный совет"},
            {"word": "family consultation", "translation": "семейная консультация"}, {"word": "family therapy", "translation": "семейная терапия"},
            {"word": "family counseling", "translation": "семейное консультирование"}, {"word": "family mediation", "translation": "семейная медиация"},
            {"word": "family arbitration", "translation": "семейный арбитраж"}, {"word": "family reconciliation", "translation": "семейное примирение"},
            {"word": "family harmony", "translation": "семейная гармония"}, {"word": "family peace", "translation": "семейный мир"},
            {"word": "family unity", "translation": "семейное единство"}, {"word": "family solidarity", "translation": "семейная солидарность"},
            {"word": "family cohesion", "translation": "семейная сплоченность"}, {"word": "family togetherness", "translation": "семейное единение"},
            {"word": "family closeness", "translation": "семейная близость"}, {"word": "family intimacy", "translation": "семейная интимность"},
            {"word": "family warmth", "translation": "семейное тепло"}, {"word": "family affection", "translation": "семейная привязанность"},
            {"word": "family love", "translation": "семейная любовь"}, {"word": "family devotion", "translation": "семейная преданность"},
            {"word": "family dedication", "translation": "семейная самоотверженность"}, {"word": "family commitment", "translation": "семейная приверженность"}
        ]
    },
    "education": {
        "A1": [
            {"word": "school", "translation": "школа"}, {"word": "college", "translation": "колледж"},
            {"word": "university", "translation": "университет"}, {"word": "kindergarten", "translation": "детский сад"},
            {"word": "nursery", "translation": "ясли"}, {"word": "preschool", "translation": "дошкольное учреждение"},
            {"word": "class", "translation": "класс"}, {"word": "lesson", "translation": "урок"},
            {"word": "course", "translation": "курс"}, {"word": "subject", "translation": "предмет"},
            {"word": "teacher", "translation": "учитель"}, {"word": "professor", "translation": "профессор"},
            {"word": "instructor", "translation": "инструктор"}, {"word": "tutor", "translation": "репетитор"},
            {"word": "student", "translation": "студент"}, {"word": "pupil", "translation": "ученик"},
            {"word": "classmate", "translation": "одноклассник"}, {"word": "friend", "translation": "друг"},
            {"word": "book", "translation": "книга"}, {"word": "notebook", "translation": "тетрадь"},
            {"word": "pen", "translation": "ручка"}, {"word": "pencil", "translation": "карандаш"},
            {"word": "eraser", "translation": "ластик"}, {"word": "ruler", "translation": "линейка"},
            {"word": "sharpener", "translation": "точилка"}, {"word": "backpack", "translation": "рюкзак"},
            {"word": "bag", "translation": "сумка"}, {"word": "desk", "translation": "парта"},
            {"word": "chair", "translation": "стул"}, {"word": "board", "translation": "доска"},
            {"word": "chalk", "translation": "мел"}, {"word": "marker", "translation": "маркер"},
            {"word": "computer", "translation": "компьютер"}, {"word": "laptop", "translation": "ноутбук"},
            {"word": "tablet", "translation": "планшет"}, {"word": "phone", "translation": "телефон"},
            {"word": "homework", "translation": "домашнее задание"}, {"word": "assignment", "translation": "задание"},
            {"word": "project", "translation": "проект"}, {"word": "presentation", "translation": "презентация"},
            {"word": "report", "translation": "доклад"}, {"word": "essay", "translation": "эссе"},
            {"word": "exam", "translation": "экзамен"}, {"word": "test", "translation": "тест"},
            {"word": "quiz", "translation": "викторина"}, {"word": "grade", "translation": "оценка"},
            {"word": "score", "translation": "балл"}, {"word": "mark", "translation": "отметка"},
            {"word": "pass", "translation": "сдать"}, {"word": "fail", "translation": "провалить"},
            {"word": "learn", "translation": "учить"}, {"word": "study", "translation": "изучать"},
            {"word": "teach", "translation": "преподавать"}, {"word": "explain", "translation": "объяснять"},
            {"word": "understand", "translation": "понимать"}, {"word": "know", "translation": "знать"},
            {"word": "remember", "translation": "помнить"}, {"word": "forget", "translation": "забывать"},
            {"word": "practice", "translation": "практиковать"}, {"word": "repeat", "translation": "повторять"},
            {"word": "review", "translation": "повторять"}, {"word": "read", "translation": "читать"},
            {"word": "write", "translation": "писать"}, {"word": "draw", "translation": "рисовать"},
            {"word": "count", "translation": "считать"}, {"word": "calculate", "translation": "вычислять"},
            {"word": "solve", "translation": "решать"}, {"word": "answer", "translation": "отвечать"},
            {"word": "ask", "translation": "спрашивать"}, {"word": "question", "translation": "вопрос"},
            {"word": "discuss", "translation": "обсуждать"}, {"word": "debate", "translation": "дискутировать"},
            {"word": "think", "translation": "думать"}, {"word": "consider", "translation": "рассматривать"},
            {"word": "decide", "translation": "решать"}, {"word": "choose", "translation": "выбирать"},
            {"word": "select", "translation": "выбирать"}, {"word": "pick", "translation": "выбирать"},
            {"word": "library", "translation": "библиотека"}, {"word": "bookstore", "translation": "книжный магазин"},
            {"word": "classroom", "translation": "классная комната"}, {"word": "laboratory", "translation": "лаборатория"},
            {"word": "cafeteria", "translation": "столовая"}, {"word": "playground", "translation": "площадка"},
            {"word": "gym", "translation": "спортзал"}, {"word": "auditorium", "translation": "актовый зал"},
            {"word": "dormitory", "translation": "общежитие"}, {"word": "campus", "translation": "кампус"},
            {"word": "education", "translation": "образование"}, {"word": "learning", "translation": "обучение"},
            {"word": "teaching", "translation": "преподавание"}, {"word": "knowledge", "translation": "знания"},
            {"word": "skill", "translation": "навык"}, {"word": "ability", "translation": "способность"},
            {"word": "talent", "translation": "талант"}, {"word": "intelligence", "translation": "интеллект"},
            {"word": "smart", "translation": "умный"}, {"word": "clever", "translation": "умный"},
            {"word": "intelligent", "translation": "интеллектуальный"}, {"word": "bright", "translation": "способный"}
        ],
        "A2": [
            {"word": "primary school", "translation": "начальная школа"}, {"word": "secondary school", "translation": "средняя школа"},
            {"word": "high school", "translation": "старшая школа"}, {"word": "vocational school", "translation": "профессиональная школа"},
            {"word": "graduate school", "translation": "аспирантура"}, {"word": "postgraduate", "translation": "аспирант"},
            {"word": "undergraduate", "translation": "студент бакалавриата"}, {"word": "bachelor", "translation": "бакалавр"},
            {"word": "master", "translation": "магистр"}, {"word": "doctorate", "translation": "докторантура"},
            {"word": "phd", "translation": "кандидат наук"}, {"word": "degree", "translation": "степень"},
            {"word": "diploma", "translation": "диплом"}, {"word": "certificate", "translation": "сертификат"},
            {"word": "qualification", "translation": "квалификация"}, {"word": "credential", "translation": "удостоверение"},
            {"word": "transcript", "translation": "выписка оценок"}, {"word": "record", "translation": "запись"},
            {"word": "major", "translation": "специализация"}, {"word": "minor", "translation": "дополнительная специализация"},
            {"word": "elective", "translation": "факультатив"}, {"word": "required", "translation": "обязательный"},
            {"word": "core", "translation": "основной"}, {"word": "optional", "translation": "необязательный"},
            {"word": "curriculum", "translation": "учебный план"}, {"word": "syllabus", "translation": "программа курса"},
            {"word": "schedule", "translation": "расписание"}, {"word": "timetable", "translation": "расписание"},
            {"word": "semester", "translation": "семестр"}, {"word": "trimester", "translation": "триместр"},
            {"word": "quarter", "translation": "четверть"}, {"word": "term", "translation": "семестр"},
            {"word": "academic year", "translation": "учебный год"}, {"word": "school year", "translation": "учебный год"},
            {"word": "holiday", "translation": "каникулы"}, {"word": "break", "translation": "перерыв"},
            {"word": "vacation", "translation": "отпуск"}, {"word": "summer break", "translation": "летние каникулы"},
            {"word": "winter break", "translation": "зимние каникулы"}, {"word": "spring break", "translation": "весенние каникулы"},
            {"word": "admission", "translation": "поступление"}, {"word": "application", "translation": "заявление"},
            {"word": "enrollment", "translation": "зачисление"}, {"word": "registration", "translation": "регистрация"},
            {"word": "orientation", "translation": "ориентация"}, {"word": "freshman", "translation": "первокурсник"},
            {"word": "sophomore", "translation": "второкурсник"}, {"word": "junior", "translation": "третьекурсник"},
            {"word": "senior", "translation": "выпускник"}, {"word": "alumnus", "translation": "выпускник"},
            {"word": "alumni", "translation": "выпускники"}, {"word": "faculty", "translation": "факультет"},
            {"word": "department", "translation": "кафедра"}, {"word": "division", "translation": "отделение"},
            {"word": "program", "translation": "программа"}, {"word": "coursework", "translation": "курсовая работа"},
            {"word": "research", "translation": "исследование"}, {"word": "thesis", "translation": "диссертация"},
            {"word": "dissertation", "translation": "диссертация"}, {"word": "paper", "translation": "работа"},
            {"word": "article", "translation": "статья"}, {"word": "journal", "translation": "журнал"},
            {"word": "textbook", "translation": "учебник"}, {"word": "workbook", "translation": "рабочая тетрадь"},
            {"word": "handbook", "translation": "справочник"}, {"word": "manual", "translation": "руководство"},
            {"word": "guide", "translation": "гид"}, {"word": "dictionary", "translation": "словарь"},
            {"word": "encyclopedia", "translation": "энциклопедия"}, {"word": "atlas", "translation": "атлас"},
            {"word": "globe", "translation": "глобус"}, {"word": "map", "translation": "карта"},
            {"word": "chart", "translation": "диаграмма"}, {"word": "graph", "translation": "график"},
            {"word": "diagram", "translation": "диаграмма"}, {"word": "illustration", "translation": "иллюстрация"},
            {"word": "photograph", "translation": "фотография"}, {"word": "image", "translation": "изображение"},
            {"word": "video", "translation": "видео"}, {"word": "audio", "translation": "аудио"},
            {"word": "recording", "translation": "запись"}, {"word": "lecture", "translation": "лекция"},
            {"word": "seminar", "translation": "семинар"}, {"word": "workshop", "translation": "мастер-класс"},
            {"word": "tutorial", "translation": "учебное пособие"}, {"word": "webinar", "translation": "вебинар"},
            {"word": "online course", "translation": "онлайн-курс"}, {"word": "distance learning", "translation": "дистанционное обучение"},
            {"word": "e-learning", "translation": "электронное обучение"}, {"word": "blended learning", "translation": "смешанное обучение"},
            {"word": "flipped classroom", "translation": "перевернутый класс"}, {"word": "homeschooling", "translation": "обучение на дому"}
        ],
        "B1": [
            {"word": "pedagogy", "translation": "педагогика"}, {"word": "andragogy", "translation": "андрагогика"},
            {"word": "didactics", "translation": "дидактика"}, {"word": "methodology", "translation": "методология"},
            {"word": "curriculum development", "translation": "разработка учебных программ"}, {"word": "lesson planning", "translation": "планирование уроков"},
            {"word": "teaching strategy", "translation": "стратегия обучения"}, {"word": "teaching technique", "translation": "методика обучения"},
            {"word": "teaching method", "translation": "метод обучения"}, {"word": "teaching approach", "translation": "подход к обучению"},
            {"word": "learning style", "translation": "стиль обучения"}, {"word": "learning preference", "translation": "предпочтение в обучении"},
            {"word": "multiple intelligences", "translation": "множественный интеллект"}, {"word": "cognitive development", "translation": "когнитивное развитие"},
            {"word": "intellectual development", "translation": "интеллектуальное развитие"}, {"word": "emotional development", "translation": "эмоциональное развитие"},
            {"word": "social development", "translation": "социальное развитие"}, {"word": "moral development", "translation": "моральное развитие"},
            {"word": "physical development", "translation": "физическое развитие"}, {"word": "child development", "translation": "развитие ребенка"},
            {"word": "adolescent development", "translation": "подростковое развитие"}, {"word": "adult education", "translation": "образование взрослых"},
            {"word": "continuing education", "translation": "непрерывное образование"}, {"word": "lifelong learning", "translation": "обучение на протяжении всей жизни"},
            {"word": "professional development", "translation": "профессиональное развитие"}, {"word": "staff development", "translation": "развитие персонала"},
            {"word": "teacher training", "translation": "подготовка учителей"}, {"word": "teacher education", "translation": "педагогическое образование"},
            {"word": "teacher certification", "translation": "сертификация учителей"}, {"word": "teacher licensure", "translation": "лицензирование учителей"},
            {"word": "teacher credential", "translation": "удостоверение учителя"}, {"word": "teacher qualification", "translation": "квалификация учителя"},
            {"word": "teacher competence", "translation": "компетентность учителя"}, {"word": "teacher effectiveness", "translation": "эффективность учителя"},
            {"word": "teacher performance", "translation": "работа учителя"}, {"word": "teacher evaluation", "translation": "оценка учителя"},
            {"word": "teacher assessment", "translation": "аттестация учителя"}, {"word": "teacher observation", "translation": "наблюдение за учителем"},
            {"word": "teacher feedback", "translation": "обратная связь учителю"}, {"word": "teacher mentoring", "translation": "наставничество учителей"},
            {"word": "teacher coaching", "translation": "коучинг учителей"}, {"word": "teacher supervision", "translation": "надзор за учителями"},
            {"word": "teacher leadership", "translation": "лидерство учителей"}, {"word": "teacher collaboration", "translation": "сотрудничество учителей"},
            {"word": "teacher teamwork", "translation": "командная работа учителей"}, {"word": "teacher community", "translation": "сообщество учителей"},
            {"word": "teacher network", "translation": "сеть учителей"}, {"word": "teacher association", "translation": "ассоциация учителей"},
            {"word": "teacher union", "translation": "профсоюз учителей"}, {"word": "teacher organization", "translation": "организация учителей"},
            {"word": "student engagement", "translation": "вовлеченность студентов"}, {"word": "student participation", "translation": "участие студентов"},
            {"word": "student involvement", "translation": "вовлеченность студентов"}, {"word": "student motivation", "translation": "мотивация студентов"},
            {"word": "student interest", "translation": "интерес студентов"}, {"word": "student attention", "translation": "внимание студентов"},
            {"word": "student concentration", "translation": "концентрация студентов"}, {"word": "student focus", "translation": "фокус студентов"},
            {"word": "student behavior", "translation": "поведение студентов"}, {"word": "student conduct", "translation": "поведение студентов"},
            {"word": "student discipline", "translation": "дисциплина студентов"}, {"word": "student attitude", "translation": "отношение студентов"},
            {"word": "student perception", "translation": "восприятие студентов"}, {"word": "student perspective", "translation": "точка зрения студентов"},
            {"word": "student experience", "translation": "опыт студентов"}, {"word": "student satisfaction", "translation": "удовлетворенность студентов"},
            {"word": "student achievement", "translation": "успеваемость студентов"}, {"word": "student performance", "translation": "успеваемость студентов"},
            {"word": "student progress", "translation": "прогресс студентов"}, {"word": "student improvement", "translation": "улучшение студентов"},
            {"word": "student growth", "translation": "рост студентов"}, {"word": "student development", "translation": "развитие студентов"},
            {"word": "student learning", "translation": "обучение студентов"}, {"word": "student outcomes", "translation": "результаты студентов"},
            {"word": "student success", "translation": "успех студентов"}, {"word": "student retention", "translation": "удержание студентов"},
            {"word": "student persistence", "translation": "настойчивость студентов"}, {"word": "student completion", "translation": "завершение обучения"},
            {"word": "student graduation", "translation": "выпуск студентов"}, {"word": "student dropout", "translation": "отсев студентов"},
            {"word": "student attrition", "translation": "отсев студентов"}, {"word": "student transfer", "translation": "перевод студентов"},
            {"word": "student mobility", "translation": "мобильность студентов"}, {"word": "student exchange", "translation": "обмен студентами"},
            {"word": "study abroad", "translation": "обучение за рубежом"}, {"word": "international student", "translation": "иностранный студент"},
            {"word": "exchange student", "translation": "студент по обмену"}, {"word": "visiting student", "translation": "приглашенный студент"}
        ],
        "B2": [
            {"word": "educational philosophy", "translation": "философия образования"}, {"word": "educational theory", "translation": "теория образования"},
            {"word": "educational psychology", "translation": "педагогическая психология"}, {"word": "educational sociology", "translation": "социология образования"},
            {"word": "educational anthropology", "translation": "антропология образования"}, {"word": "educational history", "translation": "история образования"},
            {"word": "educational policy", "translation": "образовательная политика"}, {"word": "educational reform", "translation": "образовательная реформа"},
            {"word": "educational innovation", "translation": "инновации в образовании"}, {"word": "educational technology", "translation": "образовательные технологии"},
            {"word": "educational research", "translation": "педагогические исследования"}, {"word": "educational assessment", "translation": "оценка в образовании"},
            {"word": "educational evaluation", "translation": "оценка образования"}, {"word": "educational measurement", "translation": "измерение в образовании"},
            {"word": "educational testing", "translation": "тестирование в образовании"}, {"word": "educational standards", "translation": "образовательные стандарты"},
            {"word": "educational objectives", "translation": "образовательные цели"}, {"word": "educational goals", "translation": "образовательные цели"},
            {"word": "educational aims", "translation": "образовательные цели"}, {"word": "educational outcomes", "translation": "образовательные результаты"},
            {"word": "educational attainment", "translation": "образовательный уровень"}, {"word": "educational achievement", "translation": "образовательные достижения"},
            {"word": "educational inequality", "translation": "неравенство в образовании"}, {"word": "educational equity", "translation": "равенство в образовании"},
            {"word": "educational access", "translation": "доступ к образованию"}, {"word": "educational opportunity", "translation": "образовательные возможности"},
            {"word": "educational disadvantage", "translation": "образовательное неравенство"}, {"word": "educational exclusion", "translation": "исключение из образования"},
            {"word": "educational inclusion", "translation": "инклюзия в образовании"}, {"word": "educational integration", "translation": "интеграция в образовании"},
            {"word": "educational segregation", "translation": "сегрегация в образовании"}, {"word": "educational diversity", "translation": "разнообразие в образовании"},
            {"word": "educational multiculturalism", "translation": "мультикультурализм в образовании"}, {"word": "educational interculturalism", "translation": "межкультурное образование"},
            {"word": "educational globalization", "translation": "глобализация образования"}, {"word": "educational internationalization", "translation": "интернационализация образования"},
            {"word": "educational comparativism", "translation": "сравнительное образование"}, {"word": "educational development", "translation": "развитие образования"},
            {"word": "educational planning", "translation": "планирование образования"}, {"word": "educational management", "translation": "управление образованием"},
            {"word": "educational administration", "translation": "администрирование образования"}, {"word": "educational leadership", "translation": "лидерство в образовании"},
            {"word": "educational governance", "translation": "управление образованием"}, {"word": "educational accountability", "translation": "подотчетность в образовании"},
            {"word": "educational transparency", "translation": "прозрачность в образовании"}, {"word": "educational quality", "translation": "качество образования"},
            {"word": "educational excellence", "translation": "совершенство в образовании"}, {"word": "educational effectiveness", "translation": "эффективность образования"},
            {"word": "educational efficiency", "translation": "эффективность образования"}, {"word": "educational productivity", "translation": "продуктивность образования"},
            {"word": "educational investment", "translation": "инвестиции в образование"}, {"word": "educational funding", "translation": "финансирование образования"},
            {"word": "educational expenditure", "translation": "расходы на образование"}, {"word": "educational resources", "translation": "образовательные ресурсы"},
            {"word": "educational infrastructure", "translation": "образовательная инфраструктура"}, {"word": "educational facilities", "translation": "образовательные учреждения"},
            {"word": "educational institutions", "translation": "образовательные учреждения"}, {"word": "educational organizations", "translation": "образовательные организации"},
            {"word": "educational associations", "translation": "образовательные ассоциации"}, {"word": "educational agencies", "translation": "образовательные агентства"},
            {"word": "educational authorities", "translation": "органы образования"}, {"word": "educational ministries", "translation": "министерства образования"},
            {"word": "educational departments", "translation": "департаменты образования"}, {"word": "educational boards", "translation": "советы по образованию"},
            {"word": "educational councils", "translation": "советы по образованию"}, {"word": "educational committees", "translation": "комитеты по образованию"},
            {"word": "educational commissions", "translation": "комиссии по образованию"}, {"word": "educational task forces", "translation": "целевые группы по образованию"},
            {"word": "educational working groups", "translation": "рабочие группы по образованию"}, {"word": "educational advisory boards", "translation": "консультативные советы по образованию"},
            {"word": "educational consultants", "translation": "консультанты по образованию"}, {"word": "educational experts", "translation": "эксперты в области образования"},
            {"word": "educational specialists", "translation": "специалисты в области образования"}, {"word": "educational professionals", "translation": "профессионалы в области образования"},
            {"word": "educational practitioners", "translation": "практики в области образования"}, {"word": "educational researchers", "translation": "исследователи в области образования"},
            {"word": "educational scholars", "translation": "ученые в области образования"}, {"word": "educational academics", "translation": "академики в области образования"},
            {"word": "educational theorists", "translation": "теоретики образования"}, {"word": "educational philosophers", "translation": "философы образования"},
            {"word": "educational psychologists", "translation": "психологи образования"}, {"word": "educational sociologists", "translation": "социологи образования"},
            {"word": "educational historians", "translation": "историки образования"}, {"word": "educational anthropologists", "translation": "антропологи образования"},
            {"word": "educational economists", "translation": "экономисты образования"}, {"word": "educational policymakers", "translation": "разработчики образовательной политики"},
            {"word": "educational reformers", "translation": "реформаторы образования"}, {"word": "educational innovators", "translation": "инноваторы в образовании"},
            {"word": "educational entrepreneurs", "translation": "предприниматели в образовании"}, {"word": "educational leaders", "translation": "лидеры в образовании"},
            {"word": "educational pioneers", "translation": "первопроходцы в образовании"}, {"word": "educational visionaries", "translation": "визионеры в образовании"},
            {"word": "educational advocates", "translation": "защитники образования"}, {"word": "educational activists", "translation": "активисты в образовании"},
            {"word": "educational champions", "translation": "сторонники образования"}, {"word": "educational supporters", "translation": "сторонники образования"},
            {"word": "educational promoters", "translation": "пропагандисты образования"}, {"word": "educational ambassadors", "translation": "послы образования"}
        ]
    }
}

# ========== ФУНКЦИЯ АУДИО ==========
def send_audio(chat_id, text):
    try:
        tts = gTTS(text=text, lang='en')
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as f:
            tts.save(f.name)
            with open(f.name, 'rb') as audio:
                bot.send_voice(chat_id, audio)
            os.unlink(f.name)
    except Exception as e:
        bot.send_message(chat_id, f"⚠️ Ошибка аудио: {e}")

# ========== ПОДСВЕТКА ОШИБОК ==========
def highlight_mistake(user_text, correct_word):
    user_text = user_text.lower().strip()
    correct_word = correct_word.lower().strip()
    if user_text == correct_word:
        return None
    diff = []
    for i, (u, c) in enumerate(zip(user_text, correct_word)):
        if u != c:
            diff.append(f"позиция {i+1}: должно быть *{c}*, ты написала *{u}*")
    if len(user_text) > len(correct_word):
        diff.append(f"лишние символы: *{user_text[len(correct_word):]}*")
    elif len(correct_word) > len(user_text):
        diff.append(f"не хватает: *{correct_word[len(user_text):]}*")
    return diff

# ========== ПРИВЕТСТВИЕ ==========
@bot.message_handler(commands=['start'])
def start(message):
    uid = message.from_user.id
    user_data[uid] = {"level": "A1", "topic": "food", "word": None}
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("👂 Аудирование")
    bot.send_message(
        message.chat.id,
        "👋 *Добро пожаловать в тренажёр английского!*\n\n"
        "Я помогу тебе выучить новые слова и улучшить произношение.\n\n"
        "🎯 *Как это работает:*\n"
        "1. Выбираешь тему и уровень сложности\n"
        "2. Я присылаю слово голосом\n"
        "3. Ты пишешь перевод\n"
        "4. Если ошибёшься — я покажу, где именно\n"
        "5. Не знаешь слово? Нажми «❓ Не знаю»\n\n"
        "После каждого задания ты можешь:\n"
        "🔁 *Продолжить* — то же слово\n"
        "📂 *Сменить тему*\n"
        "📊 *Сменить уровень*\n"
        "🏠 *Вернуться в меню*\n\n"
        "⬇️ Нажми кнопку ниже, чтобы начать",
        parse_mode="Markdown",
        reply_markup=markup
    )

# ========== ГЛАВНОЕ МЕНЮ ==========
@bot.message_handler(func=lambda m: m.text == "🏠 Главное меню")
def main_menu(m):
    start(m)

# ========== НАЧАЛО АУДИРОВАНИЯ ==========
@bot.message_handler(func=lambda m: m.text == "👂 Аудирование")
def choose_topic(m):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for t in TOPICS:
        markup.add(t)
    markup.add("🏠 Главное меню")
    bot.send_message(m.chat.id, "Выбери тему:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in TOPICS)
def choose_level(m):
    uid = m.from_user.id
    user_data[uid]["topic"] = m.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for l in LEVELS:
        markup.add(l)
    markup.add("🏠 Главное меню")
    bot.send_message(m.chat.id, f"Тема: *{m.text}*\nВыбери уровень:", parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in LEVELS)
def send_word(m):
    uid = m.from_user.id
    user_data[uid]["level"] = m.text
    topic = user_data[uid]["topic"]
    level = user_data[uid]["level"]
    words = WORD_BASE.get(topic, {}).get(level, [])
    if not words:
        bot.send_message(m.chat.id, "Нет слов для этой темы и уровня")
        return
    word = random.choice(words)
    user_data[uid]["word"] = word
    send_audio(m.chat.id, word["word"])
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("❓ Не знаю")
    markup.add("🏠 Главное меню")
    bot.send_message(m.chat.id, "📝 Напиши перевод слова:", reply_markup=markup)

# ========== НЕ ЗНАЮ ==========
@bot.message_handler(func=lambda m: m.text == "❓ Не знаю")
def dont_know(m):
    uid = m.from_user.id
    word = user_data[uid].get("word")
    if word:
        bot.send_message(
            m.chat.id,
            f"🔍 Слово: *{word['word']}*\nПеревод: *{word['translation']}*",
            parse_mode="Markdown"
        )
        after_task_menu(m)

# ========== ПРОВЕРКА СЛОВА ==========
@bot.message_handler(func=lambda m: user_data.get(m.from_user.id, {}).get("word") and m.text not in ["❓ Не знаю", "🏠 Главное меню", "🔁 Продолжить", "📂 Сменить тему", "📊 Сменить уровень"])
def check_word(m):
    uid = m.from_user.id
    word = user_data[uid]["word"]
    user_word = m.text.strip().lower()
    correct_word = word["word"].lower()
    translation = word["translation"]

    if user_word == correct_word:
        bot.send_message(
            m.chat.id,
            f"✅ *Верно!*\n\nСлово: *{correct_word}*\nПеревод: *{translation}*",
            parse_mode="Markdown"
        )
    else:
        diff = highlight_mistake(user_word, correct_word)
        msg = f"❌ *Ошибка*\n\nТы написала: {user_word}\nПравильно: {correct_word}\n\nПеревод: *{translation}*"
        if diff:
            msg += "\n\n*Где ошибка:*\n" + "\n".join(diff)
        bot.send_message(m.chat.id, msg, parse_mode="Markdown")
    after_task_menu(m)

# ========== МЕНЮ ПОСЛЕ ЗАДАНИЯ ==========
def after_task_menu(m):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🔁 Продолжить", "📂 Сменить тему")
    markup.add("📊 Сменить уровень", "🏠 Главное меню")
    bot.send_message(m.chat.id, "Что дальше?", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "🔁 Продолжить")
def continue_task(m):
    send_word(m)

@bot.message_handler(func=lambda m: m.text == "📂 Сменить тему")
def change_topic(m):
    choose_topic(m)

@bot.message_handler(func=lambda m: m.text == "📊 Сменить уровень")
def change_level(m):
    uid = m.from_user.id
    topic = user_data[uid]["topic"]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for l in LEVELS:
        markup.add(l)
    markup.add("🏠 Главное меню")
    bot.send_message(m.chat.id, f"Тема: *{topic}*\nВыбери уровень:", parse_mode="Markdown", reply_markup=markup)

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    print("✅ БОТ ЗАПУЩЕН")
    total = sum(len(WORD_BASE[t][l]) for t in WORD_BASE for l in WORD_BASE[t])
    print(f"Всего слов в базе: {total}")
    bot.polling(none_stop=True)