from distutils.command import check
import requests
import json
import random


### EDIT HERE
blu_api_key = "INSERT BLU API KEY"
aither_api_key = "INSERT AITHER API KEY"
iterations = 30
###

blu_url = "https://blutopia.cc/api/torrents/filter"
aither_url = "https://aither.cc/api/torrents/filter"

blu_headers = {
  'Authorization': f'Bearer {blu_api_key}',
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}

aither_headers = {
  'Authorization': f'Bearer {aither_api_key}',
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}

for i in range(0, iterations):
    params = {
        'tmdbId' : random.randint(0, 999999)
    }
    blu_response = requests.request('GET', blu_url, headers=blu_headers, params = params)
    aither_response =  requests.request('GET', aither_url, headers=aither_headers, params = params)
    blu_response = blu_response.json()
    aither_response = aither_response.json()
    try:
        if (len(blu_response['data']) == 0 and len(aither_response['data']) != 0):
            movie_name = aither_response['data'][0]['attributes']['name']
            print(movie_name)
    except:
        if ('message' in blu_response):
            print(blu_response['message'])

