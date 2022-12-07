#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created: 02Dec2022

Author: Lynn Menchaca


Resources:
   - Youtube channel: codebasics
    Playlist: Data Science Project|Machine Learning Project|Sports Celebrity Image Classification 
    https://www.youtube.com/playlist?list=PLeo1K3hjS3uvaRHZLl-jLovIjBP14QTXc


The purpose of this file is to put my trainned model on the server.

This file performs the image classification.

"""

from flask import Flask, request, jsonify
import util

app = Flask(__name__)

#testing out my python server to say hello world
#@app.route('/hello')
#def hello():
#    return "Hello World!"


@app.route('http://192.168.1.253:5000/classify_image', methods = ['GET', 'POST'])
def classify_image():
    image_data = request.form['image_data']
    
    response = jsonify(util.classify_image(image_data))
    
    response.headers.add('Access-Control-Allow-Origin', '*')
    
    return response


if __name__ == "__main__":
    print("Starting Python Flask Server For Simpson Classification")
    util.load_model()
    app.run(port=5000)



