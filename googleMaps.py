from requests import post, get
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GM_KEY")
print(API_KEY)

def searchPlace(query, lat, long):
    url = "https://places.googleapis.com/v1/places:searchText"
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': API_KEY,
        'X-Goog-FieldMask': 'places.displayName,places.id'
    }
    data = {
        'textQuery': query,
        'locationBias': {
            'circle': {
                'center': {
                    'latitude': lat,
                    'longitude': long
                },
                'radius': 5000
            }
        },
        'rankPreference': 'RELEVANCE'
    }
    response = post(url, json=data, headers=headers)
    return response.text
