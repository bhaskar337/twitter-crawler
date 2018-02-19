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
    return render(request, 'crawl/index.html')


def search(request):

    if request.method == 'GET':
        q = request.GET.get('q')
        tweets = get_n_tweets(60, q)
        return render(request, 'crawl/result.html', {'tweets': tweets})

    else:
        return HttpResponse('You must send a GET request only')


def get_n_tweets(n, search_str='PM MODI'):

    driver.get("http://twitter.com/search?q=" + search_str + "&src=typd")
    for x in range(math.ceil(n / 20) - 1):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "tweet"))
        )
        e_tweets = driver.find_elements_by_class_name("tweet")

        response = []
        for e_tweet in e_tweets:
            e_fullname = e_tweet.find_element_by_class_name('fullname')
            e_tweet_text = e_tweet.find_element_by_class_name('tweet-text')
            
            score = TextBlob(e_tweet_text.text).sentiment.polarity
            response.append({'by': e_fullname.text,
                             'tweet': e_tweet_text.text,
                             'score': round(score, 2)})

        return response

    finally:
        print('exit()')
