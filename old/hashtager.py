import os
from instagrapi import Client
from random import choice


#calling secret variables
CAT_KEY = os.environ.get("CAT_KEY")
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")


#logging with myIG
try:
  cl = Client(request_timeout=7)
  cl.login(USERNAME, PASSWORD)
  print('gato logado')
except:
  pass


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
  catliker(hashtag)
  print("like e follow foi")
except:
  print("deu ruim o story de gato")
