# use the normalized images from YouTubeFace data set to compute similarities between celebrities
# Author: Sean Y Wang
# Version: 0.1
# Date: 2015 April 23
# Version: 0.3 
# Date: 2015 April 27
# purpose: calculate pair wise cosine distance between any of two celebrity headshots
# find and rank the most similar and most dissimilar faces
# added cropping of headshot to reduce or eliminate the influence of black edges

from scipy import misc
import matplotlib.image as mpimg
import numpy as np

from scipy import spatial
# example: compute pairwise Cosine distances beteen JK Rowling, QE2, Zhu, and Yao Ming
# example: X=np.vstack((reshaped_JKR, reshaped_Yao, reshaped_QE2, reshaped_Zhu))
# example: Y=spatial.distance.pdist(X, 'cosine')

import os, sys

# import csv for writing similarity data to csv file
import csv

# source directory
# use normalized images that are 100x100 pixels
src_dir="/tmp/all_celebrities"

# function to convert RGB to grey scale
def rgb2grey(rgb):
    return np.dot(rgb[...,:3],[0.299,0.587,0.144])

# function to crop the edges off
def crop(rgb):
    lx, ly = rgb.shape
    return rgb[lx/10:-lx/10,ly/10:-ly/10]

# list all directories in the source directory and save to a list of celebrity names 
# celebrity names are used as keys throughout the code
celebrity_names=os.listdir(src_dir)

# write output to a csv file
# create header fields
# celebrity: name of the celebrity
# peer: another celebrity with whom we are computing the similarity between celebrity and peer
# similarity: the Cosine distance:
# image location: the location of the image for the peer

with open('/tmp/CelebrityWatch_cropped.csv', 'w') as csvfile:
    fieldnames = ['celebrity', 'peer','similarity','image location']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    # add the header fields
    writer.writeheader()
    
    # the outer for loop through each celebrity
    for i, name in enumerate(celebrity_names):
        path=os.path.join(src_dir,name)
        # print path
        # find the headshot file path
        file_path=os.listdir(path)
        # print file_path
        
        file_location=os.path.join(path,file_path[0])
        #print name, file_path
        # print file_location
        # read the image file into headshot
        headshot=misc.imread(path + '/' + file_path[0])
        # convert to grey scale image
        headshot=rgb2grey(headshot)
        # crop image
        headshot=crop(headshot)
        # flatten to a 1D vector
        headshot=np.reshape(headshot,6400)
        
        # 2nd for loop for cosine distance calculation
        for k in range(len(celebrity_names)):
            pairing=[name + '-' + celebrity_names[k]]
            # print pairing
            # find the pairing headshot location
            path=os.path.join(src_dir,celebrity_names[k])
            # print path
            # find the headshot file path
            file_path=os.listdir(path)
            # print file_path
            pairing_headshot=misc.imread(path + '/' + file_path[0])
            # convert to grey scale
            pairing_headshot=rgb2grey(pairing_headshot)
            # crop image
            pairing_headshot=crop(pairing_headshot)
            # flatten to 1D array
            pairing_headshot=np.reshape(pairing_headshot,6400)
            # stack two vectors together to form X
            X=np.vstack((headshot, pairing_headshot))
            # compute cosine distance between the pairing
            Y=spatial.distance.pdist(X, 'cosine')
            # print pairing, Y
            writer.writerow({'celebrity': name, 'peer': celebrity_names[k], 'similarity': Y[0], 'image location': path + '/' + file_path[0]}
