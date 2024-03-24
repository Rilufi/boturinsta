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
DOG_KEY = os.environ.get("DOG_KEY")
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")
tele_user = os.environ.get("TELE_USER")
TOKEN = os.environ["TELEGRAM_TOKEN"]
bot = telebot.TeleBot(TOKEN)


#logging with myIG
try:
    cl = Client(request_timeout=7)
    cl.login(USERNAME, PASSWORD)
    print('cachorro logado')
except ClientError as e:
    if e.status_code == 403:
        print(f"Error during login: {e}")
        print("Exiting script due to 403 Forbidden error.")
        exit()
    else:
        print(f"Error during login: {e}")
        bot.send_message(tele_user, 'boturinsta com problema')
        pass

#get the dogs
url = "https://api.thedogapi.com/v1/images/search?format=json&type=jpeg"
payload={}
headers = {
  'Content-Type': 'application/json',
  'x-api-key': DOG_KEY
}
proxies = {
  'http': 'http://10.10.1.10:3128',
}
response = requests.request("GET", url, headers=headers, data=payload, proxies=proxies)
todos = json.loads(response.text)
site = todos[0].get('url')
r = requests.get(site, allow_redirects=True)
open('dog.jpeg', 'wb').write(r.content)


#post the picture
max_retries = 3
retry_count = 0

while retry_count < max_retries:
    try:
        response = requests.request("GET", url, headers=headers, data=payload, proxies=proxies)
        todos = json.loads(response.text)
        site = todos[0].get('url')
        r = requests.get(site, allow_redirects=True)
        open('dog.jpeg', 'wb').write(r.content)

        insta_string = f""" Dog of the day {data}

#DogOfTheDay #CachorroDoDia"""

        cl.photo_upload('dog.jpeg', insta_string)
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
            bot.send_message(tele_user, 'boturinsta com problema')
