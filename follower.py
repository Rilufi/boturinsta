from instagrapi import Client
import time
import random
import os
import requests

#calling secret variables
username = os.environ.get("USUARIO")
password = os.environ.get("SENHA")

# Create an instagrapi client
client = Client(request_timeout=7)
client.login(username, password)

# Set the custom user agent in the headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Set the target account or hashtag related to dogs
target_account = "dogsofinstagram"

# Search for users related to dogs
response = requests.get(
    f"https://www.instagram.com/web/search/topsearch/?context=blended&query={target_account}&rank_token=0.7763938004511706&include_reel=true",
    headers=headers
)
results = response.json().get('users', [])
print(results)

# Extract user IDs from the search results
user_ids = [result["user"]["pk"] for result in results]
print(user_ids)

# Like and follow accounts related to dogs with randomized sleep intervals
for user_id in user_ids:
    client.user_like(user_id)
    time.sleep(random.uniform(15, 30))  # Random sleep between 15 and 30 seconds
    client.user_follow(user_id)
    time.sleep(random.uniform(30, 60))  # Random sleep between 30 and 60 seconds

# Logout after completing actions
client.logout()
