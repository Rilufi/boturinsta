import os
from instabot import Bot


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

# Like and follow accounts related to dogs
for user_id in user_ids:
    bot.like(user_id)
    bot.follow(user_id)

# Logout after completing actions
bot.logout()
