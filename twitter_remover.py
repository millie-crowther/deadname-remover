import tweepy
import os

#identify ourselves as registered app
auth = tweepy.OAuthHandler("kGx0VVO7HR9rTrKCGOne7DJDn", "bniWiIqupj9OzQRoKAl6xtcAeAtrNbW6wesKNvD9iXX25xjDUS")

# authorise the users account
os.system("firefox " + auth.get_authorization_url())
pin = raw_input("Please input the PIN given to you in your browser\n>")
access_token, access_token_secret = auth.get_access_token(verifier=pin)

#initialise the API
api = tweepy.API(auth)

#get input from user
first_name = raw_input("Please enter your old first name\n>").upper()
last_name = raw_input("Please enter your old last name\n>").upper()
handle = raw_input("Please enter your old twitter handle\n>").upper()
full_name = first_name + " " + last_name

#iterate through all of users tweets
print("Searching your tweets...")
public_tweets = tweepy.Cursor(api.user_timeline).items()
for tweet in public_tweets:
    #search for full name
    if full_name in tweet.text.upper():
        print("Deleting this tweet because it contained your old name: \n" + tweet.text)
        api.destroy_status(tweet.id)

    #search for old handle
    elif handle in tweet.text.upper():
        print("Deleting this tweet becasuse it contained your old handle: \n" + tweet.text)
        api.destroy_status(tweet.id)

    #search for first name only - require confirmation
    elif first_name in tweet.text.upper():
        print("Old first name found only. Do you want to delete this tweet? [y/n]\n" + tweet.text)
        response = raw_input(">")
        if response == 'y':
            api.destroy_status(tweet.id)

#ask other users to delete tweets
print("Searching your followers' tweets...")

#iterate through all of your followers
followers = tweepy.Cursor(api.followers).items()
for follower in followers:
    name = follower.screen_name

    #iterate through each follower's tweets
    follower_tweets = api.user_timeline(screen_name=name, count=200)
    for follower_tweet in follower_tweets:
        tweet_url = 'http://twitter.com/' + name + "/status/" + follower_tweet.id_str

        #ask to delete tweets with your full name
        if full_name in follower_tweet.text.upper():
            print("Asking @" + name + " to delete this tweet because it contained your old name: ")
            print(follower_tweet.text)
            api.send_direct_message(screen_name = name, text = 'Please delete this tweet because it contains my old name: ')
            api.send_direct_message(screen_name = name, text = tweet_url)

        #ask to delete tweets with your first name only - require confirmation
        elif first_name in tweet.text.upper():
            print("Old first name found only. Do you want to ask @" + name + " to delete this tweet? [y/n]")
            print(follower_tweet.text)
            response = raw_input(">")
            if response == 'y':
                api.send_direct_message(screen_name = name, text = 'Please delete this tweet because it contains my old first name: ')
                api.send_direct_message(screen_name = name, text = tweet_url)

        #ask to delete tweets with your old handle
        elif handle in follower_tweet.text.upper():
            print("Asking @" + name + " to delete this tweet because it contained your old handle: ")
            print(follower_tweet.text)
            api.send_direct_message(screen_name = name, text = 'Please delete this tweet because it contains my old handle: ')
            api.send_direct_message(screen_name = name, text = tweet_url)
