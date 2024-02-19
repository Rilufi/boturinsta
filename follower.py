import os
from instabot import Bot
import time
import random

#calling secret variables
username = os.environ.get("USUARIO")
password = os.environ.get("SENHA")

# Create an Instabot instance
bot = Bot()
bot.login(username=username, password=password)

# Set the target account or hashtag related to dogs
target_account = "dogsofinstagram"

# Get the user IDs of accounts related to dogs
user_ids = bot.get_hashtag_users(target_account)

# Like and follow accounts related to dogs with randomized sleep intervals
for user_id in user_ids:
    bot.like(user_id)
    time.sleep(random.uniform(20, 30))  # Random sleep between 20 and 30 seconds
    bot.follow(user_id)
    time.sleep(random.uniform(40, 60))  # Random sleep between 40 and 60 seconds

# Logout after completing actions
bot.logout()
