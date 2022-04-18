from operator import itemgetter
import requests
import json
import datetime
import random
from flask import Flask

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
    def __init__(self, name="No Name", ranking="No Ranking", address = "No address"):
            self.name = name
            self.ranking = ranking
            self.address = address
    def insert_address(self, address):
        self.address = address


class BSTNode:
    def __init__(self, item=None):
        self.left = None
        self.right = None
        self.item = item

    #compare ranking value, then insert the object
    def insert(self, item):
        if not self.item:
            self.item = item
            return

        if self.item == item:
            return

        if item.ranking < self.item.ranking:
            if self.left:
                self.left.insert(item)
                return
            self.left = BSTNode(item)
            return

        if self.right:
            self.right.insert(item)
            return
        self.right = BSTNode(item)

    # Print the data in tree inorder
    def inorder(self, item_list):
        if self.left is not None:
            self.left.inorder(item_list)
        if self.item is not None:
            item_list.append(self.item)
        if self.right is not None:
            self.right.inorder(item_list)
        return item_list

    def preorder(self, vals):
        if self.item is not None:
            vals.append(self.item.ranking)
        if self.left is not None:
            self.left.inorder(vals)
        if self.right is not None:
            self.right.inorder(vals)
        return vals

    def postorder(self, vals):
        if self.left is not None:
            self.left.inorder(vals)
        if self.right is not None:
            self.right.inorder(vals)
        if self.item is not None:
            vals.append(self.item.ranking)
        return vals

def retrive_address(university_name):
    '''This function takes a university name and look up address information'''
    api_key = "AIzaSyDxf3NYCxsgiKIVtkwgWxGF0kBqL6Sen4E"
    serviceurl = "https://maps.googleapis.com/maps/api/geocode/json?"

    parms = dict()
    parms["address"] = university_name
    parms['key'] = api_key
    response = requests.request("GET", serviceurl, params=parms)
    data = response.json()
    if data['status'] == "OK":
        address = data["results"][0]["formatted_address"]
    else:
        address = "No address info"
    return address


rapidAPI_data = None

#This block of code will ask the user for a country code to look up university rankings of a specific country
print("Welcome to the University Search Tool.\n")
COUNTRY_CODE = input("Please input the 2-digit country you would like to do your search in: ")
CACHE_FILENAME = "cache_" + COUNTRY_CODE.lower() +".json"
temp_dict = dict()
counter = 0

try:
    DATA_CACHE = open_cache(CACHE_FILENAME)  #If there is a cache for specified country, use it
    print("\nPulling data from cache...\n")
except:
    print("\nPulling data from the Web API...\n")  #Otherwise, pull data from the Web API and create cache for the specified country
    print("This may take a moment... Please be patient.\n")
    while True:
        if COUNTRY_CODE == "exit":
            print("\nGoodbye!")
            exit()
        rapidAPI_data = request_data(COUNTRY_CODE)
        if rapidAPI_data != None:
            for rank, u_name in rapidAPI_data.items():
                address = retrive_address(u_name)
                temp_dict[u_name] = [rank, address]
                counter += 1
                if counter % 100 == 0:
                    print("100 inquiries retrieved. Retrieving more...")
            CACHE_FILENAME = "cache_" + COUNTRY_CODE +".json"
            print("Saving data to cache...\n")
            save_cache(temp_dict, CACHE_FILENAME)
            DATA_CACHE = temp_dict
            break
        COUNTRY_CODE = input('No information found or invalid country code. Please try another 2-digit code or input "exit" to quit searching: ')


#print(DATA_CACHE) #Sanity check, comment out after confirm data can be accessed correctly
#print("time used: ", (t2 - t1) * 1000, "ms") #time consumption check for checkpoint, comment out after use



universities = []
for item in DATA_CACHE.items():
    name, temp_list = item
    ranking = temp_list[0]
    address = temp_list[1]
    try:
        universities.append(University(name, int(ranking), address))
    except:
        pass

#shuffle the list to make the tree more balanced
random.shuffle(universities)
university_tree = BSTNode()

for university in universities:
    university_tree.insert(university)
#sort the universities in the order of rankings
inorder_list = university_tree.inorder([])

filter_min = input("Enter the limit of best ranking for your search: ")
filter_max = input("Enter the limit of worst ranking for your search: ")
try:
    filter_min = int(filter_min)
    filter_max = int(filter_max)
except:
    print("Invalid range. Will include all results.\n")
    filter_min = 1
    filter_max = 999999

user_resp = input("Would you like detailed addresses attachted? ")
yes_list = ['yes', 'y', 'yup', 'yep' 'yeah', 'sure', 'of course', 'definitely', 'certainly']
if user_resp in yes_list:
    address_flag = True
else:
    address_flag = False

filtered_list = []
for univeristy in inorder_list:
    if univeristy.ranking >= filter_min and univeristy.ranking <= filter_max:
        filtered_list.append(univeristy)

app = Flask(__name__)

@app.route('/')
def index():     
    if address_flag is True:
        html_static ='''
        <style>
        table, th, td {
            border:1px solid black;
        }
        </style>
        <h1>Here are the results of your search</h1>
        <table style="width:100%">
            <tr>
                <th>Ranking</th>
                <th>University</th>
                <th>Address</th>
            </tr>
        '''
        html_dynamic = ''
        for item in filtered_list:
            name = item.name
            ranking = item.ranking
            address = item.address
            html_dynamic = html_dynamic + f'''
            <tr>
                <td>{ranking}</td>
                <td>{name}</td>
                <td>{address}</td>
            </tr>
                '''
    else:
        html_static ='''
        <style>
        table, th, td {
            border:1px solid black;
        }
        </style>
        <h1>Here are the results of your search</h1>
        <table style="width:50%">
            <tr>
                <th>Ranking</th>
                <th>Name</th>
            </tr>
        '''
        html_dynamic = ''
        for item in filtered_list:
            name = item.name
            ranking = item.ranking
            address = item.address
            html_dynamic = html_dynamic + f'''
            <tr>
                <td>{ranking}</td>
                <td>{name}</td>
            </tr>
                '''
    end_table = '</table>'
    return html_static + html_dynamic +end_table


print('starting Flask app', app.name)  
app.run(debug=True, use_reloader=False)






