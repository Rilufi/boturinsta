import requests
import json
import os
import sys
import math
from instagrapi import Client
from instagrapi.exceptions import ClientError
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

    # Convertendo a imagem para o modo 'RGB' caso esteja em modo 'P'
    if imagem.mode == 'P':
        imagem = imagem.convert('RGB')

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

#get the time with timezone
fuso_horario = timezone(timedelta(hours=-3))
data_e_hora_atuais = datetime.now()
data_e_hora_sao_paulo = data_e_hora_atuais.astimezone(fuso_horario)
hora = data_e_hora_sao_paulo.strftime('%H')

#what day is it?
today = date.today() # ex 2015-10-31
data = today.strftime("%d/%m")

#calling secret variables
CAT_KEY = os.environ.get("CAT_KEY")
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")
tele_user = os.environ.get("TELE_USER")
TOKEN = os.environ["TELEGRAM_TOKEN"]
bot = telebot.TeleBot(TOKEN)


#logging with myIG
try:
    cl = Client(request_timeout=7)
    cl.login(USERNAME, PASSWORD)
    print('gato logado')
except:
    print("deslogato")
    bot.send_message(tele_user, 'boturinsta com problema pra logar')
    sys.exit()

#get the cats
url = "https://api.thecatapi.com/v1/images/search?format=json&type=jpeg"
payload={}
headers = {
  'Content-Type': 'application/json',
  'x-api-key': CAT_KEY
}
proxies = {
  'http': 'http://10.10.1.10:3128',
}
response = requests.request("GET", url, headers=headers, data=payload, proxies=proxies)
todos = json.loads(response.text)
site = todos[0].get('url')
r = requests.get(site, allow_redirects=True)
open('gato.jpeg', 'wb').write(r.content)


#post the picture
max_retries = 3
retry_count = 0

while retry_count < max_retries:
    try:
        response = requests.request("GET", url, headers=headers, data=payload, proxies=proxies)
        todos = json.loads(response.text)
        site = todos[0].get('url')
        r = requests.get(site, allow_redirects=True)
        open('gato.jpeg', 'wb').write(r.content)
        response_gemini = gemini_image("Escreva uma legenda engraçada e/ou fofa sobre essa imagem de gato para postar no Instagram com hashtags","gato.jpeg")
        if response_gemini == None:
            response_gemini = "#CatOfTheDay #GatoDoDia"
        else:
            pass
        insta_string = f""" Gato do dia {data}
{response_gemini}"""

        cl.photo_upload('gato.jpeg', insta_string)
        print("foto publicada no insta")
        break  # Break the loop if upload is successful
    except ClientError as e:
        print(f"Error during photo upload: {e}")
        retry_count += 1
        if retry_count < max_retries:
            print(f"Retrying... (Attempt {retry_count}/{max_retries})")
            if e.status_code == 403:
                print("Exiting script due to 403 Forbidden error.")
                break  # Break the loop if 403 Forbidden error occurs during upload
        else:
            print("Max retries reached. Photo upload failed.")
            bot.send_message(tele_user, 'boturinsta com problema pra postar')
