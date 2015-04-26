import os
import web
import object_storage
import json

render_tweet = web.template.render('templates/').tweet
render_tweets = web.template.render('templates/').content_list

# A class to build the latest tweets UI
class page:
    # the GET route
    def GET(self):
        # Read the 'person' parameter that may have been submitted with request
        input = web.input()
        person = input.person if input.has_key('person') else ''

        # Get the latest tweets
        tweets = self.get_tweets(person)

        tweet_html = ''
        for tweet in reversed(tweets):
            tweet_html = tweet_html + str(render_tweet( tweet['name'], tweet['screen_name'], tweet['profile_image_url'], tweet['created_at'], tweet['text']))

            # And render the results via templates/tweets.html
        return render_tweets(person, tweet_html)

    def get_tweets(self, person):
        user = os.environ.get('OBJECT_STORE_USER')
        api_key =  os.environ.get('OBJECT_STORE_API_KEY')
        datacenter =  os.environ.get('OBJECT_STORE_DATACENTER')
        sl_storage = object_storage.get_client(user, api_key, datacenter=datacenter)
        return json.loads(('[' + sl_storage['faces_tweets_latest'][person.lower() + '.tweets.json.txt'].read() + ']')\
            .replace('}', '},').replace('},]', '}]'))



