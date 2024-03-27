import requests
import json
import os
import math
from instagrapi import Client
from instagrapi.exceptions import ClientError, PhotoNotUpload
import telebot
from datetime import date, timezone, timedelta, datetime

# Define função para postagem no Instagram
def post_instagram_photo():
    try:
        # Realiza login na conta do Instagram
        cl = Client(request_timeout=7)
        cl.login(USERNAME, PASSWORD)
        print('Logado no Instagram')
    except ClientError as e:
        print(f"Erro durante o login: {e}")
        bot.send_message(tele_user, 'boturinsta com problema')
        return

    # Obtém URL de uma imagem de cachorro
    url = "https://api.thedogapi.com/v1/images/search?format=json&type=jpeg"
    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': DOG_KEY
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    todos = json.loads(response.text)
    site = todos[0].get('url')
    r = requests.get(site, allow_redirects=True)
    open('dog.jpeg', 'wb').write(r.content)

    # Gera legenda para a foto do Instagram
    data = date.today().strftime("%d/%m")
    insta_string = f"""Dog do dia {data}

#DogOfTheDay #CachorroDoDia"""

    # Tenta fazer o upload da foto para o Instagram
    try:
        cl.photo_upload('dog.jpeg', insta_string)
        print("Foto publicada no Instagram")
    except PhotoNotUpload as e:
        print(f"Erro durante o upload da foto: {e}")
        if "login_required" in str(e):
            print("Login é necessário. Verifique suas credenciais.")
            bot.send_message(tele_user, 'boturinsta com problema - login necessário')
        else:
            print("Erro desconhecido durante o upload da foto.")
            bot.send_message(tele_user, 'boturinsta com problema - erro desconhecido')

# Variáveis de ambiente
DOG_KEY = os.environ.get("DOG_KEY")
USERNAME = os.environ.get("USUARIO")
PASSWORD = os.environ.get("SENHA")
tele_user = os.environ.get("TELE_USER")
TOKEN = os.environ["TELEGRAM_TOKEN"]
bot = telebot.TeleBot(TOKEN)

# Executa a função de postagem no Instagram
post_instagram_photo()
