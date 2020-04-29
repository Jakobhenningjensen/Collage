# -*- coding: utf-8 -*-
#Script which takes an image (img_in) and creates a collage of pictures from the foleder "resized_imgs"

import numpy as np
from PIL import Image #For Reading images
import pickle
from multiprocessing import Pool
from joblib import Parallel, delayed
from skimage import color
import time
import colour
import os

if __name__=="__main__":
    t=time.time()
    n_pic =-1
    col_images_list = os.listdir("Resized_imgs") #List of small images to build the collage
    img_in = Image.open("pic_in.jpg") #Big picture (to be "collaged")
    n,m = img_in.size #Size of input picture
    n_col,m_col = 28,28 #Size of the collage-images
    img_in = img_in.resize((n//n_col*n_col,m//m_col*m_col)) #Resizes
    n_new,m_new = img_in.size #size of new image

    img_out=np.array(Image.new(size=(n_new,m_new),mode="RGB")) #output image
    img_in = np.array(img_in)
    col_images_array = [color.rgb2lab(np.array(Image.open(f"Resized_imgs/{im}"))) for im in col_images_list][:n_pic]
    for j in range(n//n_col):
        for i in range(m//m_col):

                i_start,i_end,j_start,j_end = (i*n_col,(i+1)*n_col,j*m_col,(j+1)*m_col) #slize size
                slze = img_in[i_start:i_end,j_start:j_end]   #Slize of image_input
                slze = color.rgb2lab(slze)
                slze_sum = slze.mean(axis=0).mean(axis=0)

                ### Get closest image from the collage ###

                DISTS=[np.mean(color.deltaE_cmc(slze,img)) for img in col_images_array] #Calculate "differences"
                best_col = col_images_list[np.nanargmin(DISTS)]
                img_out[i_start:i_end,j_start:j_end]=np.array(Image.open(f"Resized_imgs/{best_col}"))

    print(f"Tid: {time.time()-t}")
    img_out=Image.fromarray(img_out)
    img_out.show()



