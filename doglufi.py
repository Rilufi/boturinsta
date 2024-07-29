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


# Variáveis de ambiente
dog_key = os.environ.get("DOG_KEY")
username = os.environ.get("USUARIO")
password = os.environ.get("SENHA")
tele_user = os.environ.get("TELE_USER")
token = os.environ["TELEGRAM_TOKEN"]
bot = telebot.TeleBot(token)

# Inicializando api do Gemini
GOOGLE_API_KEY=os.environ["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')

# Função para logar no Instagram com sessão
def logar_instagram():
    cl = Client()
    session_file = 'instadog_session.json'
    try:
        if os.path.exists(session_file):
            cl.load_settings(session_file)
        cl.login(username, password)
        cl.get_timeline_feed()
        cl.dump_settings(session_file)
    except Exception as e:
        print(f"Erro ao logar no Instagram: {e}")
        bot.send_message(tele_user, f"doglufi erro ao logar no Instagram: {e}")
    return cl

try:
    instagram_client = logar_instagram()
except Exception as e:
    print(f"Erro ao logar no Instagram: {e}")
    bot.send_message(tele_user, f"doglufi erro ao logar no Instagram: {e}")

# Função para postar foto no Instagram
def post_instagram_photo(cl, image_path, caption):
    try:
        cl.photo_upload(image_path, caption)
        print("Foto publicada no Instagram")
    except Exception as e:
        print(f"Erro ao postar foto no Instagram: {e}")
        bot.send_message(tele_user, f"doglufi com problema pra postar: {e}")

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

# Obtém URL de uma imagem de cachorro
url = "https://api.thedogapi.com/v1/images/search?format=json&type=jpeg"
headers = {
    'Content-Type': 'application/json',
    'x-api-key': dog_key
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
response_gemini = gemini_image("Escreva uma legenda em português do Brasil engraçada e/ou fofa sobre essa imagem de cachorro para postar no Instagram com hashtags","dog.jpeg")
if response_gemini is None:
    response_gemini = "#DogOfTheDay #CachorroDoDia"
elif response_gemini == '"':
    response_gemini = "#DogOfTheDay #CachorroDoDia"
else:
    pass
insta_string = f"""Dog do dia {data}
{response_gemini}"""
# Post the image on Instagram
if instagram_client:
    try:
        post_instagram_photo(instagram_client, 'dog.jpeg', insta_string)
    except Exception as e:
        print(f"Erro ao postar foto no Instagram: {e}")
        bot.send_message(tele_user, 'doglufi com problema pra postar imagem')
