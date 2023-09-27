# Boturinsta

Posting hourly pet stories on Instagram, after reshaping the image.

## Requirements
We employ here the unnoficial Instagram private API [instagrapi](https://subzeroid.github.io/instagrapi/)

### How this works?
Both "botgram.py" (cats) and "doglufi.py" (dogs) files consists in the scripts for getting the pets, reshaping the images, chosing a hashtag and posting the stories. Everything automated from the GitHub Actions.

#### Where does the pets come from?
The cats come from [The Cat API](https://thecatapi.com/) while the dogs com from [Dog API](https://dog.ceo/dog-api/)

#### Reshape image
There's a function to reshape the image to fit the stories.

#### Post stories
This function post the stories after choosing a random hashtag from our list.

#### Other function(s)
I've also tried a function for following accounts and liking pictures that post hashtags about cats and dogs, I didn't found a way to evade Instagram's request limit. Already tried waiting after each request and lowering the number of follows.
