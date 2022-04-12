import requests
import json

url = "https://university-college-list-and-rankings.p.rapidapi.com/api/universities"

querystring = {"countryCode":"us"}

headers = {
    'x-rapidapi-host': "university-college-list-and-rankings.p.rapidapi.com",
    'x-rapidapi-key': "bf22da12a2msh194c57441388688p152f83jsn1847770e4679"
    }



response = requests.request("GET", url, headers=headers, params=querystring)
data = response.json()
dumped_json_cache = json.dumps(data)
fh = open("university_cache.json", "w")
fh.write(dumped_json_cache)
fh.close()
