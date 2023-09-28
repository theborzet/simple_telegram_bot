import telebot
import requests
from io import BytesIO
import random 
import os

bot = telebot.TeleBot('6446274916:AAGjcIyG4reB5fd8ANk_vorVb8xbUKo4C8w')

def generate_image(chat_id):
    # Путь к папке с изображениями
    image_folder = 'images'
    
    image_files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]

    if image_files:
        random_image = random.choice(image_files)

        with open(os.path.join(image_folder, random_image), 'rb') as image_file:
            bot.send_photo(chat_id, image_file)
        send_keyboard(chat_id)
    else:
        bot.send_message(chat_id, 'В папке нет изображений.')
def generate_audio(chat_id):
    audio_folder = 'audio'
    
    audio_files = [f for f in os.listdir(audio_folder) if os.path.isfile(os.path.join(audio_folder, f))]

    if audio_files:
        random_audio = random.choice(audio_files)
        
        with open(os.path.join(audio_folder, random_audio), 'rb') as audio_file:
            bot.send_audio(chat_id, audio_file)
        
        send_keyboard(chat_id)
    else:
        bot.send_message(chat_id, 'В папке нет аудиофайлов.')
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


    @bot.message_handler(func=lambda message: message.text == "Сгенерировать картинку")
    def button1_handler(message):
        generate_image(message.chat.id)
        

    # Обработчик нажатия на кнопку "Кнопка 2"
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