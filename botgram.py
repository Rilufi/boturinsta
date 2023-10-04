import requests
import json
import urllib.request
import os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
import math
from instagrapi import Client
from instagrapi.types import StoryHashtag
from random import choice

import email
import imaplib
import re
import random

from instagrapi import Client
from instagrapi.mixins.challenge import ChallengeChoice

#calling secret variables
CAT_KEY = os.environ.get("CAT_KEY")
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")

CHALLENGE_EMAIL = os.environ.get("EMAIL_USER")
CHALLENGE_PASSWORD = os.environ.get("EMAIL_PASS")

IG_USERNAME = USERNAME
IG_PASSWORD = PASSWORD


def get_code_from_email(username):
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(CHALLENGE_EMAIL, CHALLENGE_PASSWORD)
    mail.select("inbox")
    result, data = mail.search(None, "(UNSEEN)")
    assert result == "OK", "Error1 during get_code_from_email: %s" % result
    ids = data.pop().split()
    for num in reversed(ids):
        mail.store(num, "+FLAGS", "\\Seen")  # mark as read
        result, data = mail.fetch(num, "(RFC822)")
        assert result == "OK", "Error2 during get_code_from_email: %s" % result
        msg = email.message_from_string(data[0][1].decode())
        payloads = msg.get_payload()
        if not isinstance(payloads, list):
            payloads = [msg]
        code = None
        for payload in payloads:
            body = payload.get_payload(decode=True).decode()
            if "<div" not in body:
                continue
            match = re.search(">([^>]*?({u})[^<]*?)<".format(u=username), body)
            if not match:
                continue
            print("Match from email:", match.group(1))
            match = re.search(r">(\d{6})<", body)
            if not match:
                print('Skip this email, "code" not found')
                continue
            code = match.group(1)
            if code:
                return code
    return False


def get_code_from_sms(username):
    while True:
        code = input(f"Enter code (6 digits) for {username}: ").strip()
        if code and code.isdigit():
            return code
    return None


def challenge_code_handler(username, choice):
    if choice == ChallengeChoice.SMS:
        return get_code_from_sms(username)
    elif choice == ChallengeChoice.EMAIL:
        return get_code_from_email(username)
    return False


def change_password_handler(username):
    # Simple way to generate a random string
    chars = list("abcdefghijklmnopqrstuvwxyz1234567890!&£@#")
    password = "".join(random.sample(chars, 10))
    return password


#logging with myIG
#try:
if __name__ == "__main__":
  cl = Client(request_timeout=7)
  cl.challenge_code_handler = challenge_code_handler
  cl.change_password_handler = change_password_handler
  cl.login(IG_USERNAME, IG_PASSWORD)
  print('gato tentando logar')
#except:
#  cl = Client(request_timeout=7)
#  cl.login(USERNAME, PASSWORD)
#  print('gato logado')
  

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
