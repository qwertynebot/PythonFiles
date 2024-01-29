import telebot
import subprocess

bot = telebot.TeleBot("")

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Вітаємо! Виберіть опцію для взаємодії з серверами:")
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item1 = telebot.types.KeyboardButton("Налаштувати сервер")
    item2 = telebot.types.KeyboardButton("Встановити Docker")
    markup.add(item1, item2)
    bot.send_message(message.chat.id, "Виберіть дію:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Налаштувати сервер")
def handle_configure_server(message):
    try:
        subprocess.run(['ansible-playbook', '-i', 'your_inventory_file', 'your_playbook.yml', '--extra-vars', 'ansible_ssh_user=your_ssh_user'])
        bot.send_message(message.chat.id, "Сервер налаштовано успішно!")
    except Exception as e:
        bot.send_message(message.chat.id, f"Помилка: {str(e)}")

@bot.message_handler(func=lambda message: message.text == "Встановити Docker")
def handle_install_docker(message):
    try:
        subprocess.run(['ansible-playbook', '-i', 'your_inventory_file', 'your_playbook.yml', '--extra-vars', 'ansible_ssh_user=your_ssh_user'])
        bot.send_message(message.chat.id, "Docker встановлено успішно!")
    except Exception as e:
        bot.send_message(message.chat.id, f"Помилка: {str(e)}")

bot.polling()
