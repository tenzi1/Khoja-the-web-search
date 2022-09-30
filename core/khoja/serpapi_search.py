""" module implementing search functionality using google serpapi"""

import requests
import json

def read_serpapi_key():
    """loads api key from serapapi.key"""
    serpapi_key = None
    try:
        with open('serpapi.key', 'r') as f:
            serpapi_key = f.readline().strip()
    except:
        raise IOError('serpapi.key file not found')

    if not serpapi_key:
        raise KeyError('Serpapi key not found')

    return serpapi_key


def run_query(search_terms):
    serpapi_key = read_serpapi_key()
    search_url = 'https://serpapi.com/search'
    params = {'q':search_terms,
              'engine':'google',
              'api_key':serpapi_key,
              }
    
    #Issue request with above detail
    response = requests.get(search_url,params=params)
    response.raise_for_status()
    search_results = response.json()

    results = []
    for result in search_results['organic_results']:
        results.append({
            'title': result['title'],
            'link': result['link'],
            'summary': result['snippet']
        })
    return results

# search_p = input('Enter your search query... \n' )
# results = run_query(search_p)
# print("Here are the results: \n", results)

def main():
    if __name__ ==  'main':
        main()
