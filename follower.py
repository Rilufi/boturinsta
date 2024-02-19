from instagrapi import Client
import time
import random
import os

#calling secret variables
username = os.environ.get("USUARIO")
password = os.environ.get("SENHA")

# Create an instagrapi client
client = Client(request_timeout=7)
client.login(username, password)

# Set the target account or hashtag related to dogs
target_account = "dogsofinstagram"

# Get the user IDs of accounts related to dogs
user_ids = [user.pk for user in client.user_search(target_account)]

# Like and follow accounts related to dogs with randomized sleep intervals
for user_id in user_ids:
    client.user_like(user_id)
    time.sleep(random.uniform(15, 30))  # Random sleep between 15 and 30 seconds
    client.user_follow(user_id)
    time.sleep(random.uniform(30, 60))  # Random sleep between 30 and 60 seconds

# Logout after completing actions
client.logout()

