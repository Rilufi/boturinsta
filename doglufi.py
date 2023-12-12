import requests
import json
import os
import math
from instagrapi import Client
from instagrapi.exceptions import ClientError
import telebot
from datetime import date, timezone, timedelta, datetime

#get the time with timezone
fuso_horario = timezone(timedelta(hours=-3))
data_e_hora_atuais = datetime.now()
data_e_hora_sao_paulo = data_e_hora_atuais.astimezone(fuso_horario)
hora = data_e_hora_sao_paulo.strftime('%H')

#what day is it?
today = date.today() # ex 2015-10-31
data = today.strftime("%d/%m")

#calling secret variables
USUARIO = os.environ.get("USUARIO")
SENHA = os.environ.get("SENHA")
tele_user = os.environ.get("TELE_USER")
TOKEN = os.environ["TELEGRAM_TOKEN"]
bot = telebot.TeleBot(TOKEN)


#logging with myIG
try:
    cl = Client(request_timeout=7)
    cl.login(USUARIO, SENHA)
    print('dog logado')
except ClientError as e:
    if e.status_code == 403:
        print(f"Error during login: {e}")
        print("Exiting script due to 403 Forbidden error.")
        exit()
    else:
        bot.send_message(tele_user, 'doglufi com problema')
        print('dog deslogado')
        pass

#pegar foto de dog
def get_random_dog(filename: str='temp') -> None:
    r = requests.get('https://dog.ceo/api/breeds/image/random')
    rd = json.loads(r.content)
    r2 = requests.get(rd['message'])
    with open(filename, 'wb') as image:
        for chunk in r2:
            image.write(chunk)

insta_string = f""" Dog do dia {data}

#DogOfTheDay #CachorroDoDia"""

max_retries = 3
retry_count = 0

while retry_count < max_retries:
    try:
        get_random_dog('dog.jpeg')
        cl.photo_upload('dog.jpeg', insta_string)
        print("foto publicada no insta")
        break  # Break the loop if upload is successful
    except ClientError as e:
        print(f"Error during photo upload: {e}")
        retry_count += 1
        if retry_count < max_retries:
            print(f"Retrying... (Attempt {retry_count}/{max_retries})")
            if "403" in str(e):  # Check if the error message contains "403"
                print("Exiting script due to 403 Forbidden error.")
                break  # Break the loop if 403 Forbidden error occurs during upload
        else:
            print("Max retries reached. Photo upload failed.")
            bot.send_message(tele_user, 'doglufi com problema')
                print("Exiting script due to 403 Forbidden error.")
                break  # Break the loop if 403 Forbidden error occurs during upload
        else:
            print("Max retries reached. Photo upload failed.")
            bot.send_message(tele_user, 'doglufi com problema')
