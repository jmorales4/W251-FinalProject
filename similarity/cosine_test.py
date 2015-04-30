# use the reduced data set in aligned_images_DB
from scipy import misc
import matplotlib.image as mpimg
import numpy as np
# from matplotlib import *
JKR=misc.imread("/data/YouTubeFaces/YouTubeFaces/aligned_images_DB/JK_Rowling/2/aligned_detect_2.583.jpg")
Yao=misc.imread("/data/YouTubeFaces/YouTubeFaces/aligned_images_DB/Yao_Ming/3/aligned_detect_3.469.jpg")
QE2=misc.imread("/data/YouTubeFaces/YouTubeFaces/aligned_images_DB/Queen_Elizabeth_II/3/aligned_detect_3.8011.jpg")
Zhu=misc.imread("/data/YouTubeFaces/YouTubeFaces/aligned_images_DB/Zhu_Rongji/0/aligned_detect_0.730.jpg")

# rescale RGB 
def rescale(rgb):
    return rgb/255.

print "sizes of the sample images" 
print shape(JKR), shape(Yao), shape(QE2), shape(Zhu)

JKR=rescale(JKR)
Yao=rescale(Yao)
QE2=rescale(QE2)
Zhu=rescale(Zhu)



# function to convert RGB to grey scale
def rgb2grey(rgb):
    return np.dot(rgb[...,:3],[0.299,0.587,0.144])

# weighted average to get greyscale right
def weightedAverage(pixel):
    return 0.299*pixel[0] + 0.587*pixel[1] + 0.114*pixel[2]


# grey = np.zeros((JKR.shape[0], JKR.shape[1])) # init 2D numpy array

# convert to gray scale
JKR_grey=rgb2grey(JKR)
Yao_grey=rgb2grey(Yao)
QE2_grey=rgb2grey(QE2)
Zhu_grey=rgb2grey(Zhu)

# get a sense of scales
print "max pixel value", np.amax(JKR_grey), np.amax(Yao_grey), np.amax(QE2_grey), np.amax(Zhu_grey)
print "min pixel value", np.amin(JKR_grey), np.amin(Yao_grey), np.amin(QE2_grey), np.amin(Zhu_grey)

# def normalize
def normal(grey):
    return grey/np.amax(grey)

JKR_norm=normal(JKR_grey)
Yao_norm=normal(Yao_grey)
QE2_norm=normal(QE2_grey)
Zhu_norm=normal(Zhu_grey)

# get row number
for rownum in range(len(JKR)):
   for colnum in range(len(JKR[rownum])):
      JKR_grey[rownum][colnum] = weightedAverage(JKR[rownum][colnum])
                                     


print shape(JKR_grey)

# plt.subplot(151)
# plt.imshow(JKR)
plt.subplot(151)
plt.imshow(JKR_norm, cmap = matplotlib.cm.Greys_r)
# plt.imshow(JKR[:,:,0])
# plt.imshow(JKR)

# resize image
size=(100,100)
resized_JKR=misc.imresize(JKR_norm,size)
print shape(resized_JKR)
plt.subplot(152)
plt.imshow(resized_JKR, cmap = matplotlib.cm.Greys_r)

#  print resized
reshaped_JKR=np.reshape(resized_JKR, 10000)
print reshaped_JKR

resized_Yao=misc.imresize(Yao_norm,size)

reshaped_Yao=np.reshape(resized_Yao,10000)
print reshaped_Yao
plt.subplot(153)
plt.imshow(resized_Yao, cmap = matplotlib.cm.Greys_r)

resized_QE2=misc.imresize(QE2_norm,size)

reshaped_QE2=np.reshape(resized_QE2,10000)
print reshaped_QE2
plt.subplot(154)
plt.imshow(resized_QE2, cmap = matplotlib.cm.Greys_r)

resized_Zhu=misc.imresize(Zhu_norm,size)

reshaped_Zhu=np.reshape(resized_Zhu,10000)
print reshaped_Zhu
plt.subplot(155)
plt.imshow(resized_Zhu, cmap = matplotlib.cm.Greys_r)


# compute cosine distances
from scipy import spatial
# stack JKR and Yao and QE2
X=np.vstack((reshaped_JKR, reshaped_Yao, reshaped_QE2, reshaped_Zhu))
Y=spatial.distance.pdist(X, 'cosine')
print Y
Z=['JKR-Yao','JKR-QE2','JKR-Zhu','Yao-QE2','Yao-Zhu','QE2-Zhu']
print Z
Y1=spatial.distance.pdist(X[:-1,], 'cosine')
print Y1


