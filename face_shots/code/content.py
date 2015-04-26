# class to manage the person portal
import json
import os
import urllib
import urllib2
import web

# URL of the Solr API, prepopulated to get: all rows, score, and TBD query
# solr_get = 'http://127.0.0.1:8983/solr/face_db/select?fl=*,score&rows=2147483647&wt=json&q='
solr_get = 'http://158.85.218.52:8983/solr/face_db/select?fl=*,score&rows=2147483647&wt=json&q='

render = web.template.render('templates/').content

class page:

    # the GET route
    def GET(self):
        # Read the 'query' parameter that may have been submitted with request
        input = web.input()
        key = input.key if input.has_key('key') else ''

        name = key.replace('_', ' ')
        image_path = '/static/all_celebrities/{0}/{0}.jpg'.format(key)
        wiki_path = 'http://en.wikipedia.org/wiki/' + key
        tweet_path = '/tweets?person=' + key
        video_path = '/videos?person=' + key

        # videos = sorted(os.listdir(videopath))
        # for video in videos:
        #     html += ' <a class=vid_link href="{0}/{1}" target="video" onclick="showWiki(\'{2}\');">{3}</a>' \
        #         .format(folder, video, filepath, '<img src=./static/movie.png>')
        #

    # And render the results via templates/index.html
        return render(name, image_path, wiki_path, tweet_path, video_path)

