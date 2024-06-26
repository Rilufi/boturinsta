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

# Define função para postagem no Instagram
def post_instagram_photo():
    try:
        # Realiza login na conta do Instagram
        cl = Client(request_timeout=7)
        cl.login(USERNAME, PASSWORD)
        print('Logado no Instagram')
    except Exception as e:
        print("Erro ao logar no Instagram:", e)
        bot.send_message(tele_user, 'doglufi com problema pra logar')
        sys.exit()

    # Obtém URL de uma imagem de cachorro
    url = "https://api.thedogapi.com/v1/images/search?format=json&type=jpeg"
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': DOG_KEY
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Verifica se a requisição foi bem-sucedida
        if response.text:
            todos = json.loads(response.text)
        else:
            raise ValueError("Resposta da API está vazia")
    except requests.exceptions.RequestException as e:
        print("Erro ao fazer a requisição para a API:", e)
        bot.send_message(tele_user, 'Erro ao obter imagem da API de cachorros')
        sys.exit()
    except json.JSONDecodeError as e:
        print("Erro ao decodificar o JSON:", e)
        bot.send_message(tele_user, 'Erro ao decodificar a resposta da API de cachorros')
        sys.exit()
    except ValueError as e:
        print("Erro:", e)
        bot.send_message(tele_user, 'Resposta da API de cachorros está vazia')
        sys.exit()

    site = todos[0].get('url')
    r = requests.get(site, allow_redirects=True)
    open('dog.jpeg', 'wb').write(r.content)

    # Gera legenda para a foto do Instagram
    data = date.today().strftime("%d/%m")
    response_gemini = gemini_image("Escreva uma legenda engraçada e/ou fofa sobre essa imagem de cachorro para postar no Instagram com hashtags","dog.jpeg")
    if response_gemini is None:
        response_gemini = "#DogOfTheDay #CachorroDoDia"
    
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
