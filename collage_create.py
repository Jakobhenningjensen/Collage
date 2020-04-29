# -*- coding: utf-8 -*-
#Script which takes an image (img_in) and creates a collage of pictures from the foleder "resized_imgs"

import numpy as np
from PIL import Image #For Reading images
import pickle
from multiprocessing import Pool
from joblib import Parallel, delayed
from skimage import color
import os

def calc_dist(slze_in,col_in,K1=0.045,K2=0.015):
    #Returns the "distance" between the input image and the collage images

    L1 =slze_in[:,:,0]
    L2 =col_in[:,:,0]
    dL=L1-L2
    C1 = np.sqrt(slze_in[:,:,1]**2+slze_in[:,:,2]**2)
    C2 = np.sqrt(col_in[:,:,1]**2+col_in[:,:,2]**2)
    dC= C1-C2
    a1 = slze_in[:,:,1]
    a2 = col_in[:,:,1]
    b1 = slze_in[:,:,2]
    b2 = col_in[:,:,2]
    dHab=np.sqrt((a1-a2)**2+(b1-b2)**2-dC**2)    
    SC=1+K1*C1
    SH=1+K2*C1
       
    dE=np.sqrt((dL)**2+(dC/SC)**2+(dHab/SH)**2)
    return dE.mean()

if __name__=="__main__":

    col_images_list = os.listdir("Resized_imgs") #List of small images to build the collage
    img_in = Image.open("pic_in.jpg") #Big picture (to be "collaged")
    n,m = img_in.size #Size of input picture
    n_col,m_col = 28,28 #Size of the collage-images
    img_in = img_in.resize((n//n_col*n_col,m//m_col*m_col)) #Resizes
    n_new,m_new = img_in.size #size of new image

    img_out=np.array(Image.new(size=(n_new,m_new),mode="RGB")) #output image
    img_in = np.array(img_in)
    col_images_array = [color.rgb2lab(np.array(Image.open(f"Resized_imgs/{im}"))) for im in col_images_list]
    for j in range(n//n_col):
        for i in range(m//m_col):

                i_start,i_end,j_start,j_end = (i*n_col,(i+1)*n_col,j*m_col,(j+1)*m_col) #slize size
                slze = img_in[i_start:i_end,j_start:j_end]   #Slize of image_input
                slze = color.rgb2lab(slze)
                slze_sum = slze.mean(axis=0).mean(axis=0)

                ### Get closest image from the collage ###

                DISTS=[calc_dist(slze,img) for img in col_images_array] #Calculate "differences"
                best_col = col_image_list[np.argmin(DISTS)]
                img_out[i_start:i_end,j_start:j_end]=np.array(Image.open(f"Resized_imgs/{best_col}")))

    img_out=Image.fromarray(img_out)
    img_out.show()



