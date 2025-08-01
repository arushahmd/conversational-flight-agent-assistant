"""
    This file will contain agents and tools to get information from visadb.io api

    Explore https://tequila.kiwi.com/portal/login too the api is free for testing too.
"""

# 

import requests

API_KEY = "ad133b9f3953b303f726db10d0a84f38"
url = f"https://api.aviationstack.com/v1/flights? access_key = {API_KEY}"

response = requests.get(url)
print(response)