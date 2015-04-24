from images2gif import writeGif
from PIL import Image
import os, sys

"""
call like this:
	python gifmaker.py [pathToMainDirectory] [fname_lname] [savePath]

for example: 
	python gifmaker.py ./frame_images_DB/ Alec_Baldwin ./gifs/

the script will build gifs for all images available for that celebrity and write them to the directory specified

"""

def gifmaker(maindir, face, savepath):
	paths = [x[0] for x in os.walk(maindir + face)][1:]
	print 'Number of gifs to be generated: ' + str(len(paths))

	for path in paths:
		file_names = sorted((path+'/'+fn for fn in os.listdir(path) if fn.endswith('.jpg')))

		print 'Number of images in gif ' + path[-1:] + ': ' + str(len(file_names))

		images = [Image.open(fn) for fn in file_names]

		#downsize images from (480,360) to quarter the size
		resize = (240,180)
		for im in images:
			im.thumbnail(resize, Image.ANTIALIAS)

		filename = savepath + face + '/' + path[-1:] + ".GIF"
		d = os.path.dirname(filename)
		if not os.path.exists(d):
			os.makedirs(d)
		writeGif(filename, images, duration = 0.041, repeat = False)
		#24 frame per second

if __name__ == '__main__':

	maindir = sys.argv[1]
	face = sys.argv[2]
	savepath = sys.argv[3]

	gifmaker(maindir, face, savepath)