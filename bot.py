import telebot
import requests
from io import BytesIO
import random 


bot = telebot.TeleBot('6446274916:AAGjcIyG4reB5fd8ANk_vorVb8xbUKo4C8w')

def get_value(chat_id, value):
    github_tree_url = 'https://api.github.com/repos/theborzet/projects_for_university/git/trees/master?recursive=1'

    # Отправляем GET-запрос к GitHub API
    response = requests.get(github_tree_url)
    if response.status_code == 200:
        data = response.json()

        if "tree" in data:
            tree = data["tree"]
            value_files = [item["path"] for item in tree if item["type"] == "blob" and item["path"].startswith(f"{value}/")]

            if value_files:
                random_value_path = random.choice(value_files)
                github_value_url = f'https://raw.githubusercontent.com/theborzet/projects_for_university/master/{random_value_path}'
                value_data = requests.get(github_value_url).content
                if value.startswith("images"):
                    bot.send_photo(chat_id, value_data)
                elif value.startswith("audio"):
                    bot.send_audio(chat_id, value_data)
                send_keyboard(chat_id)
            else:
                bot.send_message(chat_id, f'На GitHub нет изображений в папке "{value}".')
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
        get_value(message.chat.id, 'images')
        

    @bot.message_handler(func=lambda message: message.text == "Сгенерировать аудиофайл")
    def button2_handler(message):
        get_value(message.chat.id, 'audio')

    @bot.message_handler(func=lambda message: message.text.lower() == "вестяк")
    def handle_command1(message):
        vest_url = 'https://raw.githubusercontent.com/theborzet/projects_for_university/master/images/vestyak.jpg'
        value_data = requests.get(vest_url).content
        # Отправляем изображение в Telegram
        bot.send_photo(message.chat.id, value_data)
        send_keyboard(message.chat.id)

    @bot.message_handler(func=lambda message: "ссылка" in message.text.lower() or "ссылку" in message.text.lower())
    def send_github_link(message):
        chat_id = message.chat.id
        github_link = "https://github.com/theborzet/projects_for_university#projects_for_university" 
        bot.send_message(chat_id, f"Вот ссылка на GitHub репозиторий: {github_link}")

        
    bot.polling(none_stop=True)
if __name__ == '__main__': 
    main()

