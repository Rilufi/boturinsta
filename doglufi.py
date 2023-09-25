import requests
import json
import urllib.request
import os
from myigbot import MyIGBot
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
import math
from instagrapi import Client
from time import sleep
from datetime import datetime

#calling secret variables
USUARIO = os.environ.get("USUARIO")
SENHA = os.environ.get("SENHA")

#logging with myIG
try:
  cl = Client(request_timeout=7)
  cl.login(USUARIO, SENHA)
  print('dog logado')
except:
  print('dog deslogado')
  pass


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


#pegar foto de dog
def get_random_dog(filename: str='temp') -> None:

    r = requests.get('https://dog.ceo/api/breeds/image/random')
    rd = json.loads(r.content)
    r2 = requests.get(rd['message'])

    with open(filename, 'wb') as image:
        for chunk in r2:
            image.write(chunk)

try:
  get_random_dog('dog.jpeg')
  formatImage('dog.jpeg')
  cl.photo_upload_to_story('dog.jpeg')
  print("story de dog foi")
except:
  print("deu ruim o story de dog")
  pass


#hashtags to be followed/liked
tags_odd = ['dog', 'doglife', 'dogsofinstagram','doglovers', 'dogoftheday']
tags_even = ['dogs', 'dogstagram', 'instadog', 'puppy', 'doglover']

#function for liking and following
def catliker(hash):
    sleep(60)
    medias = cl.hashtag_medias_recent_v1(hash, amount=1)
    dicmed = medias[0].dict()
    id = dicmed.get('id')
#    print(dicmed.get('code'))
    pk = dicmed['user'].get('pk')
    sleep(60)
    cl.media_like(id)
    sleep(60)
    cl.user_follow(pk)

def tagger(tags):
    for tag in tags:
        try:
           catliker(tag)
           print(f"#{tag} foi")
        except:
           print(f"#{tag} num foi")

#get the hour
data_e_hora_atuais = datetime.now()
hour = data_e_hora_atuais.strftime('%H')

if (int(hour) % 2) == 0:
   tagger(tags_even)
else:
   tagger(tags_odd)