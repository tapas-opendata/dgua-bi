#!/usr/bin/env python
# coding: utf-8

# In[6]:


import json
import requests
import time
import itertools
from tqdm import tqdm


# ##  #1 Retrive packages
# This script retrieves packages metadata from data.gov.ua and saves it locally in **packages.json**.

# In[1]:


# get package identifiers, generate URLs
package_list = requests.get("https://data.gov.ua/api/3/action/package_list").json()["result"]
package_list = ["https://data.gov.ua/api/3/action/package_show?id={}".format(i) for i in package_list]

# get packages matadata
packages = []
for i in tqdm(package_list):
    r = requests.get(i).json()
    packages.append(r)
    time.sleep(0.01)

# get result
packages = [i["result"] for i in packages if i["success"] == True]
    
# save copy of JSON locally
with open('data/packages.json', 'w') as outfile:
    json.dump(packages, outfile, ensure_ascii=False)


# ## #2 Datastore API availability
# This script retrieves additional properties of resources from CKAN Datastore API and saves it locally in **resource_samples.json**.

# In[2]:


# get ids of resources
resources = [i["resources"] for i in packages]
resources = list(itertools.chain(*resources))
resource_id = [i["id"] for i in resources]

# generate list of URLs
resource_list = ["https://data.gov.ua/api/3/action/datastore_search?resource_id={}&limit=1".format(i) for i in resource_id]
resource_samples = []
for i in tqdm(resource_list):
    r = requests.get(i).json()
    resource_samples.append(r)
    time.sleep(0.01)

# save copy of JSON locally
with open('data/resource_samples.json', 'w') as outfile:
    json.dump(resource_samples, outfile, ensure_ascii=False)

