from config import TOKEN
from main import reve_api
import telebot

bot = telebot.TeleBot(TOKEN)
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Приветсвую вас в телеграмм боте по генерации изображений с помощью REVE API!" \
    "Какую картинку вы хотите создать?")

@bot.message_handler(func=lambda message: True)
def handle(message):
    prompt = message.text
    image_path = f"generated_{message.from_user.id}.png"
    result = reve_api.generate_reve_image(
        prompt=prompt,
        save_json=None,
        save_image=image_path
    )
    if result.get("content_violation"):
        bot.send_message(message.chat.id, "Извините, но ваш запрос нарушает политику контента.")
        return
    with open(image_path, "rb") as img_file:
        bot.send_photo(message.chat.id, img_file)

bot.polling()