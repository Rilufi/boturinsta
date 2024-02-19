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

# Search for users related to dogs
results = client.top_search(target_account)#, count=10)  # Adjust count as needed

# Extract user IDs from the search results
user_ids = [result["user"]["pk"] for result in results]

# Like and follow accounts related to dogs with randomized sleep intervals
for user_id in user_ids:
    client.user_like(user_id)
    time.sleep(random.uniform(15, 30))  # Random sleep between 15 and 30 seconds
    client.user_follow(user_id)
    time.sleep(random.uniform(30, 60))  # Random sleep between 30 and 60 seconds

# Logout after completing actions
client.logout()
