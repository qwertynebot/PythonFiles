import telebot
import docker

bot = telebot.TeleBot("")
client = docker.from_env()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    create_button = telebot.types.KeyboardButton('/create')
    start_button = telebot.types.KeyboardButton('/start')
    stop_button = telebot.types.KeyboardButton('/stop')
    remove_button = telebot.types.KeyboardButton('/remove')

    markup.add(create_button, start_button, stop_button, remove_button)
    bot.send_message(message.chat.id, "Виберіть операцію:", reply_markup=markup)

@bot.message_handler(commands=['create'])
def create_container(message):
    bot.send_message(message.chat.id, "Введіть ім'я образу та ім'я контейнера , наприклад: ubuntu my-container")
    bot.register_next_step_handler(message, create_container_step)

def create_container_step(message):
    try:
        image_name, container_name = message.text.split()
        container = client.containers.create(image=image_name, name=container_name)
        bot.send_message(message.chat.id, f"Контейнер {container_name} створено.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Помилка: {str(e)}")

@bot.message_handler(commands=['start'])
def start_container(message):
    bot.send_message(message.chat.id, "Контейнер який потрібно запустити:")
    bot.register_next_step_handler(message, start_container_step)

def start_container_step(message):
    try:
        container_name = message.text
        container = client.containers.get(container_name)
        container.start()
        bot.send_message(message.chat.id, f"Контейнер {container_name} запущено")
    except Exception as e:
        bot.send_message(message.chat.id, f"Помилка: {str(e)}")

@bot.message_handler(commands=['stop'])
def stop_container(message):
    bot.send_message(message.chat.id, "Контейнер, який потрібно зупинити:")
    bot.register_next_step_handler(message, stop_container_step)

def stop_container_step(message):
    try:
        container_name = message.text
        container = client.containers.get(container_name)
        container.stop()
        bot.send_message(message.chat.id, f"Контейнер {container_name} зупинено")
    except Exception as e:
        bot.send_message(message.chat.id, f"Помилка: {str(e)}")

@bot.message_handler(commands=['remove'])
def remove_container(message):
    bot.send_message(message.chat.id, "Контейнер який потрібно видалити:")
    bot.register_next_step_handler(message, remove_container_step)

def remove_container_step(message):
    try:
        container_name = message.text
        container = client.containers.get(container_name)
        container.remove()
        bot.send_message(message.chat.id, f"Контейнер {container_name} видалено.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Помилка: {str(e)}")

bot.polling()


