#!/usr/bin/env python
# coding: utf-8

# In[3]:


import json
import datetime
import re
import numpy as np
import pandas as pd
from dateutil.parser import parse


# In[4]:


# open local copy
with open('data/packages.json') as json_file:
    packages = json.load(json_file)


# ## #1. Subset values of dicts in arrays

# In[5]:


# common metadata
package_id = [i["id"] for i in packages]
package_title = [i["title"] for i in packages]
package_notes  = [i["notes"] for i in packages]
package_purpose = [i["purpose_of_collecting_information"] for i in packages]
package_url = ["https://data.gov.ua/dataset/{}".format(i) for i in package_id]

# get license
package_license_title = [i["license_title"] if "license_title" in i else 'null' for i in packages]
package_license_id = [i["license_id"] if "license_id" in i else 'null' for i in packages]

# get resources
package_num_resources = [i["num_resources"] if "num_resources" in i else 'null' for i in packages]

# get tags
package_tag_string = [i["tag_string"] for i in packages]
package_num_tags = [i["num_tags"] if "num_tags" in i else 'null' for i in packages] # debug absent keys in objects

# get dates
package_update_frequency = [i["update_frequency"] for i in packages]
package_metadata_created  = [parse(i["metadata_created"]).date().isoformat() for i in packages]
package_metadata_modified = [parse(i["metadata_modified"]).date().isoformat() for i in packages]

# get organization
package_organization_title = [i["organization"]["title"] for i in packages]
package_organization_name = [i["organization"]["name"] for i in packages]

# get maintainer
package_maintainer = [i["maintainer"] if "maintainer" in i else 'null' for i in packages]
package_maintainer_email = [i["maintainer_email"] if "maintainer_email" in i else 'null' for i in packages]

# get author
package_author = [i["author"] if "author" in i else 'null' for i in packages]
package_author_email = [i["author_email"] if "author_email" in i else 'null' for i in packages]

# qa
# package_qa_openness_score = [i["qa"]["openness_score"] if "qa" in i else 'null' for i in packages]
# extract openness_score_reason_args
# p = re.compile('(?<=\[\[\")[a-zA-Z]{3,5}')
# package_qa_openness_score_reason_args = [p.findall(i["qa"]["openness_score_reason_args"]) if "qa" in i else [] for i in packages]
# package_qa_openness_score_reason_args = [i[0] if len(i) > 0 else 'null' for i in package_qa_openness_score_reason_args]

# analyse length of fields
s = re.compile('\s')
package_title_len = [len(s.split(i["title"])) for i in packages]
package_notes_len  = [len(s.split(i["notes"])) for i in packages]
package_purpose_len = [len(s.split(i["purpose_of_collecting_information"])) for i in packages]


# ## #2. Calculate update status
# 
# This script calculates dataset update status (updated or not) by comparison of today date and date of the future update. If a date of the future update is less than today date, a dataset is not updated. For "immediately after making changes" option a planned period of an update is not less than one year.

# In[7]:


# create package_update_frequency array in ukrainian
package_update_frequency_ukr = []
for i in package_update_frequency:
    if i == 'more than once a day':
        package_update_frequency_ukr.append("Більш як один раз на день")
    elif i == 'once a day':
        package_update_frequency_ukr.append("Щодня")
    elif i == 'once a week':
        package_update_frequency_ukr.append("Щотижня")
    elif i == 'once a month':
        package_update_frequency_ukr.append("Щомісяця")
    elif i == 'once a quarter':
        package_update_frequency_ukr.append("Щокварталу")
    elif i == 'once a half year':
        package_update_frequency_ukr.append("Кожного півріччя")
    elif i == 'once a year':
        package_update_frequency_ukr.append("Щороку")
    elif i == 'immediately after making changes':
        package_update_frequency_ukr.append("Відразу після внесення змін")
    else:
        package_update_frequency_ukr.append("Інше")
        
        
# create timedelta (package_update_frequency_timedelta) array based on package_update_frequency
package_update_frequency_timedelta = []
for i in package_update_frequency:
    if i == 'more than once a day':
        package_update_frequency_timedelta.append(datetime.timedelta(seconds=86399))
    elif i == 'once a day':
        package_update_frequency_timedelta.append(datetime.timedelta(days=1))
    elif i == 'once a week':
        package_update_frequency_timedelta.append(datetime.timedelta(days=7))
    elif i == 'once a month':
        package_update_frequency_timedelta.append(datetime.timedelta(days=31))
    elif i == 'once a quarter':
        package_update_frequency_timedelta.append(datetime.timedelta(days=92))
    elif i == 'once a half year':
        package_update_frequency_timedelta.append(datetime.timedelta(days=183))
    elif i == 'once a year':
        package_update_frequency_timedelta.append(datetime.timedelta(days=365))
    elif i == 'immediately after making changes':
        package_update_frequency_timedelta.append(datetime.timedelta(days=365))
    else:
        package_update_frequency_timedelta.append(datetime.timedelta(days=365))
        
# convert strings to date objects
package_metadata_created_date = [parse(i).date() for i in package_metadata_created]
package_metadata_modified_date = [parse(i).date() for i in package_metadata_modified]

# create array of planned update dates and check status (updated in time of not)
package_metadata_planned_date = np.array(package_update_frequency_timedelta) + np.array(package_metadata_modified_date)
# convert package_metadata_planned_date to ISO format
package_metadata_planned_date_iso = [i.isoformat() for i in package_metadata_planned_date]
# calculate update satus: if planned apdate date in the past, dataset is not updated 0 - updated in time, 1 - not updated 
package_update_satus_code = [0 if i > datetime.datetime.now().date() else 1 for i in package_metadata_planned_date]
package_update_satus_ukr = ["Оновлено вчасно" if i > datetime.datetime.now().date() else "Не оновлено вчасно" for i in package_metadata_planned_date]


# ## #3. Save df 

# In[8]:


# create and save df
packages_df =  pd.DataFrame({"id": package_id,
                             "title": package_title,
                             "notes": package_notes,
                             "purpose": package_purpose,
                             "url": package_url,
                             "license_title": package_license_title,
                             "license_id": package_license_id,
                             "num_resources": package_num_resources,
                             "tag_string": package_tag_string,
                             "num_tags": package_num_tags,
                             "update_frequency": package_update_frequency,
                             "update_frequency_ukr": package_update_frequency_ukr,
                             "metadata_created": package_metadata_created,
                             "metadata_modified": package_metadata_modified,
                             "metadata_planned_date_iso": package_metadata_planned_date_iso,
                             "update_satus_code": package_update_satus_code,
                             "update_satus_ukr": package_update_satus_ukr,
                             "organization_title": package_organization_title,
                             "organization_name": package_organization_name,
                             "maintainer": package_maintainer,
                             "maintainer_email": package_maintainer_email,
                             "author": package_author,
                             "author_email": package_author_email,
#                             "qa_openness_score": package_qa_openness_score,
#                             "qa_openness_score_reason_args": package_qa_openness_score_reason_args,
                             "title_len": package_title_len,
                             "notes_len": package_notes_len,
                             "purpose_len": package_purpose_len
                            })

packages_df.to_csv("data/packages.csv", index=False)

