# class to manage the main page
import json
import os
import urllib
import urllib2
import web

# URL of the Solr API, prepopulated to get: all rows, score, and TBD query
# solr_get = 'http://127.0.0.1:8983/solr/face_db/select?fl=*,score&rows=2147483647&wt=json&q='
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
        return render(query, num_results, results)

    # Run the query
    def run_query(self, query):
        # Call the solr_get url above appended with the passed in query (url encoded)
        response = json.loads(urllib2.urlopen(solr_get + urllib.quote_plus(query)).read())

        result = ''
        existing_keys = []

        # Add a line for each doc
        result += reduce(lambda s1, s2: s1 + s2,
                         filter(lambda s1: s1 is not None,
                                map(lambda doc: self.format_doc_result(doc, existing_keys),
                                    response['response']['docs'])),
                         '')

        return len(existing_keys), result


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
            html = '<p>{0:.4f}<a class="result" href="/content?key={1}" target="content">{2}</a>'.format(score, key, name)

            html += '</p>'
            return html

        except Exception as e:
            print e
            return None

