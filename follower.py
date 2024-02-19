from instapy import InstaPy
import os

#calling secret variables
username = os.environ.get("USUARIO")
password = os.environ.get("SENHA")

# Set the target account or hashtag related to dogs
target_account = "dogsofinstagram"

# Create an InstaPy session
session = InstaPy(username=username, password=password)

# Login to Instagram
session.login()

# Set up actions to like and follow accounts related to dogs
session.set_relationship_bounds(enabled=True, max_followers=1000)
session.set_do_follow(True, percentage=50)
session.set_user_interact(amount=3, randomize=True, percentage=80, media="Photo")

# Interact with posts from the target account
session.like_by_targets([target_account], amount=5, randomize=True)

# End the session
session.end()
