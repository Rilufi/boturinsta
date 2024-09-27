import requests
import json
import os
import sys
import time
from instagrapi import Client
from instagrapi.exceptions import ClientError
import telebot
from datetime import date, timezone, timedelta, datetime
from PIL import Image
import google.generativeai as genai


# Inicializando api do Gemini
GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')

def gemini_image(prompt, image_path, max_retries=6):
    imagem = Image.open(image_path)

    if imagem.mode == 'P':
        imagem = imagem.convert('RGB')

    retries = 1
    while retries < max_retries:
        try:
            response = model.generate_content([prompt, imagem], stream=True)
            response.resolve()
            
            if response.candidates and len(response.candidates) > 0:
                if response.candidates[0].content.parts and len(response.candidates[0].content.parts) > 0:
                    return response.candidates[0].content.parts[0].text
                else:
                    print("Nenhuma parte de conteúdo encontrada na resposta.")
            else:
                print("Nenhum candidato válido encontrado.")
            break  # Saia do loop se tudo correr bem

        except ServiceUnavailable as e:
            print(f"Erro: {e}. Tentando novamente em {5 ** retries} segundos...")
            time.sleep(5 ** retries)  # Backoff exponencial
            retries += 1

    print("Falha ao gerar conteúdo após várias tentativas.")
    return None

fuso_horario = timezone(timedelta(hours=-3))
data_e_hora_atuais = datetime.now()
data_e_hora_sao_paulo = data_e_hora_atuais.astimezone(fuso_horario)
hora = data_e_hora_sao_paulo.strftime('%H')

today = date.today()
data = today.strftime("%d/%m")

cat_key = os.environ.get("CAT_KEY")
username = os.environ.get("USERNAME")
password = os.environ.get("PASSWORD")
tele_user = os.environ.get("TELE_USER")
token = os.environ["TELEGRAM_TOKEN"]
bot = telebot.TeleBot(token)


# Função para logar no Instagram com sessão
def logar_instagram():
    cl = Client()
    session_file = 'instacat_session.json'
    try:
        if os.path.exists(session_file):
            cl.load_settings(session_file)
        cl.login(username, password)
        cl.get_timeline_feed()
        cl.dump_settings(session_file)
    except Exception as e:
        print(f"Erro ao logar no Instagram: {e}")
        bot.send_message(tele_user, f"boturinsta erro ao logar no Instagram: {e}")
        sys.exit()
    return cl

try:
    instagram_client = logar_instagram()
except Exception as e:
    print(f"Erro ao logar no Instagram: {e}")
    bot.send_message(tele_user, f"boturinsta erro ao logar no Instagram: {e}")

url = "https://api.thecatapi.com/v1/images/search?format=json&type=jpeg"
payload = {}
headers = {
    'Content-Type': 'application/json',
    'x-api-key': cat_key
}
proxies = {
    'http': 'http://10.10.1.10:3128',
}

response = requests.request("GET", url, headers=headers, data=payload, proxies=proxies)
todos = json.loads(response.text)
site = todos[0].get('url')
r = requests.get(site, allow_redirects=True)
open('gato.jpeg', 'wb').write(r.content)

# Função para postar foto no Instagram
def post_instagram_photo(cl, image_path, caption):
    try:
        cl.photo_upload(image_path, caption)
        print("Foto publicada no Instagram")
    except Exception as e:
        print(f"Erro ao postar foto no Instagram: {e}")
        bot.send_message(tele_user, f"boturinsta com problema pra postar: {e}")

response = requests.request("GET", url, headers=headers, data=payload, proxies=proxies)
todos = json.loads(response.text)
site = todos[0].get('url')
r = requests.get(site, allow_redirects=True)
open('gato.jpeg', 'wb').write(r.content)
response_gemini = gemini_image("Escreva uma legenda em português do Brasil engraçada e/ou fofa sobre essa imagem de gato para postar no Instagram com hashtags", "gato.jpeg")
if response_gemini == None:
    response_gemini = "#CatOfTheDay #GatoDoDia"
elif response_gemini == '"':
    response_gemini = "#CatOfTheDay #GatoDoDia"
else:
    pass
insta_string = f""" Gato do dia {data}
{response_gemini}"""
# Post the image on Instagram
if instagram_client:
    try:
        post_instagram_photo(instagram_client, 'gato.jpeg', insta_string)
    except Exception as e:
        print(f"Erro ao postar foto no Instagram: {e}")
        bot.send_message(tele_user, 'boturinsta com problema pra postar imagem')
