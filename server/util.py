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
    
convert image to base64:
    - https://www.base64-image.de/
    - drag and drop image
    - copy image
    - paste and save as .txt file

"""
import cv2
import joblib
import json
import numpy as np
import base64
import pywt
from matplotlib import pyplot as plt


#File paths
data_file = '/Users/lynnpowell/Documents/DS_Projects/Data_Files/'
model_path = '/Users/lynnpowell/Documents/DS_Projects/Simpson_Classifier/server/artifacts/'



#variables
__class_name_to_number = {}
__class_number_to_name = {}
__model = None


#wavelet transformation function
def w2d(img, mode='haar', level=1):
    imArray = img
    #Datatype conversions
    #convert to grayscale
    imArray = cv2.cvtColor( imArray,cv2.COLOR_RGB2GRAY )
    #convert to float
    imArray =  np.float32(imArray)   
    imArray /= 255;
    # compute coefficients 
    coeffs=pywt.wavedec2(imArray, mode, level=level)

    #Process Coefficients
    coeffs_H=list(coeffs)  
    coeffs_H[0] *= 0;  

    # reconstruction
    imArray_H=pywt.waverec2(coeffs_H, mode);
    imArray_H *= 255;
    imArray_H =  np.uint8(imArray_H)

    return imArray_H

#Load Model
def load_model():
    print('Loading Model')
    global __class_name_to_number
    global __class_number_to_name
    
    with open(model_path + 'class_dictionary.json', 'r') as f:
        __class_name_to_number = json.load(f)
        __class_number_to_name = {v:k for k,v in __class_name_to_number.items()}
        
    global __model
    if __model is None:
        #using the SVM model
        with open(model_path + 'svm_model.pkl', 'rb') as f:
        #using the SVM model
        #with open(model_path + 'logr_model.pkl', 'rb') as f:
            __model = joblib.load(f)
    print('Finished Loading Model')



#classify image, can pass image file path
def classify_image(image_base64_data, file_path=None):
    #print(file_path)
    imgs = cropped_image(file_path, image_base64_data)
    
    results = []
    
    for img in imgs:
        #scale images to a uniform size
        scalled_raw_img = cv2.resize(img, (32,32))
        #wavelet transformed image
        img_har = w2d(img, 'db1', 5)
        #scale images to a uniform size
        scalled_img_har = cv2.resize(img_har, (32,32))
        #stacking images using numpy
        combine_img = np.vstack((scalled_raw_img.reshape(32*32*3,1), scalled_img_har.reshape(32*32,1)))
        
        len_img_array = 32*32*3+32*32
        
        final = combine_img.reshape(1, len_img_array).astype(float)
        
        #results.append(__model.predict(final)[0])
        #print(class_number_to_name(__model.predict(final)[0]))
        results.append({
            'class' : class_number_to_name(__model.predict(final)[0]),
            'class_probability' : np.round(__model.predict_proba(final) * 100, 2).tolist()[0],
            'class_dictionary' : __class_name_to_number
            })
        
        
    return results


#get the base64 string from image
def b64_string_from_image(b64str):
    encoded_data = b64str.split(',')[1]
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img



#fuction to find the cropped face of the photo
def cropped_image(image_path, image_base64_data):
    face_cascade = cv2.CascadeClassifier(data_file + 'simpson_cascade/cascade.xml')
    
    if image_path:
        img = cv2.imread(image_path)
    else:
        img = b64_string_from_image(image_base64_data)
    
    #print(img)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    face_detect = face_cascade.detectMultiScale(gray, 1.3, 5)
    #print(face_detect)
    (x,y,w,h) = face_detect[0]
    
    cropped_face = []
    
    """
    for (x,y,w,h) in face_detect:
        face_img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = face_img[y:y+h, x:x+w]
        cropped_face.append(roi_color)
        
        #face_img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

        plt.imshow(roi_color)
        plt.show()
    """
    
    face_img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = face_img[y:y+h, x:x+w]
    
    #To verify the face is identified in the photo
    plt.imshow(roi_color)
    plt.show()
    
    cropped_face.append(roi_color)
        
    return cropped_face
        
    
#Convert output value from number to simpson character name
def class_number_to_name(class_num):
    return __class_number_to_name[class_num]    
    



#function to pull the base64 bart image that was manually created with the link above
def get_b64_test_image():
    #file is in the same folder as this file
    with open('bart_solo_base64.txt') as f:
        return f.read()



if __name__ == '__main__':
    #loading model
    load_model()
    
    #testing with image manually converted in to a base64
    #print(classify_image(get_b64_test_image(), None))
    
    #testing with image from folder
    #since this file is in the folder with the "test_images" folder below is the path
    print(classify_image(None, 'test_images/bart_solo.jpg'))
    print(classify_image(None, 'test_images/marge_solo.jpg'))
    print(classify_image(None, 'test_images/marge_hat_hard.jpg'))
    print(classify_image(None, 'test_images/homer_pillow_hard.jpg'))
    
    #class_number_to_name(2)


