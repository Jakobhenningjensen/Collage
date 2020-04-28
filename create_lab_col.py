"""
Script creating the LAB colors for all collage-images and storing them in "img_list"

"""


from PIL import Image #For Reading images
import numpy
import pickle
import os
import numpy as np
from skimage import color
col_folder = "Resized_imgs/" #path to collage images
imgs = os.listdir(col_folder) #All images
n,m =(28,28) #Size of collage images
img_list =np.zeros(shape=(len(imgs),n,m,3))

for i,im in enumerate(imgs):
    img_list[i]=color.rgb2lab(np.array(Image.open(col_folder+im)))

pickle.dump(img_list,open("img_list_lab","wb"))