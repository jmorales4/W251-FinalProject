__author__ = 'dmilad'

import os, sys

"""
collect name of all people in the dataset

and write as a filter string, to be fed to the twitter streaming files
"""

def namecollector(maindir, savepath):
	faces = os.walk(maindir).next()[1]

	names = ""

	for face in faces:
		name = ' '.join(face.split('_'))+','
		names += name
		print name
	
	#get rid of last comma
	names = names[:-1]
	with open(savepath, 'w') as f:
		f.write(names) 

if __name__ == '__main__':

	maindir = sys.argv[1]
	savepath = sys.argv[2]

	namecollector(maindir, savepath)