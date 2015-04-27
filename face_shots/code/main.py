# class to manage the main page
import cgi
import json
import urllib
import urllib2
from pymongo import MongoClient

import web


# URL of the Solr API, prepopulated to get: all rows, score, and TBD query
solr_get = 'http://158.85.218.52:8983/solr/face_db/select?fl=*,score&rows=2147483647&wt=json&q='

render = web.template.render('templates/').main


class page:
    # the GET route
    def GET(self):
        # Read the 'query' parameter that may have been submitted with request
        input = web.input()
        query = input.query if input.has_key('query') else ''

        # Run the query if it exists
        num_results, results = self.run_query(query) if query != '' else (0, '')

        # And render the results via templates/index.html
        return render(cgi.escape(query, quote=True), num_results, results)

    # Run the query
    def run_query(self, query):
        try:
            if query.startswith('looks like:'):
                return self.looks_like(query[query.find(':') + 1:])

            like_query = query.startswith('like:')
            if (like_query):
                name = query[query.find(':') + 1:]
                query = '"{0}"'.format(name)

            # Call the solr_get url above appended with the passed in query (url encoded)
            response = json.loads(urllib2.urlopen(solr_get + urllib.quote_plus(query)).read())

            existing_keys = []
            results = filter(lambda result: result is not None and not (like_query and name in result),
                             map(lambda doc: self.format_doc_result(doc, existing_keys), response['response']['docs']))

            return len(results), reduce(lambda s1, s2: s1 + s2, results, '')

        except Exception as e:
            print e
            return 0, '<p class="result">{0}</p>'.format(e)

    # Given a doc, create a line of results
    def format_doc_result(self, doc, existing_keys):
        try:
            resource_name = doc['resourcename'][0]
            filename = resource_name[resource_name.rfind('/') + 1:]
            name = filename[:filename.rfind('.')]
            if '.' in name: name = name[:name.rfind('.')]
            key = name.replace(' ', '_');

            # Check for duplicates
            if key in existing_keys: return None
            existing_keys.append(key)

            score = doc['score']

            # Score, name
            html = '<p>{0:.4f}<a class="result" href="/content?key={1}" target="content">{2}</a>'.format(score, key,
                                                                                                         name)

            html += '</p>'
            return html

        except Exception as e:
            print e
            return '<p class="result">{0}</p>'.format(e)


    # Find celebrities who look like X
    def looks_like(self, name):
        try:
            client = MongoClient("158.85.218.52")
            results = client.celebritywatch.faces.find({"$and": [
                {"celebrity": "Elizabeth_Taylor"},
                {"similarity": {"$lt": 0.20}}
            ]})

            return results.count(), results

        except Exception as e:
            print e
            return 0, '<p class="result">{0}</p>'.format(e)
