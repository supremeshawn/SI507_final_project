import requests
import json
import datetime

def request_data(country_code):
    base_url = "https://university-college-list-and-rankings.p.rapidapi.com/api/universities"
    querystring = {"countryCode": country_code.lower()}

    headers = {
        'x-rapidapi-host': "university-college-list-and-rankings.p.rapidapi.com",
        'x-rapidapi-key': "bf22da12a2msh194c57441388688p152f83jsn1847770e4679"
    }

    response = requests.request("GET", base_url, headers=headers, params=querystring)
    data = response.json()
    
    return data

def open_cache(file_name):
    ''' opens the cache file if it exists and loads the JSON into
    a dictionary, which it then returns.
    if the cache file doesn't exist, creates a new cache dictionary
    Parameters
    ----------
    None
    Returns
    -------
    The opened cache
    '''
    #try:
    cache_file = open(file_name, 'r')
    cache_contents = cache_file.read()
    cache_dict = json.loads(cache_contents)
    cache_file.close()
    #except:
        #cache_dict = {}
    return cache_dict

def save_cache(cache_dict, file_name):
    ''' saves the current state of the cache to disk
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(file_name,"w")
    fw.write(dumped_json_cache)
    fw.close() 

class University:
    def __init__(self, name="No Name", ranking="No Ranking", geo_location="No Location"):
            self.name = name
            self.ranking = ranking
            self.geo_location = geo_location

class Node:
    def __init__(self, item):
        self.left = None
        self.right = None
        self.item = item

    #compare ranking value, then insert the object
    def insert(self, item):
        if self.item:
            if item.ranking < self.item.ranking:
                if self.left is None:
                    self.left = Node(item)
                else:
                    self.left.insert(item)
            elif item.ranking > self.item.ranking:
                if self.right is None:
                    self.right = Node(item)
                else:
                    self.right.insert(item)
            else:
                self.item = item

# Print the tree
    def PrintTree(self):
        if self.left:
            self.left.PrintTree()
        print( self.data),
        if self.right:
            self.right.PrintTree()



data = None

#This block of code will ask the user for a country code to look up university rankings of a specific country
COUNTRY_CODE = input("Please input the 2-digit country you would like to do your search in: ")
CACHE_FILENAME = "cache_" + COUNTRY_CODE.lower() +".json"
t1 = datetime.datetime.now().timestamp()
try:
    DATA_CACHE = open_cache(CACHE_FILENAME)  #If there is a cache for specified country, use it
    print("\nPulling data from cache...\n")
except:
    print("\nPulling data from the Web API...\n")  #Otherwise, pull data from the Web API and create cache for the specified country
    while True:
        if COUNTRY_CODE == "exit":
            print("\nGoodbye!")
            exit()
        data = request_data(COUNTRY_CODE)
        if data != None:
            CACHE_FILENAME = "cache_" + COUNTRY_CODE +".json"
            print("Saving data to cache...")
            save_cache(data, CACHE_FILENAME)
            DATA_CACHE = data
            break
        COUNTRY_CODE = input('No information found or invalid country code. Please try another 2-digit code or input "exit" to quit searching: ')

t2 = datetime.datetime.now().timestamp()
#print(DATA_CACHE) #Sanity check, comment out after confirm data can be accessed correctly
#print("time used: ", (t2 - t1) * 1000, "ms") #time consumption check for checkpoint, comment out after use

universities = []
for key, value in DATA_CACHE.items():
    try:
        universities.append(University(value, int(key)))
    except:
        pass

for university in universities:
    print(university.name, university.ranking)







#dumped_json_cache = json.dumps(data)
#fh = open("university_cache.json", "w")
#fh.write(dumped_json_cache)
#fh.close()
