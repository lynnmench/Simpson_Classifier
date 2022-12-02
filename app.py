#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Lynn Menchaca
Date: 28Nov2022

Project: Simpson Classification

"""

"""
Resources:
    - youtube -> Krish Naik -> Live Project Playlist

The purpose of this file is to

"""



# Importing the necessary Libraries
from flask_cors import CORS,cross_origin
from flask import Flask, render_template, request,jsonify
from ImageScraper import ScrapperImage
from businesslayer.BusinessLayerUtil import BusinessLayer
import os

data_file_path = '/Users/lynnpowell/Documents/DS_Projects/Simpson_Classification/'

# import request
app = Flask(__name__) # initialising the flask app with the name 'app'

#response = 'Welcome!'


@app.route('/')  # route for redirecting to the home page
@cross_origin()
def home():
    return render_template('index.html')

@app.route('/ShowImages')
@cross_origin()
def displayImages():
    list_images=os.listdir('static')
    print(list_images)
    
    try:
        if(len(list_images)>0):
            return render_template('showImage.html',user_images=list_images)
        else:
            return "Images are not present"
    except Exception as e:
        print("No images found",e)
        return "Please try with a different search keyword"

@app.route('/searchImages',methods=['Get','POST'])
def searchImage():
    if request.method=="POST":
        search_term=request.form['keyword'] # assigning the value of the input keyword to the variable keyword
        
    else:
        print("Please enter something")
    
    imagescrapperutil=BusinessLayer ## Instantiate a object for ScrapperImage Class
    imagescrapper=ScrapperImage()
    list_images=os.listdir('static')
    imagescrapper.delete_downloaded_images(list_images)## Delete the old images before search
    
    image_name=search_term.split()
    image_name="+".join(image_name)
    
    ## We need to add the header metadata
    
    header={
        'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"
            
            }
    lst_images=imagescrapperutil.downloadImages(search_term,header)
    
    return displayImages() # redirect the control to the show images method



if __name__ == '__main__':
    #Enable debugging
    app.debug = True
    
    #to run on local machine
    app.run(host='192.168.1.253', port=8000)
    
    #to run on the cloud
    #app.run(debug=True)







