# based on http://badhessian.org/2012/10/collecting-real-time-twitter-data-with-the-streaming-api/
# with modifications by http://github.com/marciw
# requires Tweepy https://github.com/tweepy/tweepy

__author__ = 'dmilad'

from tweepy import StreamListener
import json, time, sys, os
import object_storage
import tweettail
import urllib2
import datetime

class TWaiter(StreamListener):

    def __init__(self, api = None, label = 'tweets'):
        self.api = api or API()
        self.bulkcounter = 0
        self.apicounter = 0
        self.label = label
        self.output  = open('tweetdata/' + label + '.' + time.strftime('%Y-%m-%d_%H-%M-%S') + '.txt', 'w')
        #self.outputj  = open('../tweetdata/' + label + '.' + time.strftime('%Y-%m-%d_%H-%M-%S') + '.json', 'w')
        self.deleted  = open('deletedtweets/deleted_tweets.txt', 'a')
        self.names = []
        self.files_to_update = []
        with open('twitterfiles/names/names_sample.txt', 'r') as namesfile:
            self.names = namesfile.readline().split(',')
        self.sl_storage = object_storage.get_client('SLOS431078-4:SL431078', 'c52b259c2ff5ece265e453b917e0dcf8100ecc2e05c4cbe01410e47a81edd1cc', datacenter='dal05')
        self.apistring = ""

    def on_data(self, data):
        # The presence of 'in_reply_to_status' indicates a "normal" tweet.
        # The presence of 'delete' indicates a tweet that was deleted after posting.
        if  'in_reply_to_status' in data:
            self.on_status(data)
        elif 'delete' in data:
            delete = json.loads(data)['delete']['status']
            if self.on_delete(delete['id'], delete['user_id']) is False:
                return False


    def on_status(self, status):
        all = str(json.dumps(json.loads(status)))

        #archive the entire tweet object
        self.output.write(all + '\n')  

        created_at = str(json.dumps(json.loads(status)['created_at']))[1:-1]
        screen_name = str(json.dumps(json.loads(status)['user']['screen_name']))[1:-1]
        name = str(json.dumps(json.loads(status)['user']['name']))[1:-1]
        profile_image_url = str(json.dumps(json.loads(status)['user']['profile_image_url']))[1:-1]
        text = str(json.dumps(json.loads(status)['text']))[1:-1]
        media_url = 'None'
        try:
            media_url = str(json.dumps(json.loads(status)['entities']['media']['media_url']))[1:-1]
        except:
            pass
 
        jsondict = {'created_at': created_at, 'screen_name': screen_name, 'name': name, 'profile_image_url': profile_image_url, 'text': text, 'media_url': media_url}

        #associate with the right face
        for n in self.names:
            if n.lower() in text.lower():
                self.bulkcounter += 1
                self.apicounter += 1

                print self.bulkcounter, self.apicounter, n, text

                self.files_to_update.append('tweetdata/' + '_'.join(n.lower().split(' ')) + '.tweets.json.txt')
                jsondict['face'] = n

                recent_four = ""
                try:
                    with open('tweetdata/' + '_'.join(n.lower().split(' ')) + '.tweets.json.txt', 'r') as rfile:
                        recent_four = tweettail.tail(rfile, 4)
                except:
                    pass

                #time in miliseconds since epoch
                timestring = str(int((datetime.datetime.now() - datetime.datetime.utcfromtimestamp(0)).total_seconds()*1000000))
                #tweet doc to push to solr
                apisubjson = {'doc': {'id': n + '.' + timestring, 'resourcename': '/tweets/' + n + '.' + timestring, 'tweet': text}}
                self.apistring += '\"add\": ' + json.dumps(apisubjson) + ","

                #push 10 tweets at a time
                if self.apicounter >= 10:

                    #format the string
                    self.apistring = "{" + self.apistring[:-1] + "}"

                    #make API call to update Solr index
                    req = urllib2.Request(url='http://158.85.218.52:8983/solr/face_db/update/json?commit=true', data=self.apistring)
                    req.add_header('Content-type', 'application/json')
                    urllib2.urlopen(req)
                    #print self.apistring

                    self.apicounter = 0
                    self.apistring = ""


                with open('tweetdata/' + '_'.join(n.lower().split(' ')) + '.tweets.json.txt', 'w') as wfile:
                    if recent_four != "":
                        wfile.write(recent_four+'\n')
                    #wfile.write('\n')
                    json.dump(jsondict, wfile)

                    #write interesting parts to a separate file
                    #json.dump(jsondict, self.outputj)
                      
                    if self.bulkcounter >= 100:
                        self.output.close()

                        #write to swift object storage
                        with open(self.output.name, 'r') as self.output:
                            self.sl_storage['faces_tweets_bulk'][self.output.name.split('/')[-1]].send(self.output)

                        #remove local copy
                        os.remove(self.output.name)

                        #send them to object store
                        self.files_to_update = list(set(self.files_to_update))
                        for f in self.files_to_update:
                            with open(f, 'r') as rfile:
                                self.sl_storage['faces_tweets_latest'][rfile.name.split('/')[-1]].send(rfile)                            

                        print "A new cycle of tweets..."
                        self.output = open('tweetdata/' + self.label + '.' + time.strftime('%Y-%m-%d_%H-%M-%S') + '.txt', 'w')
                        self.bulkcounter = 0

                        self.files_to_update = []            
                        #sys.exit()
                    #else:
                        #self.outputj.write(',\n')
                break                   
        return

    def on_delete(self, status_id, user_id):
        self.deleted.write(str(status_id) + "\n")
        return

    def on_error(self, status_code):
        sys.stderr.write('Error: ' + str(status_code) + "\n")
        return False
    
    def on_timeout(self):
        sys.stderr.write("Timeout, sleeping for 60 seconds...\n")
        time.sleep(60)
        return 