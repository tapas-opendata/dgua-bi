#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import itertools
import re
import pandas as pd


# In[2]:


# open local copy
with open('data/resource_samples.json') as json_file:
    resource_samples = json.load(json_file)


# ## #1. Subset values of dicts in arrays

# In[3]:


# filter successful results
datastore_result_filt = [i["result"] for i in resource_samples if "result" in i]
# subset properties
datastore_result_resource_id = [i["resource_id"] for i in datastore_result_filt]
datastore_result_fields = [i["fields"] for i in datastore_result_filt]
datastore_result_fields_len = [len(i["fields"]) for i in datastore_result_filt]
# unnest fields
fields = list(itertools.chain(*datastore_result_fields))
field_type = [i["type"] for i in fields]
field_id = [i["id"] for i in fields]
field_len = [len(i["id"]) for i in fields]

# in the case of exceeded data rate limit relaunch Jupiter with parameter: jupyter notebook --NotebookApp.iopub_data_rate_limit=10000000000

# create an array of resources identifier with equal length to fields
field_resource_id = []

for i, l in zip(datastore_result_resource_id, datastore_result_fields_len):
    field_resource_id.append(list(itertools.repeat(i, l)))
    
field_resource_id = list(itertools.chain(*field_resource_id))

# create API request
field_url = []

for fi, ri in zip(field_id, field_resource_id):
    field_url.append("https://data.gov.ua/api/3/action/datastore_search_sql?sql=SELECT \"{}\" from \"{}\"".format(fi, ri))
    


# ## #2. Attribute names parsing
# This code parses attributes and returns error types.

# In[4]:


# match system identifier
sys_id = re.compile('^_id$')
# match system column indexes
sys_columns = re.compile('^\d+_$')
# match numbers and codes
code = re.compile('^\d+$|^\d+\.\d+$')
# match camelCase or snake_case
correct_name = re.compile('^[a-zA-Z]{2}[a-zA-Z0-9_]*$')
# match cyrillic with spaces
incorrect_name = re.compile('[А-яІіЇїЄєҐґ]+')

field_status = []
field_status_code = []


for i in field_id:
    if code.match(i) != None:
        field_status.append("Номер або числовий код")
        field_status_code.append(0)
    elif sys_id.match(i) != None:
        field_status.append("Системний ідентифікатор")
        field_status_code.append(0)
    elif sys_columns.match(i) != None:
        field_status.append("Назви атрибутів нерозпізнані: присвоєно системні індекси")
        field_status_code.append(0)
    elif correct_name.match(i) != None:
        field_status.append("Рекомендоване оформлення (camelCase або snake_case)")
        field_status_code.append(1)
    elif incorrect_name.match(i) != None:
        field_status.append("Кирилиця у назвах атрибутів")
        field_status_code.append(0)
    else:
        field_status.append("Інші помилки")
        field_status_code.append(0)


# In[5]:


# create and save df
field_df = pd.DataFrame({"id": field_id,
                         "type": field_type,
                         "status": field_status,
                         "status_code":field_status_code,
                         "len": field_len,
                         "url": field_url,
                         "resource_id": field_resource_id})


# ## #3. Add aditional metadata

# In[6]:


# (3.1.) upload packages_df and resources_df
resources_df = pd.read_csv("data/resources.csv")
packages_df = pd.read_csv("data/packages.csv")

# (3.2.) add package_id
field_df = pd.merge(field_df, resources_df[["id", "package_id", "name"]],
                  left_on = "resource_id", right_on = "id", how = "left", suffixes= ("_field", "_resource"))
# rename columns
field_df = field_df.rename(index=str, columns={"id_field": "id",
                                              "name":"resource_name"})
# drop doubling id
field_df = field_df.drop(["id_resource"], axis=1)


# (3.3.) add package metadata
field_df = pd.merge(field_df, packages_df[["id", "title", "organization_title", "organization_name"]],
                  left_on = "package_id", right_on = "id", how = "left", suffixes= ("_field", "_package"))
# rename columns
field_df = field_df.rename(index=str, columns={"id_field": "id",
                                               "title": "package_title"})
# drop doubling id
field_df = field_df.drop(["id_package"], axis=1)

# save df
field_df.to_csv("data/fields.csv", index=False)

