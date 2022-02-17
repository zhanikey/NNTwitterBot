import json
import requests
import telebot
from PIL import Image, ImageDraw, ImageFont, ImageOps
import resnext

config = json.load(open("config.json", "rb"))
token = config['token']
download_to = config['download_to']
bot = telebot.TeleBot(token)

def meme_guess(file):
    image = Image.open(file)
    width = image.size[0]
    height = image.size[1]
    font = ImageFont.truetype("botresources/Lobster-Regular.ttf", int(width/12)) # int(width/10)
    x = int(width / 2 - width / 3.5)
    y = height - int(width/7 * 1.328147)
    predicted_text = resnext.resnext_classify('submissions/temp.jpg')
    predicted_text = ', '.join(predicted_text[0])
    predicted_text = predicted_text.split(',')[0]
    tool = ImageDraw.Draw(image)
    w, h = tool.textsize(predicted_text, font)
    tool.text(((width-w)/2,(height-h)-40), predicted_text, (255, 255, 255), font=font)
    image.save(f'{download_to}/output.jpg', 'JPEG', quality=100)

download = 'https://api.telegram.org/file/bot' + token + '/'


@bot.message_handler(content_types=["photo"])
def meme(message):
    photo = message.photo[-1].file_id
    path = bot.get_file(file_id=photo).file_path
    with open(f'{download_to}/temp.jpg', 'wb') as file:
        r = requests.get(download + path)
        for chunk in r:
            file.write(chunk)
    meme_guess(f'{download_to}/temp.jpg')
    f = open(f'{download_to}/output.jpg', 'rb')
    bot.send_photo(message.chat.id, f, None)


if __name__ == '__main__':
    bot.polling(none_stop=True)