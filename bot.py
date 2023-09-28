import telebot
import requests
from io import BytesIO
import random 
import os
import json


bot = telebot.TeleBot('6446274916:AAGjcIyG4reB5fd8ANk_vorVb8xbUKo4C8w')

def generate_image(chat_id):
    # URL для получения данных о дереве файлов и папок на GitHub
    github_tree_url = 'https://api.github.com/repos/theborzet/projects_for_university/git/trees/master?recursive=1'

    # Отправляем GET-запрос к GitHub API
    response = requests.get(github_tree_url)
    if response.status_code == 200:
        data = response.json()
        print(data)

        if "tree" in data:
            tree = data["tree"]
            image_files = [item["path"] for item in tree if item["type"] == "blob" and item["path"].startswith("images/")]

            if image_files:
                random_image_path = random.choice(image_files)
                github_image_url = f'https://raw.githubusercontent.com/theborzet/projects_for_university/master/{random_image_path}'
                image_data = requests.get(github_image_url).content
                bot.send_photo(chat_id, image_data)
                send_keyboard(chat_id)
            else:
                bot.send_message(chat_id, 'На GitHub нет изображений в папке "images".')
        else:
            bot.send_message(chat_id, 'Не удалось получить данные о дереве файлов с GitHub.')
    else:
        bot.send_message(chat_id, 'Ошибка при запросе к GitHub API.')
def generate_audio(chat_id):
    # URL для получения данных о дереве файлов и папок на GitHub
    github_tree_url = 'https://api.github.com/repos/theborzet/projects_for_university/git/trees/master?recursive=1'

    # Отправляем GET-запрос к GitHub API
    response = requests.get(github_tree_url)
    if response.status_code == 200:
        data = response.json()

        if "tree" in data:
            tree = data["tree"]
            audio_files = [item["path"] for item in tree if item["type"] == "blob" and item["path"].startswith("audio/")]

            if audio_files:
                random_audio_path = random.choice(audio_files)
                github_audio_url = f'https://raw.githubusercontent.com/theborzet/projects_for_university/master/{random_audio_path}'
                audio_data = requests.get(github_audio_url).content
                bot.send_audio(chat_id, audio_data)
                send_keyboard(chat_id)
            else:
                bot.send_message(chat_id, 'На GitHub нет аудиофайлов в папке "audio".')
        else:
            bot.send_message(chat_id, 'Не удалось получить данные о дереве файлов с GitHub.')
    else:
        bot.send_message(chat_id, 'Ошибка при запросе к GitHub API.')
def send_keyboard(chat_id):
    user_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button1 = telebot.types.KeyboardButton("Сгенерировать картинку")
    button2 = telebot.types.KeyboardButton("Сгенерировать аудиофайл")
    user_markup.row(button1, button2)
    
    bot.send_message(chat_id, 'Что бы вы хотели сделать?', reply_markup=user_markup)


def main():
    @bot.message_handler(commands=['start'])
    def start(message):
        user_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button1 = telebot.types.KeyboardButton("Сгенерировать картинку")
        button2 = telebot.types.KeyboardButton("Сгенерировать аудиофайл")
        user_markup.row(button1, button2)

        bot.send_message(message.chat.id, 'Привет! Я бот. Как я могу вам помочь?', reply_markup=user_markup)

    @bot.message_handler(commands=['stop'])
    def stop(message):
        # Отправьте сообщение о завершении работы бота и остановите бота
        bot.send_message(message.chat.id, 'Бот остановлен.')
        bot.stop_polling()


    @bot.message_handler(func=lambda message: message.text == "Сгенерировать картинку")
    def button1_handler(message):
        generate_image(message.chat.id)
        

    @bot.message_handler(func=lambda message: message.text == "Сгенерировать аудиофайл")
    def button2_handler(message):
        generate_audio(message.chat.id)
    @bot.message_handler(func=lambda message: message.text.lower() == "вестяк")
    def handle_command1(message):
        with open(os.path.join('images', 'vestyak.jpg'), 'rb') as image_file:
            bot.send_photo(message.chat.id, image_file)
        send_keyboard(message.chat.id)
    @bot.message_handler(func=lambda message: "ссылка" in message.text.lower() or "ссылку" in message.text.lower())
    def send_github_link(message):
        chat_id = message.chat.id
        github_link = "https://github.com/theborzet/projects_for_university#projects_for_university" 
        bot.send_message(chat_id, f"Вот ссылка на GitHub репозиторий: {github_link}")

        
    bot.polling(none_stop=True)
if __name__ == '__main__': 
    main()