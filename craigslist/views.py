import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from requests.compat import quote_plus
from . import models
import urllib

BASE_CRAIGSLIST_URL = 'https://bangalore.craigslist.org/search/?query={}'

def home(request):
    return render(request,'craigslist/base.html')

def new_search(request):
    search = request.POST.get('search')
    print(search)
    models.Search.objects.create(search=search)
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(str(search)))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')

    post_listings = soup.find_all('li', {'class': 'result-row'})

    final_postings = []

    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')

        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'
        
        final_postings.append((post_title, post_url, post_price))


    for_front = {
        'search' : search,
        'final_postings' : final_postings,
    }
    return render(request, 'craigslist/new_search.html', for_front)