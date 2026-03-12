ogg_file.write(voice_content)
            ogg_path = ogg_file.name
        
        # Конвертируем OGG в WAV через ffmpeg
        wav_path = ogg_path.replace('.ogg', '.wav')
        ffmpeg_cmd = ['ffmpeg', '-i', ogg_path, '-ar', '16000', '-ac', '1', wav_path, '-y']
        subprocess.run(ffmpeg_cmd, capture_output=True)
        
        # Распознаем речь через Google Speech Recognition
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
        
        try:
            spoken_text = recognizer.recognize_google(audio_data, language='ru-RU')
        except sr.UnknownValueError:
            spoken_text = None
        except sr.RequestError:
            spoken_text = None
        
        # Получаем ожидаемое слово
        expected_word = user_data[user_id]['current_word']
        
        # Сравниваем результат
        if spoken_text and spoken_text.lower() == expected_word.lower():
            result = f"✅ *Правильно!*\n\nТы сказал: _{spoken_text}_"
        elif spoken_text:
            result = f"❌ *Ошибка*\n\nТы сказал: _{spoken_text}_\nНужно: *{expected_word}*"
        else:
            result = "❌ *Не удалось распознать речь*\n\nПопробуй произнести четче или проверь микрофон."
        
        # Удаляем временные файлы
        os.unlink(ogg_path)
        os.unlink(wav_path)
        
        # Отправляем результат
        bot.edit_message_text(result, 
                            chat_id=message.chat.id, 
                            message_id=status_msg.message_id,
                            parse_mode='Markdown')
        
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка при обработке голосового: {e}")

# Запуск бота
if name == 'main':
    print("✅ Бот запущен и готов к работе!")
    print("📱 Найди бота в Telegram: @твой_юзернейм_бота")
    print("🔄 Нажми /start для начала работы")
    bot.polling(none_stop=True)