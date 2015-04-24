import datetime, json
import urllib2

resourcename = ''
text = 'qwerasdfzxcv'
n = 'Al Pacino'
st = ""

for i in range(2):
	timestring = str(int((datetime.datetime.now() - datetime.datetime.utcfromtimestamp(0)).total_seconds()*1000000))
	updatestring = {'doc': {'id': n + '.' + timestring, 'resourcename': '/tweets/' + n + '.' + timestring, 'tweet': text}}
	st += '\"add\": ' + json.dumps(updatestring) + ","

st = "{" + st[:-1] + "}"
print st

req = urllib2.Request(url='http://158.85.218.52:8983/solr/face_db/update/json?commit=true', data=st)
req.add_header('Content-type', 'application/json')
#f = urllib2.urlopen(req)
#print f.read()