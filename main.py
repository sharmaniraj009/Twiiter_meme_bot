import os
import praw
import requests
import tweepy
from dotenv import load_dotenv

load_dotenv('.env')

auth = tweepy.OAuth1UserHandler(
    os.getenv('consumer_key'), os.getenv('consumer_secret'), os.getenv(
        'access_token'), os.getenv('access_token_secret')
)
api = tweepy.API(auth)

reddit = praw.Reddit(
        client_id= os.getenv('client_id'),
        client_secret= os.getenv('client_secret'),
        user_agent= os.getenv('user_agent')
)

def post_meme():
    subreddit = reddit.subreddit('dankmemes')
    post = subreddit.random()
    
    image_url = post.url
    response = requests.get(image_url)
    
    # Check the size of the image
    if len(response.content) > 5000000:
        print("Image size too large to upload")
        return
    
    with open("temp.jpg", "wb") as f:
        f.write(response.content)
    
    try:
        api.update_status_with_media(image_url,"temp.jpg")
        print("Meme posted successfully!")
    except Exception as e:
        print(f"Failed to post meme: {e}")

post_meme()
