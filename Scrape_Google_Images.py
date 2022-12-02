#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created: 28Nov2022

Author: Lynn Menchaca

Resources:
    Hutson-Hacks -> Automating Google Chrome to Scrape Images with Selenium and Python
    https://www.youtube.com/watch?v=7KhuEsq-I8o
    
At the end to install the requitements.txt code directory folder:
    pip install -r requirments.txt
    
    
The purpose of this file is to create a webscraper to scrape character images 
from the TV show The Simpsons.
    
    
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import requests
import io
from datetime import datetime as dt
from PIL import Image
import time
import os

driver_path = r'/Users/lynnpowell/Documents/Drivers/chromedriver.exe'
image_file_path = '/Users/lynnpowell/Documents/DS_Projects/Data_Files/Simpson_Images/'


#Had a lot of problems with webdriver finding chrom driver executable path

# Driver for Chrome = ChromeDriver
#chromedriver.chromium.org/downloads
#chrome version -> 108

#executable_path points to the chrome driver path on desktop.
#options = webdriver.ChromeOptions()
#driver = webdriver.Chrome(executable_path=driver_path, options=options)
#driver.set_window_size(1120, 1000)

#options = webdriver.ChromeOptions()
#options.add_argument('user-agent = Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.71 Safari/537.36')
#driver = webdriver.Chrome(executable_path=driver_path, options=options)

#driver = webdriver.Chrome(executable_path = driver_path)

#s = Service(driver_path)
#driver = webdriver.Chrome(service = s)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.set_window_size(1120, 1000)

# Function to get and list of image urls from google
#First step scroll across the page and grab images left to right on horizontal line
#Second step scroll down, then repeat step 1. Do for whole page
def get_google_images(driver, delay, max_images, url):
    #function to scroll down the page
    def scroll_down(driver):
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(delay)
        
    url = url
    driver.get(url)
    
    #set is an ordered list without duplicates
    image_urls = set()
    #iterator
    skips = 0
    
    while len(image_urls) + skips < max_images:
        scroll_down(driver)
        #class name -> jsname for each image (just the thumbnail)
        thumbnails = driver.find_elements(By.CLASS_NAME, 'Q4LuWd')

        for img in thumbnails[len(image_urls) + skips:max_images]:
            #try clicking the image 
            #if fail continue on (to avoid breaking the loop)
            try:
                img.click()
                time.sleep(delay)
            except:
                continue
            
            #class name -> class for each image (actual image (post click))
            #source the image url link to later download the image
            images = driver.find_elements(By.CLASS_NAME, 'n3VNCb')
            for image in images:
                if image.get_attribute('src') in image_urls:
                    max_images += 1
                    skips += 1
                    break
                
                if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                    image_urls.add(image.get_attribute('src'))
                    
    return image_urls


# Function to download images
def download_image(down_path, url, file_name, image_type='JPEG', verbose=True):
    try:
        time = dt.now()
        curr_time = time.strftime('%H:%M:%S')
        #get image content
        image_content = requests.get(url).content
        #get the IO output byte
        img_file = io.BytesIO(image_content)
        #Store the file in memory and
        #convert to an image ffile iwth the PIL (pillow package)
        image = Image.open(img_file)
        full_path = down_path + file_name
        
        #save the image
        with open(full_path, 'wb') as file:
            image.save(file, image_type)
            
        if verbose == True:
            #print(f'The image: {full_path} donwloaded succesfully at {curr_time}')
            print('The image: {} donwloaded succesfully at {}'.format(full_path, curr_time))
    except Exception as e:
        #print(f'Unable to download image from Google using driver due to:\n: {str(e)}')
        print('Unable to download image due to: ', e)


if __name__ == '__main__':
    # google phots url - Homer Simpson
    google_urls = [
        'https://www.google.com/search?q=Homer+Simpson&tbm=isch&ved=2ahUKEwi4trPzo9b7AhWBnVMKHc6_DY4Q2-cCegQIABAA&oq=Homer+Simpson&gs_lcp=CgNpbWcQAzIECCMQJzIECCMQJzIHCAAQsQMQQzIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIECAAQQzoICAAQgAQQsQNQsghY3hhgvSNoAHAAeAGAAdACiAHRCZIBCDEyLjEuMC4xmAEAoAEBqgELZ3dzLXdpei1pbWfAAQE&sclient=img&ei=yn6HY7ipHIG7zgLO_7bwCA&bih=684&biw=1378',
        'https://www.google.com/search?q=Magre+Simpson&tbm=isch&ved=2ahUKEwiM-rWFpdb7AhUUad8KHXViB3wQ2-cCegQIABAA&oq=Magre+Simpson&gs_lcp=CgNpbWcQAzoECCMQJzoFCAAQgAQ6BAgAEEM6BggAEAcQHjoICAAQCBAHEB5QoQlYzA9g4hxoAHAAeACAAVSIAZMDkgEBNpgBAKABAaoBC2d3cy13aXotaW1nwAEB&sclient=img&ei=_H-HY4yMKpTS_Qb1xJ3gBw&bih=684&biw=1378',
        'https://www.google.com/search?q=Bart+Simpson&tbm=isch&ved=2ahUKEwj865ydpdb7AhUfoYQIHZ3ADi4Q2-cCegQIABAA&oq=Bart+Simpson&gs_lcp=CgNpbWcQAzIHCAAQsQMQQzIECAAQQzIFCAAQgAQyBAgAEEMyBQgAEIAEMgUIABCABDIECAAQQzIFCAAQgAQyBQgAEIAEMgUIABCABDoECCMQJzoGCAAQBxAeUP8KWNMOYIUdaABwAHgAgAFZiAHSApIBATWYAQCgAQGqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=LoCHY_ycJZ_CkvQPnYG78AI&bih=684&biw=1378',
        'https://www.google.com/search?q=Lisa+Simpson&tbm=isch&ved=2ahUKEwiY2ryjpdb7AhV2azABHTQlAVMQ2-cCegQIABAA&oq=Lisa+Simpson&gs_lcp=CgNpbWcQAzIFCAAQgAQyBAgAEEMyBAgAEEMyBQgAEIAEMgQIABBDMgUIABCABDIECAAQQzIFCAAQgAQyBQgAEIAEMgUIABCABDoECCMQJzoGCAAQBxAeUPEJWIAPYO8TaABwAHgAgAFLiAHZApIBATWYAQCgAQGqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=O4CHY9jQK_bWwbkPtMqEmAU&bih=684&biw=1378',
        'https://www.google.com/search?q=Maggie+Simpson&tbm=isch&ved=2ahUKEwjwmJ6spdb7AhUslYQIHbngANUQ2-cCegQIABAA&oq=Maggie+Simpson&gs_lcp=CgNpbWcQAzIECAAQQzIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBAgAEEMyBQgAEIAEOgQIIxAnOgYIABAHEB5QhAdYvhBg1hJoAHAAeACAAV6IAc8DkgEBN5gBAKABAaoBC2d3cy13aXotaW1nwAEB&sclient=img&ei=ToCHY_C5BayqkvQPucGDqA0&bih=684&biw=1378'
        ]

    # label
    labels = ['homer_simpson', 'marge_simpson', 'bart_simpson', 'lisa_simpson', 'maggie_simpson']
    
    #check the lenght of labels match our url
    if len(google_urls) != len(labels):
        raise ValueError('The lenght of the url list does not match th elabels list.')

    # Make directory if it doesn't exist
    for label in labels:
        if not os.path.exists(image_file_path + label):
            print('Making Directory: ', label)
            os.makedirs(image_file_path + label)
            
    #loop through the google urls and labels list and get the images
    #total number of examples is 100 -> set max_imgaes = 100
    for url_current, label in zip(google_urls, labels):
        urls = get_google_images(driver=driver, delay=0.2, max_images=100, url=url_current)
        
        for idx, url in enumerate(urls):
            download_path = image_file_path + label + '/'
            download_image(down_path=download_path,
                           url = url,
                           file_name=str(idx+1)+'.jpg',
                           verbose=True)
            
    # kill web driver
    driver.quit()






