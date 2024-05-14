import requests
import json
import os
import sys
import math
from instagrapi import Client
from instagrapi.exceptions import ClientError, PhotoNotUpload
import telebot
from datetime import date, timezone, timedelta, datetime
from PIL import Image
import google.generativeai as genai


# Inicializando api do Gemini
GOOGLE_API_KEY=os.environ["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro-vision')

def gemini_image(prompt, image_path):
    # Carregando a imagem
    imagem = Image.open(image_path)

    # Gerando conteúdo com base na imagem e no prompt
    response = model.generate_content([prompt, imagem], stream=True)

    # Aguarda a conclusão da iteração antes de acessar os candidatos
    response.resolve()

    # Verificando a resposta
    if response.candidates and len(response.candidates) > 0:
        if response.candidates[0].content.parts and len(response.candidates[0].content.parts) > 0:
            return response.candidates[0].content.parts[0].text
        else:
            print("Nenhuma parte de conteúdo encontrada na resposta.")
    else:
        print("Nenhum candidato válido encontrado.")

# Define função para postagem no Instagram
def post_instagram_photo():
    try:
        # Realiza login na conta do Instagram
        cl = Client(request_timeout=7)
        cl.login(USERNAME, PASSWORD)
        print('Logado no Instagram')
    except:
        print("deslodog")
        bot.send_message(tele_user, 'doglufi com problema pra logar')
        sys.exit()

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
    response_gemini = gemini_image("Escreva uma legenda engraçada e/ou fofa sobre essa imagem de cachorro para postar no Instagram com hashtags","dog.jpeg")
    if response_gemini == None:
        response_gemini = "#DogOfTheDay #CachorroDoDia"
    else:
        pass
    insta_string = f"""Dog do dia {data}
{response_gemini}"""

    # Tenta fazer o upload da foto para o Instagram
    try:
        cl.photo_upload('dog.jpeg', insta_string)
        print("Foto publicada no Instagram")
    except PhotoNotUpload as e:
        print(f"Erro durante o upload da foto: {e}")
        if "login_required" in str(e):
            print("Login é necessário. Verifique suas credenciais.")
            bot.send_message(tele_user, 'doglufi com problema pra postar')
        else:
            print("Erro desconhecido durante o upload da foto.")
            bot.send_message(tele_user, 'doglufi com problema pra postar')

# Variáveis de ambiente
DOG_KEY = os.environ.get("DOG_KEY")
USERNAME = os.environ.get("USUARIO")
PASSWORD = os.environ.get("SENHA")
tele_user = os.environ.get("TELE_USER")
TOKEN = os.environ["TELEGRAM_TOKEN"]
bot = telebot.TeleBot(TOKEN)

# Executa a função de postagem no Instagram
post_instagram_photo()
