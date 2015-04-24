# based on http://badhessian.org/2012/10/collecting-real-time-twitter-data-with-the-streaming-api/
# with modifications by http://github.com/marciw

__author__ = 'dmilad'

from twaiter import TWaiter
import tweepy, twitterparams
import time, sys, os
import email_alert

consumer_key = twitterparams.OAuthConsKey
consumer_secret = twitterparams.OAuthConsSecret
access_token = twitterparams.OAuthToken
access_token_secret = twitterparams.OAuthTokenSecret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def main():

    if not os.path.exists('tweetdata/'):
        os.makedirs('tweetdata/')

    if not os.path.exists('deletedtweets/'):
        os.makedirs('deletedtweets/')

    collection = 'tweets'
    waiter = TWaiter(api, collection)

    names = []

    with open('twitterfiles/names/names_sample.txt', 'r') as namefile:
        names = [namefile.read()]

    print "Collecting tweets. Please wait."

    try:
        stream = tweepy.Stream(auth, waiter)
        stream.filter(track = names)
    except Exception, e:
        print "An error occurred. No tweets collected.", e
        stream.disconnect()

        email_alert.send_email_alert()
        time.sleep(60)



if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception, e:
            print "error: ", e
            print "retrying in 60 seconds..."
        time.sleep(60)
