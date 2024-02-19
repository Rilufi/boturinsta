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

# Like and follow accounts related to dogs with sleep intervals
for user_id in user_ids:
    bot.like(user_id)
    time.sleep(10)  # Sleep for 10 seconds between likes
    bot.follow(user_id)
    time.sleep(15)  # Sleep for 15 seconds between follows

# Logout after completing actions
bot.logout()
