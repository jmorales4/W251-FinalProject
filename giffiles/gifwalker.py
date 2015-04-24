from gifmaker import gifmaker
import os, sys
import resource

resource.setrlimit(resource.RLIMIT_NOFILE, (65536, 65536))

"""
call like this:
	python gifwalker.py [pathToMainDirectory] [savePath]

for example: 
	python gifmaker.py ./frame_images_DB/ ./gifs/

the script will build gifs for all images available for all celebrities the  main folder 
and write them to the directory specified

"""

def gifwalker(maindir, savepath):
	faces = os.walk(maindir).next()[1]

	for face in faces:
		print '\n' + ' '.join(face.split('_')) + ':'
		gifmaker(maindir, face, savepath)

if __name__ == '__main__':

	maindir = sys.argv[1]
	savepath = sys.argv[2]

	gifwalker(maindir, savepath)