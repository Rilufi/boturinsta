import requests
import json
import urllib.request
import os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
import math
from instagrapi import Client
from instagrapi.types import StoryHashtag
from random import choice
import telebot

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
  print('gato deslogado')
  bot.send_message(tele_user,  'boturinsta com problema')
  pass

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


def formatImage(image):
    base = Image.new('RGB', (1080,1920), (255,255,0))
    cat = Image.open(image)
    originalCat = cat.copy()

    #~ Resize and spawn multiple image of cat in the background
    wPercent = (216/float(originalCat.size[0]))
    hSize = int((float(originalCat.size[1])*float(wPercent)))
    smallCat = originalCat.resize((216,hSize), Image.LANCZOS)#Resampling.LANCZOS)

    #~ Reduce brightness & blur, goal is to put in foreground the main cat
    smallCat = ImageEnhance.Brightness(smallCat).enhance(.75)
    smallCat = smallCat.filter(ImageFilter.GaussianBlur(4))

    for i in range( math.ceil(base.size[1]/hSize) ):
        for j in range( math.ceil(base.size[0]/smallCat.size[0]) ):
            base.paste(smallCat, (j*smallCat.size[0],i*smallCat.size[1]))

    #~ Resize the image to fit, if it's too large (>1000) or too small (<800)
    if cat.size[0] > 1000 or cat.size[0] < 800:
        wPercent = (1000/float(cat.size[0]))
        hSize = int((float(cat.size[1])*float(wPercent)))
        cat = cat.resize((1000,hSize), Image.LANCZOS)#Resampling.LANCZOS)

    wPos = int((1080-cat.size[0])/2)
    hPos = int((1920-cat.size[1])/2)

    base.paste(cat, (wPos, hPos))
    base.save(image, quality=95)

cattags = ['cats', 'catlife', 'catsofinstagram','catlovers', 'cat', 'instacat', 'catstagram', 'catlover', 'kittens', 'catoftheday']
hashtag = cl.hashtag_info(choice(cattags))

def catliker(hash):
    medias = cl.hashtag_medias_recent_v1(hash, amount=1)
    dicmed = medias[0].dict()
    id = dicmed.get('id')
    print(dicmed.get('code'))
    pk = dicmed['user'].get('pk')
    cl.media_like(id)
    cl.user_follow(pk)

try:
  formatImage('gato.jpeg')
  cl.photo_upload_to_story('gato.jpeg', hashtags=[StoryHashtag(hashtag=hashtag, x=0.23, y=0.32, width=0.5, height=0.22)])#[StoryHashtag(hashtag=hashtag, x=0.23, y=0.32, width=0.5, height=0.22)])
  print("story de gato foi")
  #catliker(hashtag)
  #print("like e follow foi")
except:
  print("deu ruim o story de gato")
