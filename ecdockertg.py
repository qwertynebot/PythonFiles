import telebot
import docker
import boto3
import subprocess

bot = telebot.TeleBot("")

region_name = 'eu-north-1'
aws_access_key = ''
aws_secret_key = ''
docker_client = docker.from_env()

region_name = 'us-north-1'  
ec2 = boto3.resource('ec2', region_name=region_name, aws_access_key_id=aws_access_key , aws_secret_access_key=aws_secret_key)

@bot.message_handler(commands=['start'])
def handle_start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    create_ec2_button = telebot.types.KeyboardButton('Створити EC2')
    create_docker_button = telebot.types.KeyboardButton('Створити Docker контейнер')
    start_docker_button = telebot.types.KeyboardButton('Запустити Docker контейнер')
    stop_docker_button = telebot.types.KeyboardButton('Зупинити Docker контейнер')
    remove_docker_button = telebot.types.KeyboardButton('Видалити Docker контейнер')
    markup.row(create_ec2_button, create_docker_button)
    markup.row(start_docker_button, stop_docker_button)
    markup.row(remove_docker_button)
    bot.send_message(message.chat.id, "Виберіть операцію:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Створити EC2')
def create_ec2_instance(message):
    try:
        user_data_script = '''#!/bin/bash
                                sudo apt-get update -y
                                sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
                                curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
                                sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
                                sudo apt-get update -y
                                sudo apt-get install -y docker-ce
                                sudo usermod -aG docker $USER

                            '''
        instance = ec2.create_instances(
            ImageId='ami-0989fb15ce71ba39e',     
            MinCount=1,
            MaxCount=1,
            InstanceType='t3.micro',
            KeyName='Kluc',
            SecurityGroups=['New security group '], 
            UserData=user_data_script,
        )
        bot.send_message(message.chat.id, f"EC2 інстанс створено з ID: {instance[0].id}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Помилка при створенні EC2: {str(e)}")

@bot.message_handler(func=lambda message: message.text == 'Створити Docker контейнер')
def create_docker_container(message):
    bot.send_message(message.chat.id, "Введіть ім'я образу та ім'я контейнера, наприклад: ubuntu my-container")
    bot.register_next_step_handler(message, create_docker_container_step)

def create_docker_container_step(message):
    try:
        image_name, container_name = message.text.split()
        container = docker_client.containers.create(image=image_name, name=container_name)
        bot.send_message(message.chat.id, f"Контейнер {container_name} створено.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Помилка при створенні контейнера: {str(e)}")

@bot.message_handler(func=lambda message: message.text == 'Запустити Docker контейнер')
def start_docker_container(message):
    bot.send_message(message.chat.id, "Введіть ім'я контейнера, який потрібно запустити:")
    bot.register_next_step_handler(message, start_docker_container_step)

def start_docker_container_step(message):
    try:
        container_name = message.text
        container = docker_client.containers.get(container_name)
        container.start()
        bot.send_message(message.chat.id, f"Контейнер {container_name} запущено")
    except Exception as e:
        bot.send_message(message.chat.id, f"Помилка при запуску контейнера: {str(e)}")

@bot.message_handler(func=lambda message: message.text == 'Зупинити Docker контейнер')
def stop_docker_container(message):
    bot.send_message(message.chat.id, "Введіть ім'я контейнера, який потрібно зупинити:")
    bot.register_next_step_handler(message, stop_docker_container_step)

def stop_docker_container_step(message):
    try:
        container_name = message.text
        container = docker_client.containers.get(container_name)
        container.stop()
        bot.send_message(message.chat.id, f"Контейнер {container_name} зупинено")
    except Exception as e:
        bot.send_message(message.chat.id, f"Помилка при зупинці контейнера: {str(e)}")

@bot.message_handler(func=lambda message: message.text == 'Видалити Docker контейнер')
def remove_docker_container(message):
    bot.send_message(message.chat.id, "Введіть ім'я контейнера, який потрібно видалити:")
    bot.register_next_step_handler(message, remove_docker_container_step)

def remove_docker_container_step(message):
    try:
        container_name = message.text
        container = docker_client.containers.get(container_name)
        container.remove()
        bot.send_message(message.chat.id, f"Контейнер {container_name} видалено.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Помилка при видаленні контейнера: {str(e)}")


if __name__ == "__main__":
    bot.polling()
