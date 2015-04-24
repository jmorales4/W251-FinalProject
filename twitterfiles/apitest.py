#{"screen_name": "abuborhanuddin", "text": "Abdul Rahman bin Sipahon", "created_at": "Thu Apr 16 07:26:55 +0000 2015", "profile_image_url": "http://pbs.twimg.com/profile_images/587267452284731394/RaxHvL31_normal.jpg", "name": "abuborhanuddin", "face": "Abdul Rahman", "media_url": "None"}
#
#
#
#{
# "add": {"doc": {"id" : "TestDoc1", "title" : "test1"} },
# "add": {"doc": {"id" : "TestDoc2", "title" : "another test"} }
#}
#
#{
#  "add": {
#    "doc": {
#      "id": "Oprah Winfrey.1429706726",
#      "resourcename": "/tweets/Oprah Winfrey.1429706726",
#      "tweet": "qwerasdfzxcv"
#    }
#  }
#}

import datetime, json
import urllib2


print str(int((datetime.datetime.now() - datetime.datetime.utcfromtimestamp(0)).total_seconds()*1000000))

resourcename = ''
text = 'qwerasdfzxcv'
n = 'Al Pacino'

updatestring = {'add': {'doc': {'id': n + '.' + str(datetime.datetime.now()), 'resourcename': '/tweets/' + n + '.' + str(datetime.datetime.now()), 'tweet': text}}}
st = json.dumps(updatestring) + ","

print updatestring
print st

totalstring = {}

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

#stj = json.loads(st)
#print stj