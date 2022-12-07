#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created: 30Nov2022

Author: Lynn Menchaca


Resources:
    - Youtube channel: Learn Code By Gaming -> Training a Cascade classifier - OpenCV Object Detection in Games #8
        https://www.youtube.com/watch?v=XrCAvs9AePM
    - OpenCV - Open Source Computer Vision
        https://docs.opencv.org/3.4/dc/d88/tutorial_traincascade.html
    
Used Windows computer to create the positive text files:
https://docs.opencv.org/3.4/d3/d52/tutorial_windows_install.html
    - downloaded OpenCV -> OpenCV:Installation in Windows -> sourceforge -> 3.4.16
    - Folder with executables opencv\build\x64\vc15\bin
    
    
The purpose of this file is to create the positive and negative txt files 
to use with cascade and train out Simpson classification model.
    
    
"""


import os


image_file_path = '/Users/lynnpowell/Documents/DS_Projects/Data_Files/Simpson_Images/'

def generate_negative_homer_file():
    # open the output file for writing.
    # will overwrite all existing data in there
    with open('homer_neg.txt','w') as f:
        #loop over all the file names
        #folders = [image_file_path+'bart_simpson', ]
        no_homer_labels = ['marge_simpson', 'bart_simpson', 'lisa_simpson', 'maggie_simpson']
        #no_homer_labels = ['marge_simpson', 'bart_simpson']
        for folder in no_homer_labels:
            for filename in os.listdir(image_file_path+folder):
                f.write(image_file_path+folder+filename+'\n')


def generate_negative_img_file():
    with open('neg_image_file_lst.txt','w') as f:
        #loop over all the file names
        neg_image_folder_path = image_file_path + 'neg_image'        
        
        for filename in os.listdir(neg_image_folder_path):
            f.write(neg_image_folder_path + '/' +filename+'\n')



if __name__ == '__main__':
    
    # file is save at: /Users/lynnpowell/Documents/DS_Projects/Simpson_Classifier
    generate_negative_img_file()


