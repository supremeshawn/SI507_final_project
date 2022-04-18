class University:
    def __init__(self, name="No Name", ranking="No Ranking", address = "No address"):
            self.name = name
            self.ranking = ranking
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
    cache_file = open(file_name, 'r')
    cache_contents = cache_file.read()
    cache_dict = json.loads(cache_contents)
    cache_file.close()
    return cache_dict


DATA_CACHE = open_cache("cache__us.json")
universities = []
for item in DATA_CACHE.items():
    name, temp_list = item
    ranking = temp_list[0]
    address = temp_list[1]
    try:
        universities.append(University(name, int(ranking), address))
    except:
        pass

#Here tree nodes are inserted to make a complete tree
university_tree = BSTNode()
for university in universities:
    university_tree.insert(university)