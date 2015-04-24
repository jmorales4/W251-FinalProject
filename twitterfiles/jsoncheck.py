__author__ = 'dmilad'

import json
from pprint import pprint

with open('../tweetdata/tweets.Apr12-2055.json.txt') as datafile:
	for line in datafile:
		data = json.loads(line)

		pprint(data)