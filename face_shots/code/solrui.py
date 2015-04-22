import os

__author__ = 'jmorales'

import web
import urllib
import urllib2
import json

# URL of the Solr API, prepopulated to get: all rows, score, and TBD query
# solr_get = 'http://127.0.0.1:8983/solr/face_db/select?fl=*,score&rows=2147483647&wt=json&q='
solr_get = 'http://158.85.218.52:8983/solr/face_db/select?fl=*,score&rows=2147483647&wt=json&q='

# Default route
urls = (
    '/', 'index'
)

# web.py objects
render = web.template.render('templates/')
app = web.application(urls, globals())

# class to manage the default route
class index:
    # the GET route
    def GET(self):
        # Read the 'query' parameter that may have been submitted with request
        input = web.input()
        query = input.query if input.has_key('query') else ''

        # Run the query if it exists
        results = self.run_query(query) if query != '' else ''

        # And render the results via templates/index.html
        return render.index(query, results)

    # Run the query
    def run_query(self, query):
        # Call the solr_get url above appended with the passed in query (url encoded)
        response = json.loads(urllib2.urlopen(solr_get + urllib.quote_plus(query)).read())

        # Pick off number of docs
        num_docs = response['response']['numFound']
        result = '<p>{} results found</p>'.format(num_docs)

        # Add a line for each doc
        if num_docs > 0:
            result += reduce(lambda s1, s2: s1 + s2,
                             filter(lambda s1: s1 != None, map(self.format_doc_result, response['response']['docs'])))

        return result

    # Given a doc, create a line of results
    def format_doc_result(self, doc):
        resource_name = doc['resourcename'][0]
        filename = resource_name[resource_name.rfind('/') + 1:]
        person = filename[:filename.rfind('.')]
        filepath = 'http://en.wikipedia.org/wiki/' + person.replace(' ', '_')
        score = doc['score']

        folder = './static/gifs/' + person.replace(' ', '_')
        if not os.path.exists(folder): return None

        videos = sorted(os.listdir(folder))

        html = '<p>{0:.4f}<a href="{1}" target="wiki" onclick="showVideo(\'{3}/{4}\')">{2}</a>'\
            .format(score, filepath, person, folder, videos[0])

        for video in videos:
            html += ' <a class=vid_link href="{0}/{1}" target="video" onclick="showWiki(\'{2}\');">{3}</a>'\
                .format(folder, video, filepath, '<img src=./static/movie.png>')

        html += '</p>'
        return html


if __name__ == "__main__":
    app.run()
