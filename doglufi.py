import requests
import json
import urllib.request
import os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
import math
from instagrapi import Client
from instagrapi.types import StoryHashtag
from random import choice


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

dogtags = ['dog', 'doglife', 'dogsofinstagram','doglovers', 'dogoftheday', 'dogs', 'dogstagram', 'instadog', 'puppy', 'doglover']
hashtag = cl.hashtag_info(choice(dogtags))


try:
  get_random_dog('dog.jpeg')
  formatImage('dog.jpeg')
  cl.photo_upload_to_story('dog.jpeg', hashtags=[StoryHashtag(hashtag=hashtag, x=0.23, y=0.32, width=0.5, height=0.22)])#[StoryHashtag(hashtag=hashtag, x=0.23, y=0.32, width=0.5, height=0.22)])
  print("story de dog foi")
except:
  print("deu ruim o story de dog")
  pass
