import tweepy
import os

# access tokens for @HackathonAcct
#access_token = "847744745090686976-vTf0XUilEVh3ashprVGEc3Rc8ohdZco"
#access_token_secret = "DgbIYYQyuGQR40pjfb0ZWKiPrIdVNlQuHNAvFqCARnxO2"

#identify ourselves as registered app
auth = tweepy.OAuthHandler("kGx0VVO7HR9rTrKCGOne7DJDn", "bniWiIqupj9OzQRoKAl6xtcAeAtrNbW6wesKNvD9iXX25xjDUS")

# authorise the users account
redirect_url = auth.get_authorization_url()
os.system("firefox " + redirect_url)
pin = raw_input("Please input the PIN given to you in your broswer\n>")
token = auth.get_access_token(verifier=pin)
access_token = token[0]
access_token_secret = token[1]

#auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#delete a users own tweets
first_name = raw_input("Please enter your old first name\n>").upper()
last_name = raw_input("Please enter your old last name\n>").upper()
new_name = raw_input("Please enter your new full name\n>")
handle = raw_input("Please enter your old twitter handle\n>").upper()

full_name = first_name + " " + last_name
print("Searching your tweets...")
public_tweets = tweepy.Cursor(api.user_timeline).items()

for tweet in public_tweets:
    if full_name in tweet.text.upper():
        print("Deleting this tweet because it contained your old name: ")
        print(tweet.text + "\n")
        api.destroy_status(tweet.id)

    elif handle in tweet.text.upper():
        print("Deleting this tweet becasuse it contained your old handle: ")
        print(tweet.text + "\n")
        api.destroy_status(tweet.id)

    elif first_name in tweet.text.upper():
        print("Old first name found. Do you want to delete this tweet? [y/n]")
        print(tweet.text)
        response = raw_input(">")
        if response == 'y':
            api.destroy_status(tweet.id)
            print("Deleting the tweet")
        else:
            print("Ignoring the tweet")

    else:
        print("Ignoring this tweet: " + tweet.text)

#ask other users to delete tweets
print("Searching your followers' tweets...")
followers = tweepy.Cursor(api.followers).items()
for follower in followers:
    name = follower.screen_name
    follower_tweets = api.user_timeline(screen_name=name, count=200)
    for follower_tweet in follower_tweets:
        if full_name in follower_tweet.text.upper():
            print("Asking @" + name + " to delete this tweet because it contained your old name: ")
            print(follower_tweet.text + "\n")
            api.send_direct_message(screen_name=name, text=('Please delete this tweet because it contains my old name: '))
            api.send_direct_message(screen_name=name, text=('http://twitter.com/' + name + "/status/" + follower_tweet.id_str))
