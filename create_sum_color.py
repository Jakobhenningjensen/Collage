#Calculates the average color of images in the folder Resized_imgs.

import numpy as np
import os
from PIL import Image #For Reading images
import pickle

images = os.listdir("Resized_imgs") #Pictures of which the input-picture is build of
sum_dict = {i:[0,0,0] for i in range(len(images))}

for i,img in enumerate(images):
    with Image.open("Resized_imgs/"+img) as im:
       sum_dict[i]= np.array(im).sum(axis=0).sum(axis=0) #Calculates the sum of each channel/color
    
pickle.dump(sum_dict,open("sum_dict.pkl","wb")) #Dump the dictionary
               