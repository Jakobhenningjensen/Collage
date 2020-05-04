# -*- coding: utf-8 -*-
#Script which takes an image (img_in) and creates a collage of pictures from the foleder "resized_imgs"
import numpy as np
from PIL import Image #For Reading images
from skimage import color
import os
from multiprocessing import Pool,Manager
from itertools import product
import ctypes


class Collage():
    def __init__(self,img_in_path,col_images_path,n_pic):
        
        
        self.img_in = Image.open(img_in_path) #loads input images

        n_in,m_in = self.img_in.size #Size of input picture

        self.n_col,self.m_col = 28,28 #Size of the collage-images

        self.img_in = self.img_in.resize((n_in//self.n_col*self.n_col,m_in//self.m_col*self.m_col)) #Resize the input image (crop)
        n_new,m_new = self.img_in.size #size of new (resized) image

        self.img_out=np.array(Image.new(size=(n_new,m_new),mode="RGB")) #output image

        col_images_list = os.listdir(col_images_path)
        self.col_images_array = [color.rgb2lab(np.array(Image.open(f"{col_images_path}/{im}"))) for im in col_images_list][:n_pic]
        manager = Manager()
        self.img_in=manager.Array(ctypes.c_double)
        self.img_in.np.array(self.img_in))
        self.n_new,self.m_new = n_new,m_new
    

    def __create_col__(self,i,j):
        i_start,i_end,j_start,j_end = (i*self.n_col,(i+1)*self.n_col,j*self.m_col,(j+1)*self.m_col)
        slze = self.img_in[i_start:i_end,j_start:j_end]
        slze = color.rgb2lab(slze)
        DISTS=[np.mean(color.deltaE_cmc(slze,img)) for img in self.col_images_array]#Calculate "differences"
        best_col = np.nanargmin(DISTS)
        self.img_out[i_start:i_end,j_start:j_end]=self.col_images_array[best_col]




    def fit(self):

        I = range(self.m_new//self.m_col)
        J = range(self.n_new//self.n_col)
        
        for j in J:
            for i in I:
                self.__create_col__(i,j,self.n_col,self.m_col)

        self.img_out=Image.fromarray(self.img_out)
        self.img_out.show()



if __name__=="__main__":
    img_in_path = "pic_in.jpg"
    col_images_path = "Resized_imgs/"
    col=Collage(img_in_path=img_in_path,col_images_path=col_images_path,n_pic=10)
    col.fit()