import requests
import json
import urllib.request
import os
from myigbot import MyIGBot
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
import math
from instagrapi import Client
from time import sleep

#calling secret variables
CAT_KEY = os.environ.get("CAT_KEY")
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")

#logging with myIG
try:
   bot = MyIGBot(USERNAME, PASSWORD)
except:
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


def formatImage():
    base = Image.new('RGB', (1080,1920), (255,255,0))
    cat = Image.open('gato.jpeg')
    originalCat = cat.copy()

    #~ Resize and spawn multiple image of cat in the background
    wPercent = (216/float(originalCat.size[0]))
    hSize = int((float(originalCat.size[1])*float(wPercent)))
    smallCat = originalCat.resize((216,hSize), Image.Resampling.LANCZOS)

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
        cat = cat.resize((1000,hSize), Image.Resampling.LANCZOS)

    wPos = int((1080-cat.size[0])/2)
    hPos = int((1920-cat.size[1])/2)

    base.paste(cat, (wPos, hPos))
    base.save('gatogram.jpeg', quality=95)

try:
  formatImage()
  response = bot.upload_story('gatogram.jpeg')
  #cl.photo_upload_to_story('gatogram.jpeg')
  print("story de gato foi")
except:
  print("deu ruim o story")


#logging with instragrapi
cl = Client()
cl.login(USERNAME, PASSWORD)

#hashtags to be followed/liked
tags = ['catlife', 'catsofinstagram', 'instacat', 'catstagram', 'catlovers']

#function for liking and following
def catliker(hash):
    medias = cl.hashtag_medias_recent_v1(hash, amount=1)
    dicmed = medias[0].dict()
    id = dicmed.get('id')
    print(dicmed.get('code'))
    pk = dicmed['user'].get('pk')
    cl.media_like(id)
    cl.user_follow(pk)

for tag in tags:
    catliker(tag)
    print(f"{tag} hashtag foi")
