import os

def tweetwalker(maindir):
	faces = ['../tweetdata/'+f for f in os.walk(maindir).next()[2] if f.endswith(".txt")]
	print faces

tweetwalker('../tweetdata/')