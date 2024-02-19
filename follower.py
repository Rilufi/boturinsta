from InstagramAPI import InstagramAPI
import time
import random


#calling secret variables
username = os.environ.get("USUARIO")
password = os.environ.get("SENHA")

# Create an InstagramAPI instance
api = InstagramAPI(username, password)
api.login()

# Set the target account or hashtag related to dogs
target_account = "dogsofinstagram"

# Get the user IDs of accounts related to dogs
api.searchUsername(target_account)
user_id = api.LastJson.get('user', {}).get('pk', None)

# Like and follow accounts related to dogs with randomized sleep intervals
if user_id:
    api.getUserFollowings(user_id)
    followings = api.LastJson.get('users', [])
    
    for user in followings:
        user_id = user.get('pk')
        
        api.like(user_id)
        time.sleep(random.uniform(15, 30))  # Random sleep between 15 and 30 seconds
        api.follow(user_id)
        time.sleep(random.uniform(30, 60))  # Random sleep between 30 and 60 seconds

# Logout after completing actions
api.logout()
