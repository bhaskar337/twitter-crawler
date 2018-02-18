from django.shortcuts import render, HttpResponse
from django.http import JsonResponse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import math
from textblob import TextBlob

driver = webdriver.Firefox(executable_path='geckodriver.exe')


def index(request):

	tweets = get_n_tweets(20)
	return JsonResponse(tweets, safe=False)


def get_n_tweets(n, search_str='PM MODI'):
	driver.get("http://twitter.com/search?q="+search_str+"&src=typd")
	for x in range(math.ceil(n/20)-1):	
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(5)

	try:
	    element = WebDriverWait(driver, 10).until(
	        EC.presence_of_element_located((By.CLASS_NAME, "tweet"))
	    )
	    tweets = driver.find_elements_by_class_name("tweet")

	    response = []
	    for i in tweets:
	    	response.append({'tweet' : i.text, 'score' : TextBlob(i.text).sentiment.polarity})

	    return response
	    
	finally:
		driver.quit()


