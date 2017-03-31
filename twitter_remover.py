import tweepy

#identify ourselves as registered app
auth = tweepy.OAuthHandler("kGx0VVO7HR9rTrKCGOne7DJDn", "bniWiIqupj9OzQRoKAl6xtcAeAtrNbW6wesKNvD9iXX25xjDUS")
auth.set_access_token("847744745090686976-vTf0XUilEVh3ashprVGEc3Rc8ohdZco", "DgbIYYQyuGQR40pjfb0ZWKiPrIdVNlQuHNAvFqCARnxO2")
api = tweepy.API(auth)

#delete tweets containg deadname
first_name = raw_input("Please enter your old first name\n>")
last_name = raw_input("Please enter your old last name\n>")
full_name = first_name + " " + last_name
handle = raw_input("Please enter your old twitter handle\n>")

#delete a users own tweets
print("Searching your tweets...")
public_tweets = tweepy.Cursor(api.user_timeline).items()
for tweet in public_tweets:
    if full_name in tweet.text:
        print("Deleting this tweet becasuse it contained your old name: ")
        print(tweet.text)
        api.destroy_status(tweet.id)

    elif handle in tweet.text:
        print("Deleting this tweet becasuse it contained your old handle: ")
        print(tweet.text)
        api.destroy_status(tweet.id)

    elif first_name in tweet.text:
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
print("Searching other people's tweets...")
query = api.search(q=handle)
for tweet in query:
    print(tweet.text) 
