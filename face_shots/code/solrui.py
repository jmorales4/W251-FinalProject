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
        result = '<p>Number of results found: {}</p>'.format(num_docs)

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
        score = doc['score']

        folder = './static/gifs/' + person.replace(' ', '_')
        if not os.path.exists(folder): return None

        html = '<p><a href="./static/wiki/{0}" target="wiki">{1}</a>'.format(filename, person)
        for gif in os.listdir(folder):
            html += ' <a href="{0}/{1}" target="video">{1}</a>'.format(folder, gif)

        html += 'Score: {:.4f}</p>'.format(score)
        return html


if __name__ == "__main__":
    app.run()
