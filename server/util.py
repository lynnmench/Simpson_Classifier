#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created: 02Dec2022

Author: Lynn Menchaca


Resources:
   - Youtube channel: codebasics
    Playlist: Data Science Project|Machine Learning Project|Sports Celebrity Image Classification 
    https://www.youtube.com/playlist?list=PLeo1K3hjS3uvaRHZLl-jLovIjBP14QTXc


The purpose of this file is to send a dragged and dropped image to backend for classification.
Two methods to do this:
    1. upload image to S3 bucket and send bucket link
    2. send bit 64 end coded string -> convert image in to a string
    
google: convert image to base64
https://www.base64-image.de/
drag and drop image
copy image
paste and save as .txt file

"""


#classify image, can pass image file path
def classify_image(image_base64_data, file_path=None):
    pass


#fuction to find the cropped face of the photo



#function to pull the base64 bart image that was manually created with the link above
def get_b64_test_image():
    #file is in the same folder as this file
    with open('bart_solo_base64.txt') as f:
        return f.read()



if __name__ == '__main__':
    print(classify_image(get_b64_test_image(), None))
    



