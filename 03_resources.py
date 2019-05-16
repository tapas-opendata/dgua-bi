#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import itertools
import re
import pandas as pd
from dateutil.parser import parse


# In[2]:


# upload packages
with open('data/packages.json') as json_file:
    packages = json.load(json_file)


# ## #1. Subset values of dicts in arrays

# In[3]:


# get resources and unnest array [[1,2,3],[1,2],[1]] -> [1,2,3,1,2,1]
resources = [i["resources"] for i in packages]
resources = list(itertools.chain(*resources))

# common metadata
resource_package_id = [i["package_id"] for i in resources]
resource_id = [i["id"] for i in resources]
resource_description = [i["description"] for i in resources]
resource_name = [i["name"] for i in resources]
# resource_position = [i["position"] for i in resources]

# size: added condition to avoid NoneType
resource_size = [i["size"] for i in resources]
resource_size_mb = [i["size"]*0.000001 if type(i["size"]) == int else "null" for i in resources]

# dates
resource_last_modified = [parse(i["last_modified"]).date().isoformat() if type(i["last_modified"]) == str else "null" for i in resources]
resource_created = [parse(i["created"]).date().isoformat() if type(i["created"]) == str else "null" for i in resources]

# format
resource_format = [i["format"] for i in resources]
resource_mimetype = [i["mimetype"] for i in resources]

# url
resource_landing_page = ["https://data.gov.ua/dataset/{}/resource/{}".format(i["package_id"], i["id"]) for i in resources]
resource_datastore_url = ["https://data.gov.ua/api/3/action/datastore_search?resource_id={}".format(i) for i in resource_id]
resource_download_url = [i["url"] for i in resources]
# resource_url_type = [i["url_type"] for i in resources]

# qa
# in some resources qa property is quoted — ['{\'updated\': \'2019-02-02T02:22:02.723316\', \'openness_score\':
# i subset them by nulls. reminder: fix it in the future
# resource_qa = [i["qa"] if "qa" in i else "null" for i in resources]
# resource_qa_openness_score = [i["openness_score"] if type(i) == dict else "null" for i in resource_qa]
# resource_qa_format = [i["format"] if type(i) == dict else "null" for i in resource_qa]

# analyse length of fields
# s = re.compile('\s')
# resource_description_len = [len(s.split(i["description"])) for i in resources]
# resource_name_len = [len(s.split(i["name"])) for i in resources]

# resourse domain
slash_pattern = re.compile('\/')
resource_url_domain = [slash_pattern.split(i)[2] if bool(slash_pattern.search(i)) == True else "null" for i in resource_download_url]


# ## #2. Formats of resources 

# In[4]:


# clan format notation using mimetypes
resource_format_clean = []
for i in resource_mimetype:
    if i == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        resource_format_clean.append("XLSX")
    elif i == "application/vnd.ms-excel":
        resource_format_clean.append("XLS")
    elif i == "text/csv":
        resource_format_clean.append("CSV")
    elif i == "application/msword":
        resource_format_clean.append("DOC")
    elif i == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        resource_format_clean.append("DOCX")
    elif i == "application/zip":
        resource_format_clean.append("ZIP") 
    elif i == "text/xml":
        resource_format_clean.append("XML")
    elif i == "application/pdf":
        resource_format_clean.append("PDF")
    elif i == "application/vnd.oasis.opendocument.text":
        resource_format_clean.append("ODT")
    elif i == "application/json":
        resource_format_clean.append("JSON")
    elif i == "application/rtf":
        resource_format_clean.append("RTF")
    elif i == "application/vnd.oasis.opendocument.spreadsheet":
        resource_format_clean.append("ODS")
    elif i == "image/jpeg":
        resource_format_clean.append("JPEG")
    elif i == "text/html":
        resource_format_clean.append("HTML")
    elif i == "application/rdf+xml":
        resource_format_clean.append("RDF/XML")
    elif i == "text/plain":
        resource_format_clean.append("TXT")
    elif i == "application/xml":
        resource_format_clean.append("XML")
    elif i == "application/rar":
        resource_format_clean.append("RAR")
    elif i == "image/png":
        resource_format_clean.append("PNG")
    elif i == "image/gif":
        resource_format_clean.append("GIF")
    elif i == "None":
        resource_format_clean.append("Немає даних")
    else:
        resource_format_clean.append("Інше")

resource_format_type = []
for i in resource_mimetype:
    if i == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        resource_format_type.append("Структуровані")
    elif i == "application/vnd.ms-excel":
        resource_format_type.append("Структуровані")
    elif i == "text/csv":
        resource_format_type.append("Структуровані")
    elif i == "application/msword":
        resource_format_type.append("Текстові")
    elif i == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        resource_format_type.append("Текстові")
    elif i == "application/zip":
        resource_format_type.append("Архіви") 
    elif i == "text/xml":
        resource_format_type.append("Структуровані")
    elif i == "application/pdf":
        resource_format_type.append("Текстові")
    elif i == "application/vnd.oasis.opendocument.text":
        resource_format_type.append("Текстові")
    elif i == "application/json":
        resource_format_type.append("Структуровані")
    elif i == "application/rtf":
        resource_format_type.append("Текстові")
    elif i == "application/vnd.oasis.opendocument.spreadsheet":
        resource_format_type.append("Структуровані")
    elif i == "image/jpeg":
        resource_format_type.append("Графічні")
    elif i == "text/html":
        resource_format_type.append("Текстові")
    elif i == "application/rdf+xml":
        resource_format_type.append("Структуровані")
    elif i == "text/plain":
        resource_format_type.append("Текстові")
    elif i == "application/xml":
        resource_format_type.append("Структуровані")
    elif i == "application/rar":
        resource_format_type.append("Архіви")
    elif i == "image/png":
        resource_format_type.append("Графічні")
    elif i == "image/gif":
        resource_format_type.append("Графічні")
    elif i == "None":
        resource_format_type.append("Немає даних")
    else:
        resource_format_type.append("Інше")
        
# add is_format_structured_code
is_format_structured_code = []
for i in resource_format_type:
    if i == "Структуровані":
        is_format_structured_code.append(1)
    else:
        is_format_structured_code.append(0)


# In[5]:


# resource_format == resource_format_clean

is_format_correct_ukr = []
is_format_correct_code = []

for rf, rfc in zip(resource_format, resource_format_clean):
    if (rf == rfc or rf == "Немає даних" or rf == "Інше"):
        is_format_correct_ukr.append("Формати співпадають")
        is_format_correct_code.append(0)
    else:
        is_format_correct_ukr.append("Формати не співпадають")
        is_format_correct_code.append(1)


# ## #3 Datastore API availability

# In[7]:


# open local copy
with open('data/resource_samples.json') as json_file:
    resource_samples = json.load(json_file)


# In[8]:


# datastore properties
datastore_success = [i["success"] for i in resource_samples]
datastore_success_code = [1 if i == True else 0 for i in datastore_success]
# datastore_error = [i["error"]["message"] if "error" in i else "null" for i in resource_samples]
datastore_result = [i["result"] if "result" in i else "null" for i in resource_samples]
datastore_fields_len = [len(i["fields"]) if "fields" in i else "null" for i in datastore_result]


# In[9]:


# create and save df
resources_df = pd.DataFrame({"package_id": resource_package_id,
                             "id": resource_id,
                             "description": resource_description,
                             "name": resource_name,
#                             "position": resource_position,
                             "size": resource_size,
                             "size_mb": resource_size_mb,
                             "last_modified": resource_last_modified,
                             "created": resource_created,
                             "format": resource_format,
                             "mimetype": resource_mimetype,
                             "format_clean": resource_format_clean,
                             "format_type": resource_format_type,
                             "is_format_correct_code": is_format_correct_code,
                             "is_format_correct_ukr": is_format_correct_ukr,
                             "is_format_structured_code": is_format_structured_code,
                             "landing_page":resource_landing_page,
                             "download_url": resource_download_url,
                             "datastore_url": resource_datastore_url,
                             "url_domain": resource_url_domain,
#                             "url_type": resource_url_type,
#                             "qa_openness_score": resource_qa_openness_score,
#                             "qa_format": resource_qa_format,
#                             "description_len": resource_description_len,
#                             "name_len": resource_name_len,
                             "datastore_success": datastore_success,
                             "datastore_success_code": datastore_success_code,
#                             "datastore_error": datastore_error,
                             "datastore_fields_len": datastore_fields_len
                            })


# ## #4. Add aditional metadata

# In[10]:


# upload packages_df
packages_df = pd.read_csv("data/packages.csv")


# add package matadata
resources_df = pd.merge(resources_df, packages_df[["id", "title", "organization_title", "organization_name"]],
                        left_on = "package_id", right_on = "id", how = "left", suffixes= ("_resource", "_package"))

resources_df = resources_df.rename(index=str, columns={"id_resource": "id", "title": "package_title"})
resources_df = resources_df.drop(["id_package"], axis=1)

# save table
resources_df.to_csv("data/resources.csv", index=False)

