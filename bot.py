import telebot
import random
import os
import requests
import time
import subprocess
import tempfile
import difflib
import speech_recognition as sr

# ТОКЕН СЮДА (вставь свой из BotFather)
TOKEN = "7636052400:AAEVH-BNqkSgpVbRUKibqG5j41cAxVStq9M"

bot = telebot.TeleBot(TOKEN)

# Хранилище данных пользователей
user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 
        "🎤 Тренажер произношения\n\n"
        "1. Отправь файл .txt со словами\n"
        "2. Напиши /word чтобы получить слово\n"
        "3. Отправь голосовое сообщение\n\n"
        "Начинаем! 👇",
        parse_mode='Markdown'
    )

@bot.message_handler(commands=['word'])
def get_word(message):
    user_id = message.from_user.id
    
    if user_id not in user_data or 'words' not in user_data[user_id]:
        bot.reply_to(message, "Сначала отправь файл со словами!")
        return
    
    word = random.choice(user_data[user_id]['words'])
    user_data[user_id]['current_word'] = word
    
    bot.reply_to(message, f"📢 Твое слово: {word}\n\nГовори!", parse_mode='Markdown')

@bot.message_handler(content_types=['document'])
def handle_file(message):
    try:
        user_id = message.from_user.id
        
        # Скачиваем файл
        file_info = bot.get_file(message.document.file_id)
        file = requests.get(f'https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}')
        
        # Читаем слова
        content = file.text
        words = [line.strip() for line in content.split('\n') if line.strip()]
        
        if user_id not in user_data:
            user_data[user_id] = {}
        
        user_data[user_id]['words'] = words
        
        bot.reply_to(message, 
            f"✅ Файл получен! Загружено слов: {len(words)}\n"
            f"Примеры: {', '.join(words[:5])}\n\n"
            f"Теперь напиши /word",
            parse_mode='Markdown'
        )
        
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    user_id = message.from_user.id
    
    if user_id not in user_data or 'current_word' not in user_data[user_id]:
        bot.reply_to(message, "Сначала получи слово через /word!")
        return
    
    try:
        status_msg = bot.reply_to(message, "🎧 Обрабатываю...")
        
        # Скачиваем голосовое
        file_info = bot.get_file(message.voice.file_id)
        voice_file = requests.get(f'https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}')
        
        # Сохраняем
        with tempfile.NamedTemporaryFile(suffix='.ogg', delete=False) as f:
            f.write(voice_file.content)
            ogg_path = f.name
        
        # Конвертируем в wav
        wav_path = ogg_path.replace('.ogg', '.wav')
        cmd = ['ffmpeg', '-i', ogg_path, '-ar', '16000', '-ac', '1', wav_path, '-y']
        subprocess.run(cmd, capture_output=True)
        
        # Распознаем речь
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio = recognizer.record(source)
        
        try:
            spoken_text = recognizer.recognize_google(audio, language='ru-RU')
        except:
            spoken_text = None
        
        expected = user_data[user_id]['current_word']
        
        # Проверяем
        if spoken_text and spoken_text.lower() == expected.lower():
            result = f"✅ Правильно!\n\nТы сказал: _{spoken_text}_"
        elif spoken_text:
            result = f"❌ Ошибка\n\nТы сказал: _{spoken_text}_\nНужно: _{expected}_"
        else:
            result = "❌ Не удалось распознать речь. Попробуй еще раз."
        
        # Удаляем файлы
        os.unlink(ogg_path)
        os.unlink(wav_path)
        
        bot.edit_message_text(result, chat_id=message.chat.id, message_id=status_msg.message_id, parse_mode='Markdown')
        
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling(none_stop=True)