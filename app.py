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
#from scrapperImage.ScrapperImage import ScrapperImage
#from businesslayer.BusinessLayerUtil import BusinessLayer
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





if __name__ == '__main__':
    #Enable debugging
    app.debug = True
    
    #to run on local machine
    app.run(host='192.168.1.253', port=8000)
    
    #to run on the cloud
    #app.run(debug=True)







