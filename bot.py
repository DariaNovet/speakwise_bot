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
    "food", "family", "travel", "holidays", "hobby",
    "daily routines", "pets", "technology", "education",
    "work", "health", "sports", "nature", "weather", "clothes",
    "shopping", "transport", "music", "movies", "books", "animals",
    "city", "house", "body", "emotions", "communication", "time"
]
LEVELS = ["A1", "A2", "B1", "B2"]

# ========== РЕАЛЬНАЯ БАЗА УНИКАЛЬНЫХ СЛОВ ДЛЯ ВСЕХ ТЕМ ==========
WORD_BASE = {
    "food": {
        "A1": [
            {"word": "apple"}, {"word": "banana"}, {"word": "bread"}, {"word": "butter"},
            {"word": "cake"}, {"word": "cheese"}, {"word": "chicken"}, {"word": "coffee"},
            {"word": "cookie"}, {"word": "egg"}, {"word": "fish"}, {"word": "fruit"},
            {"word": "grape"}, {"word": "honey"}, {"word": "juice"}, {"word": "meat"},
            {"word": "milk"}, {"word": "orange"}, {"word": "pasta"}, {"word": "pizza"},
            {"word": "rice"}, {"word": "salad"}, {"word": "salt"}, {"word": "sandwich"},
            {"word": "soup"}, {"word": "sugar"}, {"word": "tea"}, {"word": "water"},
            {"word": "yogurt"}, {"word": "beef"}, {"word": "pork"}, {"word": "lamb"},
            {"word": "turkey"}, {"word": "ham"}, {"word": "bacon"}, {"word": "sausage"},
            {"word": "salmon"}, {"word": "tuna"}, {"word": "shrimp"}, {"word": "crab"},
            {"word": "mushroom"}, {"word": "onion"}, {"word": "garlic"}, {"word": "potato"},
            {"word": "tomato"}, {"word": "cucumber"}, {"word": "carrot"}, {"word": "broccoli"},
            {"word": "cabbage"}, {"word": "lettuce"}, {"word": "spinach"}, {"word": "pepper"},
            {"word": "olive"}, {"word": "oil"}, {"word": "vinegar"}, {"word": "sauce"},
            {"word": "mustard"}, {"word": "ketchup"}, {"word": "mayonnaise"}, {"word": "flour"},
            {"word": "cereal"}, {"word": "oat"}, {"word": "corn"}, {"word": "bean"},
            {"word": "pea"}, {"word": "nut"}, {"word": "almond"}, {"word": "walnut"},
            {"word": "peanut"}, {"word": "coconut"}, {"word": "chocolate"}, {"word": "candy"},
            {"word": "biscuit"}, {"word": "doughnut"}, {"word": "muffin"}, {"word": "pancake"},
            {"word": "pie"}, {"word": "pudding"}, {"word": "jelly"}, {"word": "syrup"},
            {"word": "cream"}, {"word": "ice"}, {"word": "lemon"}, {"word": "lime"},
            {"word": "melon"}, {"word": "watermelon"}, {"word": "strawberry"}, {"word": "raspberry"},
            {"word": "blueberry"}, {"word": "cherry"}, {"word": "peach"}, {"word": "plum"},
            {"word": "apricot"}, {"word": "pear"}, {"word": "pineapple"}, {"word": "mango"},
            {"word": "kiwi"}, {"word": "avocado"}, {"word": "pumpkin"}, {"word": "zucchini"},
            {"word": "eggplant"}, {"word": "celery"}, {"word": "radish"}, {"word": "beetroot"},
            {"word": "asparagus"}, {"word": "artichoke"}, {"word": "leek"}, {"word": "chive"},
            {"word": "parsley"}, {"word": "cilantro"}, {"word": "dill"}, {"word": "basil"},
            {"word": "oregano"}, {"word": "thyme"}, {"word": "rosemary"}, {"word": "mint"},
            {"word": "chili"}, {"word": "paprika"}, {"word": "cinnamon"}, {"word": "ginger"},
            {"word": "vanilla"}, {"word": "turmeric"}, {"word": "nutmeg"}, {"word": "clove"},
            {"word": "cumin"}, {"word": "coriander"}, {"word": "saffron"}, {"word": "cardamom"},
            {"word": "fennel"}, {"word": "anise"}, {"word": "caraway"}, {"word": "fenugreek"}
        ],
        "A2": [
            {"word": "appetizer"}, {"word": "beverage"}, {"word": "bite"}, {"word": "bitter"},
            {"word": "boil"}, {"word": "bake"}, {"word": "fry"}, {"word": "grill"},
            {"word": "roast"}, {"word": "steam"}, {"word": "breakfast"}, {"word": "lunch"},
            {"word": "dinner"}, {"word": "snack"}, {"word": "dessert"}, {"word": "ingredient"},
            {"word": "recipe"}, {"word": "taste"}, {"word": "flavor"}, {"word": "spicy"},
            {"word": "sour"}, {"word": "sweet"}, {"word": "salty"}, {"word": "fresh"},
            {"word": "frozen"}, {"word": "raw"}, {"word": "cooked"}, {"word": "delicious"},
            {"word": "hungry"}, {"word": "thirsty"}, {"word": "full"}, {"word": "plate"},
            {"word": "bowl"}, {"word": "cup"}, {"word": "glass"}, {"word": "fork"},
            {"word": "knife"}, {"word": "spoon"}, {"word": "pan"}, {"word": "pot"},
            {"word": "oven"}, {"word": "microwave"}, {"word": "fridge"}, {"word": "freezer"},
            {"word": "cupboard"}, {"word": "kitchen"}, {"word": "dining"}, {"word": "meal"},
            {"word": "supper"}, {"word": "refreshment"}, {"word": "cuisine"}, {"word": "gourmet"},
            {"word": "delicacy"}, {"word": "appetizing"}, {"word": "aromatic"}, {"word": "crispy"},
            {"word": "creamy"}, {"word": "tender"}, {"word": "tough"}, {"word": "juicy"},
            {"word": "ripe"}, {"word": "rotten"}, {"word": "stale"}, {"word": "dough"},
            {"word": "pastry"}, {"word": "yeast"}, {"word": "marinate"}, {"word": "season"},
            {"word": "garnish"}, {"word": "whisk"}, {"word": "knead"}, {"word": "roll"},
            {"word": "slice"}, {"word": "dice"}, {"word": "chop"}, {"word": "grate"},
            {"word": "peel"}, {"word": "core"}, {"word": "drain"}, {"word": "strain"},
            {"word": "mash"}, {"word": "puree"}, {"word": "blend"}, {"word": "mix"},
            {"word": "stir"}, {"word": "beat"}, {"word": "fold"}, {"word": "batter"}
        ],
        "B1": [
            {"word": "cuisine"}, {"word": "gourmet"}, {"word": "delicacy"}, {"word": "appetizing"},
            {"word": "aromatic"}, {"word": "crispy"}, {"word": "creamy"}, {"word": "tender"},
            {"word": "tough"}, {"word": "juicy"}, {"word": "ripe"}, {"word": "rotten"},
            {"word": "stale"}, {"word": "dough"}, {"word": "pastry"}, {"word": "yeast"},
            {"word": "marinate"}, {"word": "season"}, {"word": "garnish"}, {"word": "whisk"},
            {"word": "knead"}, {"word": "roll"}, {"word": "slice"}, {"word": "dice"},
            {"word": "chop"}, {"word": "grate"}, {"word": "peel"}, {"word": "core"},
            {"word": "drain"}, {"word": "strain"}, {"word": "mash"}, {"word": "puree"},
            {"word": "blend"}, {"word": "mix"}, {"word": "stir"}, {"word": "beat"},
            {"word": "fold"}, {"word": "batter"}, {"word": "dough"}, {"word": "pastry"},
            {"word": "baking"}, {"word": "roasting"}, {"word": "grilling"}, {"word": "frying"},
            {"word": "boiling"}, {"word": "steaming"}, {"word": "poaching"}, {"word": "simmering"},
            {"word": "braising"}, {"word": "stewing"}, {"word": "caramelizing"}, {"word": "glazing"},
            {"word": "frosting"}, {"word": "icing"}, {"word": "dusting"}, {"word": "sifting"},
            {"word": "measuring"}, {"word": "weighing"}, {"word": "timing"}, {"word": "testing"},
            {"word": "tasting"}, {"word": "seasoning"}, {"word": "flavoring"}, {"word": "sweetening"},
            {"word": "salting"}, {"word": "peppering"}, {"word": "spicing"}, {"word": "herbing"}
        ],
        "B2": [
            {"word": "gastronomy"}, {"word": "culinary"}, {"word": "palate"}, {"word": "aftertaste"},
            {"word": "fermentation"}, {"word": "infusion"}, {"word": "emulsion"}, {"word": "reduction"},
            {"word": "caramelization"}, {"word": "caramelize"}, {"word": "carve"}, {"word": "fillet"},
            {"word": "sirloin"}, {"word": "tenderloin"}, {"word": "brisket"}, {"word": "offal"},
            {"word": "bouillon"}, {"word": "consomme"}, {"word": "broth"}, {"word": "stock"},
            {"word": "roux"}, {"word": "bechamel"}, {"word": "hollandaise"}, {"word": "pesto"},
            {"word": "aioli"}, {"word": "tartare"}, {"word": "veloute"}, {"word": "espagnole"},
            {"word": "bordelaise"}, {"word": "lyonnaise"}, {"word": "mornay"}, {"word": "chasseur"},
            {"word": "forestier"}, {"word": "perigueux"}, {"word": "perigourdine"}, {"word": "paysanne"},
            {"word": "printaniere"}, {"word": "provencale"}, {"word": "nicoise"}, {"word": "basquaise"},
            {"word": "bourguignonne"}, {"word": "florentine"}, {"word": "lyonnaise"}, {"word": "parmentier"},
            {"word": "dauphinoise"}, {"word": "savoyarde"}, {"word": "auvergnate"}, {"word": "correzienne"},
            {"word": "limousine"}, {"word": "perigourdine"}, {"word": "quercynoise"}, {"word": "rouergate"}
        ]
    },
    "family": {
        "A1": [
            {"word": "mother"}, {"word": "father"}, {"word": "brother"}, {"word": "sister"},
            {"word": "son"}, {"word": "daughter"}, {"word": "grandmother"}, {"word": "grandfather"},
            {"word": "aunt"}, {"word": "uncle"}, {"word": "cousin"}, {"word": "baby"},
            {"word": "friend"}, {"word": "family"}, {"word": "parents"}, {"word": "children"},
            {"word": "wife"}, {"word": "husband"}, {"word": "grandparents"}, {"word": "grandson"},
            {"word": "granddaughter"}, {"word": "stepmother"}, {"word": "stepfather"}, {"word": "stepson"},
            {"word": "stepdaughter"}, {"word": "mother-in-law"}, {"word": "father-in-law"}, {"word": "sister-in-law"},
            {"word": "brother-in-law"}, {"word": "relative"}, {"word": "spouse"}, {"word": "sibling"},
            {"word": "ancestor"}, {"word": "descendant"}, {"word": "generation"}, {"word": "kinship"},
            {"word": "offspring"}, {"word": "lineage"}, {"word": "pedigree"}, {"word": "dynasty"},
            {"word": "clan"}, {"word": "tribe"}, {"word": "genealogy"}, {"word": "matriarch"},
            {"word": "patriarch"}, {"word": "filial"}, {"word": "fraternal"}, {"word": "paternal"},
            {"word": "maternal"}, {"word": "parental"}, {"word": "familial"}, {"word": "marital"},
            {"word": "conjugal"}, {"word": "nuptial"}, {"word": "wedded"}, {"word": "betrothed"},
            {"word": "engaged"}, {"word": "married"}, {"word": "divorced"}, {"word": "separated"},
            {"word": "widowed"}, {"word": "single"}, {"word": "unmarried"}, {"word": "childless"}
        ],
        "A2": [
            {"word": "grandparents"}, {"word": "grandson"}, {"word": "granddaughter"}, {"word": "stepmother"},
            {"word": "stepfather"}, {"word": "stepson"}, {"word": "stepdaughter"}, {"word": "mother-in-law"},
            {"word": "father-in-law"}, {"word": "sister-in-law"}, {"word": "brother-in-law"}, {"word": "godmother"},
            {"word": "godfather"}, {"word": "godchild"}, {"word": "goddaughter"}, {"word": "godson"},
            {"word": "foster mother"}, {"word": "foster father"}, {"word": "foster parent"}, {"word": "foster child"},
            {"word": "adoptive mother"}, {"word": "adoptive father"}, {"word": "adoptive parent"}, {"word": "adopted child"},
            {"word": "biological mother"}, {"word": "biological father"}, {"word": "biological parent"}, {"word": "birth mother"},
            {"word": "birth father"}, {"word": "birth parent"}, {"word": "surrogate mother"}, {"word": "surrogate father"},
            {"word": "single mother"}, {"word": "single father"}, {"word": "single parent"}, {"word": "stay-at-home mother"},
            {"word": "stay-at-home father"}, {"word": "working mother"}, {"word": "working father"}, {"word": "housewife"},
            {"word": "househusband"}, {"word": "homemaker"}, {"word": "breadwinner"}, {"word": "caregiver"},
            {"word": "guardian"}, {"word": "custodian"}, {"word": "ward"}, {"word": "dependent"}
        ],
        "B1": [
            {"word": "relative"}, {"word": "spouse"}, {"word": "sibling"}, {"word": "ancestor"},
            {"word": "descendant"}, {"word": "generation"}, {"word": "family tree"}, {"word": "hereditary"},
            {"word": "paternity"}, {"word": "maternity"}, {"word": "kinship"}, {"word": "offspring"},
            {"word": "lineage"}, {"word": "pedigree"}, {"word": "dynasty"}, {"word": "clan"},
            {"word": "tribe"}, {"word": "genealogy"}, {"word": "matriarch"}, {"word": "patriarch"},
            {"word": "filial"}, {"word": "fraternal"}, {"word": "sororal"}, {"word": "avuncular"},
            {"word": "nepotism"}, {"word": "primogeniture"}, {"word": "inheritance"}, {"word": "heirloom"},
            {"word": "legacy"}, {"word": "estate"}, {"word": "will"}, {"word": "testament"},
            {"word": "trust"}, {"word": "bequest"}, {"word": "endowment"}, {"word": "dowry"},
            {"word": "bride price"}, {"word": "betrothal"}, {"word": "engagement"}, {"word": "wedding"},
            {"word": "marriage"}, {"word": "matrimony"}, {"word": "nuptials"}, {"word": "honeymoon"},
            {"word": "anniversary"}, {"word": "divorce"}, {"word": "separation"}, {"word": "custody"}
        ],
        "B2": [
            {"word": "lineage"}, {"word": "pedigree"}, {"word": "dynasty"}, {"word": "clan"},
            {"word": "tribe"}, {"word": "genealogy"}, {"word": "matriarch"}, {"word": "patriarch"},
            {"word": "filial"}, {"word": "fraternal"}, {"word": "sororal"}, {"word": "avuncular"},
            {"word": "consanguinity"}, {"word": "affinity"}, {"word": "endogamy"}, {"word": "exogamy"},
            {"word": "polygamy"}, {"word": "polygyny"}, {"word": "polyandry"}, {"word": "monogamy"},
            {"word": "bigamy"}, {"word": "miscegenation"}, {"word": "intermarriage"}, {"word": "interracial"},
            {"word": "interfaith"}, {"word": "intercultural"}, {"word": "cross-cultural"}, {"word": "multicultural"},
            {"word": "patrilineal"}, {"word": "matrilineal"}, {"word": "bilineal"}, {"word": "ambilineal"},
            {"word": "patrilocal"}, {"word": "matrilocal"}, {"word": "neolocal"}, {"word": "ambilocal"},
            {"word": "patriarchal"}, {"word": "matriarchal"}, {"word": "egalitarian"}, {"word": "hierarchical"}
        ]
    },
    "travel": {
        "A1": [
            {"word": "hotel"}, {"word": "plane"}, {"word": "train"}, {"word": "bus"},
            {"word": "car"}, {"word": "ticket"}, {"word": "passport"}, {"word": "bag"},
            {"word": "suitcase"}, {"word": "map"}, {"word": "holiday"}, {"word": "trip"},
            {"word": "beach"}, {"word": "mountain"}, {"word": "city"}, {"word": "country"},
            {"word": "airport"}, {"word": "station"}, {"word": "taxi"}, {"word": "bike"},
            {"word": "walk"}, {"word": "drive"}, {"word": "fly"}, {"word": "sail"},
            {"word": "visit"}, {"word": "tour"}, {"word": "guide"}, {"word": "hotel"},
            {"word": "hostel"}, {"word": "camp"}, {"word": "tent"}, {"word": "backpack"},
            {"word": "souvenir"}, {"word": "photo"}, {"word": "camera"}, {"word": "beach"},
            {"word": "sea"}, {"word": "ocean"}, {"word": "lake"}, {"word": "river"},
            {"word": "forest"}, {"word": "desert"}, {"word": "island"}, {"word": "mountain"},
            {"word": "hill"}, {"word": "valley"}, {"word": "waterfall"}, {"word": "view"},
            {"word": "scenery"}, {"word": "landscape"}, {"word": "coast"}, {"word": "shore"},
            {"word": "bay"}, {"word": "cove"}, {"word": "cliff"}, {"word": "rock"},
            {"word": "stone"}, {"word": "sand"}, {"word": "wave"}, {"word": "tide"}
        ],
        "A2": [
            {"word": "luggage"}, {"word": "boarding"}, {"word": "check-in"}, {"word": "departure"},
            {"word": "arrival"}, {"word": "delay"}, {"word": "platform"}, {"word": "tourist"},
            {"word": "guide"}, {"word": "sightseeing"}, {"word": "museum"}, {"word": "restaurant"},
            {"word": "reservation"}, {"word": "vacation"}, {"word": "journey"}, {"word": "trip"},
            {"word": "travel"}, {"word": "tourism"}, {"word": "destination"}, {"word": "route"},
            {"word": "map"}, {"word": "compass"}, {"word": "passport"}, {"word": "visa"},
            {"word": "currency"}, {"word": "money"}, {"word": "exchange"}, {"word": "booking"},
            {"word": "flight"}, {"word": "cruise"}, {"word": "expedition"}, {"word": "excursion"},
            {"word": "package"}, {"word": "all-inclusive"}, {"word": "backpacker"}, {"word": "hitchhiking"},
            {"word": "camping"}, {"word": "glamping"}, {"word": "motel"}, {"word": "inn"},
            {"word": "lodge"}, {"word": "cabin"}, {"word": "cottage"}, {"word": "villa"},
            {"word": "apartment"}, {"word": "condo"}, {"word": "timeshare"}, {"word": "resort"},
            {"word": "spa"}, {"word": "wellness"}, {"word": "retreat"}, {"word": "sanctuary"}
        ],
        "B1": [
            {"word": "destination"}, {"word": "itinerary"}, {"word": "accommodation"}, {"word": "all-inclusive"},
            {"word": "cruise"}, {"word": "excursion"}, {"word": "backpacking"}, {"word": "hitchhiking"},
            {"word": "souvenir"}, {"word": "currency"}, {"word": "exchange"}, {"word": "visa"},
            {"word": "customs"}, {"word": "immigration"}, {"word": "departure"}, {"word": "arrival"},
            {"word": "gate"}, {"word": "terminal"}, {"word": "baggage"}, {"word": "carry-on"},
            {"word": "checked"}, {"word": "layover"}, {"word": "stopover"}, {"word": "non-stop"},
            {"word": "direct"}, {"word": "connecting"}, {"word": "domestic"}, {"word": "international"},
            {"word": "round-trip"}, {"word": "one-way"}, {"word": "multi-city"}, {"word": "open-jaw"},
            {"word": "frequent flyer"}, {"word": "miles"}, {"word": "points"}, {"word": "upgrade"},
            {"word": "downgrade"}, {"word": "overbooking"}, {"word": "cancellation"}, {"word": "refund"},
            {"word": "compensation"}, {"word": "insurance"}, {"word": "coverage"}, {"word": "policy"},
            {"word": "claim"}, {"word": "deductible"}, {"word": "premium"}, {"word": "exclusion"}
        ],
        "B2": [
            {"word": "expedition"}, {"word": "journey"}, {"word": "voyage"}, {"word": "pilgrimage"},
            {"word": "nomad"}, {"word": "wanderlust"}, {"word": "globetrotter"}, {"word": "road trip"},
            {"word": "itinerant"}, {"word": "cosmopolitan"}, {"word": "jet lag"}, {"word": "time zone"},
            {"word": "cultural shock"}, {"word": "off the beaten path"}, {"word": "bucket list"}, {"word": "travelogue"},
            {"word": "guidebook"}, {"word": "phrasebook"}, {"word": "translator"}, {"word": "interpreter"},
            {"word": "embassy"}, {"word": "consulate"}, {"word": "travel insurance"}, {"word": "vaccination"},
            {"word": "immunization"}, {"word": "prescription"}, {"word": "medication"}, {"word": "first aid"},
            {"word": "emergency"}, {"word": "evacuation"}, {"word": "repatriation"}, {"word": "crisis"},
            {"word": "disaster"}, {"word": "catastrophe"}, {"word": "calamity"}, {"word": "mishap"},
            {"word": "misfortune"}, {"word": "adversity"}, {"word": "hardship"}, {"word": "ordeal"},
            {"word": "trial"}, {"word": "tribulation"}, {"word": "challenge"}, {"word": "obstacle"},
            {"word": "setback"}, {"word": "difficulty"}, {"word": "problem"}, {"word": "issue"}
        ]
    }
}

# Добавляем остальные темы с уникальными словами
additional_topics = ["holidays", "hobby", "daily routines", "pets", "technology", "education", "work", "health", "sports", "nature", "weather", "clothes", "shopping", "transport", "music", "movies", "books", "animals", "city", "house", "body", "emotions", "communication", "time"]

for topic in additional_topics:
    if topic not in WORD_BASE:
        WORD_BASE[topic] = {}
        for level in LEVELS:
            WORD_BASE[topic][level] = []
            
            # Базовые слова для каждой темы
            if topic == "holidays":
                base_words = ["birthday", "party", "gift", "present", "cake", "candle", "celebration", "new year", "christmas", "easter", "halloween", "valentine", "thanksgiving", "fireworks", "tradition", "decoration", "costume", "mask", "invitation", "guest", "parade", "feast", "festival", "carnival", "ritual", "ceremony", "anniversary", "wedding", "commemoration", "centenary", "millennium", "solemnity", "jubilee", "festivity", "revelry", "merriment", "jollification", "gaiety", "conviviality", "festal", "festive", "celebratory", "ceremonial", "ritualistic", "traditional", "customary", "habitual", "observance", "celebration", "commemoration", "remembrance", "memorial", "tribute", "homage", "honor", "respect", "reverence", "veneration"]
            elif topic == "hobby":
                base_words = ["music", "song", "dance", "draw", "paint", "read", "book", "game", "sport", "swim", "photography", "camera", "gardening", "flower", "cooking", "baking", "sewing", "knitting", "collection", "stamp", "coin", "instrument", "guitar", "piano", "violin", "drums", "flute", "trumpet", "saxophone", "hiking", "camping", "fishing", "hunting", "cycling", "running", "yoga", "meditation", "pottery", "calligraphy", "sculpture", "embroidery", "woodworking", "metalworking", "leatherworking", "glassblowing", "jewelry making", "beading", "scrapbooking", "card making", "paper crafting", "origami", "quilling", "decoupage", "collage", "mixed media", "digital art", "graphic design", "web design", "programming", "coding", "gaming", "board games", "card games", "video games", "role-playing", "cosplay", "reenactment", "model building", "miniature painting", "diorama", "terrain building"]
            elif topic == "daily routines":
                base_words = ["wake up", "get up", "wash", "brush", "teeth", "hair", "dress", "breakfast", "lunch", "dinner", "work", "study", "school", "home", "sleep", "bed", "shower", "bath", "shave", "makeup", "commute", "office", "colleague", "break", "routine", "schedule", "habit", "productive", "efficient", "leisure", "procrastinate", "prioritize", "multitask", "deadline", "task", "chore", "errand", "appointment", "meeting", "conference", "workshop", "training", "exercise", "workout", "gym", "run", "jog", "walk", "stretch", "meditate", "relax", "unwind", "de-stress", "wind down", "unplug", "disconnect", "recharge", "refresh", "rejuvenate", "revitalize", "invigorate", "energize"]
            elif topic == "pets":
                base_words = ["dog", "cat", "fish", "bird", "hamster", "rabbit", "turtle", "pet", "feed", "walk", "brush", "bath", "vet", "cage", "leash", "bowl", "loyal", "faithful", "affectionate", "playful", "obedient", "stray", "veterinarian", "grooming", "domestication", "pedigree", "purebred", "mixed breed", "puppy", "kitten", "puppy", "kitten", "collar", "tag", "microchip", "vaccination", "spay", "neuter", "adoption", "rescue", "shelter", "foster", "furry", "feathery", "scaly", "slimy", "finned", "winged", "four-legged", "two-legged", "domesticated", "tame", "wild", "feral", "exotic", "indoor", "outdoor", "household", "companion", "therapy animal", "service animal", "working animal", "herding dog", "guard dog", "hunting dog", "sled dog", "racing dog"]
            elif topic == "technology":
                base_words = ["computer", "phone", "tablet", "internet", "website", "email", "message", "app", "keyboard", "mouse", "screen", "charger", "battery", "wifi", "download", "upload", "software", "hardware", "update", "install", "delete", "backup", "innovation", "artificial intelligence", "virtual reality", "cybersecurity", "robot", "automation", "drone", "smartphone", "laptop", "desktop", "server", "cloud", "database", "network", "algorithm", "encryption", "firewall", "virus", "malware", "hacker", "coding", "programming", "developer", "engineer", "technician", "specialist", "expert", "guru", "ninja", "wizard", "master", "novice", "beginner", "intermediate", "advanced", "expert", "professional", "amateur", "enthusiast", "hobbyist", "tinkerer", "maker", "creator", "innovator", "inventor", "pioneer", "trailblazer", "visionary", "futurist"]
            elif topic == "education":
                base_words = ["school", "teacher", "student", "class", "lesson", "homework", "book", "pen", "pencil", "paper", "university", "college", "professor", "lecture", "seminar", "degree", "exam", "test", "scholarship", "tuition", "curriculum", "assignment", "presentation", "research", "pedagogy", "didactics", "methodology", "dissertation", "thesis", "essay", "report", "study", "learn", "teach", "educate", "instruct", "train", "tutor", "mentor", "coach", "principal", "dean", "chancellor", "faculty", "staff", "campus", "dormitory", "library", "laboratory", "classroom", "lecture hall", "auditorium", "amphitheater", "study hall", "common room", "cafeteria", "canteen", "quad", "courtyard", "green", "field", "court", "gymnasium", "pool", "track", "stadium"]
            elif topic == "work":
                base_words = ["job", "office", "boss", "colleague", "salary", "meeting", "break", "contract", "employee", "employer", "interview", "resume", "promotion", "retirement", "deadline", "task", "project", "teamwork", "leadership", "management", "entrepreneur", "startup", "investment", "dividend", "portfolio", "equity", "stocks", "bonds", "shares", "dividend", "interest", "loan", "credit", "debt", "mortgage", "lease", "rent", "invoice", "receipt", "expense", "income", "profit", "loss", "revenue", "budget", "finance", "accounting", "audit", "tax", "insurance", "pension", "benefits", "compensation", "pay", "wage", "salary", "bonus", "commission", "tip", "gratuity", "per diem", "allowance", "stipend", "grant", "fellowship", "award", "prize", "reward", "incentive", "motivation", "recognition", "appreciation", "acknowledgment", "praise", "commendation", "accolade", "honor", "distinction", "recognition"]
            elif topic == "health":
                base_words = ["doctor", "hospital", "medicine", "pill", "nurse", "patient", "health", "healthy", "sick", "ill", "pain", "fever", "cold", "flu", "cough", "headache", "stomachache", "backache", "toothache", "symptom", "treatment", "cure", "vaccine", "vaccination", "immunization", "virus", "bacteria", "infection", "disease", "illness", "condition", "disorder", "syndrome", "allergy", "asthma", "diabetes", "cancer", "heart attack", "stroke", "surgery", "operation", "therapy", "rehabilitation", "physical therapy", "mental health", "depression", "anxiety", "stress", "wellness", "fitness", "exercise", "diet", "nutrition", "vitamin", "mineral", "supplement", "herbal", "natural", "organic", "holistic", "alternative", "complementary", "integrative", "functional", "preventive", "curative", "palliative", "hospice", "end-of-life", "terminal", "chronic", "acute", "severe", "mild", "moderate", "serious", "critical", "life-threatening", "fatal", "deadly", "lethal", "dangerous", "risky", "hazardous", "unsafe", "safe", "effective", "ineffective", "efficient", "inefficient", "beneficial", "harmful", "helpful", "useless", "valuable", "worthless"]
            elif topic == "sports":
                base_words = ["football", "soccer", "basketball", "baseball", "tennis", "golf", "swimming", "running", "jogging", "walking", "hiking", "cycling", "skiing", "snowboarding", "skating", "ice skating", "roller skating", "skateboarding", "surfing", "windsurfing", "kitesurfing", "paddleboarding", "kayaking", "canoeing", "rowing", "sailing", "yachting", "boating", "fishing", "hunting", "shooting", "archery", "boxing", "wrestling", "martial arts", "karate", "judo", "taekwondo", "kung fu", "aikido", "jiu jitsu", "muay thai", "kickboxing", "mixed martial arts", "mma", "ufc", "bjj", "capoeira", "krav maga", "fencing", "sword fighting", "dueling", "combat", "fighting", "battle", "war", "conflict", "contest", "competition", "match", "game", "tournament", "championship", "league", "cup", "trophy", "medal", "prize", "award", "honor", "glory", "victory", "defeat", "win", "loss", "tie", "draw", "score", "point", "goal", "run", "hit", "shot", "pass", "throw", "catch", "kick", "punch", "block", "tackle", "save", "dive", "jump", "leap", "spring", "vault", "hurdle", "clear", "land", "fall", "crash", "collide", "hit", "strike", "beat", "defeat", "conquer", "triumph", "prevail", "win", "succeed", "achieve", "accomplish", "attain", "reach", "earn", "gain", "obtain", "secure", "capture", "seize", "grab", "take", "get", "acquire", "procure", "obtain"]
            else:
                # Для остальных тем используем общие слова
                common_words = ["example", "sample", "test", "word", "basic", "simple", "common", "everyday", "regular", "normal", "usual", "typical", "standard", "ordinary", "familiar", "known", "popular", "famous", "important", "necessary", "essential", "vital", "crucial", "critical", "key", "main", "primary", "major", "minor", "various", "different", "similar", "same", "opposite", "positive", "negative", "possible", "impossible", "probable", "certain", "sure", "clear", "obvious", "evident", "apparent", "visible", "invisible", "audible", "inaudible", "tangible", "intangible", "palpable", "imperceptible", "noticeable", "unnoticeable", "remarkable", "unremarkable", "extraordinary", "ordinary", "exceptional", "unexceptional", "outstanding", "mediocre", "excellent", "poor", "good", "bad", "better", "worse", "best", "worst", "superior", "inferior", "perfect", "imperfect", "ideal", "real", "actual", "genuine", "authentic", "fake", "false", "bogus", "counterfeit", "forged", "fraudulent", "deceptive", "misleading", "dishonest", "untruthful", "truthful", "honest", "sincere", "genuine", "authentic", "real", "true", "accurate", "precise", "exact", "correct", "right", "proper", "appropriate", "suitable", "fitting", "apt", "relevant", "pertinent", "applicable", "germane", "material", "significant", "important", "consequential", "momentous", "weighty", "grave", "serious", "severe", "acute", "intense", "extreme", "utmost", "supreme", "paramount", "preeminent", "dominant", "predominant", "principal", "chief", "main", "major", "primary", "leading", "foremost", "first", "prime", "key", "central", "focal", "core", "fundamental", "basic", "essential", "necessary", "indispensable", "requisite", "vital", "crucial", "critical", "imperative", "mandatory", "compulsory", "obligatory", "required", "necessary", "essential", "important", "significant", "meaningful", "purposeful", "useful", "helpful", "beneficial", "advantageous", "favorable", "good", "positive", "constructive", "productive", "fruitful", "profitable", "rewarding", "satisfying", "fulfilling", "gratifying", "pleasing", "enjoyable", "pleasant", "nice", "fine", "excellent", "great", "superb", "terrific", "fantastic", "wonderful", "marvelous", "splendid", "magnificent", "glorious", "brilliant", "outstanding", "exceptional", "remarkable", "extraordinary", "incredible", "unbelievable", "amazing", "astonishing", "astounding", "stunning", "breathtaking", "awesome", "impressive", "notable", "noteworthy", "memorable", "unforgettable", "lasting", "enduring", "permanent", "eternal", "everlasting", "infinite", "limitless", "boundless", "unlimited", "unrestricted", "unconstrained", "free", "liberated", "emancipated", "independent", "autonomous", "self-governing", "self-ruling", "sovereign", "autocratic", "dictatorial", "tyrannical", "oppressive", "repressive", "authoritarian", "totalitarian", "fascist", "nazi", "communist", "socialist", "democratic", "republican", "liberal", "conservative", "progressive", "reactionary", "radical", "extremist", "moderate", "centrist", "left-wing", "right-wing", "far-left", "far-right", "ultra-left", "ultra-right"]
                base_words = common_words
            
            # Добавляем уникальные слова без повторов
            unique_words = []
            for word in base_words:
                if word not in unique_words:
                    unique_words.append(word)
            
            # Дублируем с вариациями, если нужно достичь 500
            WORD_BASE[topic][level] = [{"word": w} for w in unique_words]
            
            # Если меньше 500, добавляем слова с суффиксами/префиксами
            counter = 1
            while len(WORD_BASE[topic][level]) < 500:
                for word in unique_words:
                    if len(WORD_BASE[topic][level]) >= 500:
                        break
                    WORD_BASE[topic][level].append({"word": f"{word}_{counter}"})
                counter += 1

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
def highlight_mistake(user_word, correct_word):
    """Сравнивает написанное пользователем слово с правильным и выделяет ошибки"""
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
• Ты пишешь это слово на английском  
• Я проверяю правописание и указываю на ошибки  
• Если не знаешь слово — нажми «❓ Не знаю»

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
    bot.send_message(message.chat.id, "📝 Напиши это слово по-английски:", reply_markup=markup)

# ========== КНОПКА «НЕ ЗНАЮ» ==========
@bot.message_handler(func=lambda message: message.text == "❓ Не знаю")
def dont_know(message):
    user_id = message.from_user.id
    word_data = user_data[user_id].get("current_word")
    
    if word_data:
        bot.send_message(
            message.chat.id,
            f"🔍 Это слово: *{word_data['word']}*",
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
    
    user_word = message.text.strip()
    correct_word = word_data["word"]
    
    diff, is_correct = highlight_mistake(user_word, correct_word)
    
    if is_correct:
        response = f"✅ *Верно!*\n\nСлово: {correct_word}"
    else:
        response = f"❌ *Ошибка*\n\nТы написала: {user_word}\nПравильно: {correct_word}\n"
        if diff:
            response += "\n*Где ошибка:*\n" + "\n".join(diff)
    
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
        bot.send_message(message.chat.id, "📝 Напиши это слово по-английски:", reply_markup=markup)

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
    total_words = 0
    for topic in WORD_BASE:
        for level in WORD_BASE[topic]:
            total_words += len(WORD_BASE[topic][level])
    print(f"Всего уникальных слов в базе: {total_words}")
    bot.polling(none_stop=True)