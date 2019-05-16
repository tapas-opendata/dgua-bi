#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import itertools
import re
import pandas as pd


# In[2]:


# upload packages
with open('data/packages.json') as json_file:
    packages = json.load(json_file)


# ## #1. Subset values of dicts in arrays

# In[3]:


# subsetting at the level of packages
package_id = [i["id"] for i in packages]
package_tags = [i["tags"] for i in packages]
package_tags_len = [len(i["tags"]) for i in packages]

# subsetting at the level of tags
tags = list(itertools.chain(*package_tags))
tag_name = [i["name"] for i in tags]
# tag_display_name = [i["display_name"] for i in tags]
tag_state = [i["state"] for i in tags]
tag_id = [i["id"] for i in tags]

# calculate length of tags
s = re.compile('\s')
tag_name_len = [len(s.split(i)) for i in tag_name]

# generate array of package ids for each tag
tag_package_id = []
for i, l in zip(package_id, package_tags_len):
    tag_package_id.append(list(itertools.repeat(i, l)))

tag_package_id = list(itertools.chain(*tag_package_id))


# In[4]:


# create and save df
tag_df = pd.DataFrame({"name": tag_name,
#                       "display_name": tag_display_name,
                       "state": tag_state,
                       "id": tag_id,
                       "name_len": tag_name_len,
                       "package_id": tag_package_id
                      })


# ## #4. Add aditional metadata

# In[5]:


# upload packages_df
packages_df = pd.read_csv("data/packages.csv")

# add packages' matadata
tag_df = pd.merge(tag_df, packages_df[["id", "title", "organization_title", "organization_name"]],
                  left_on = "package_id", right_on = "id", how = "left", suffixes= ("_tag", "_package"))

tag_df = tag_df.rename(index=str, columns={"id_tag": "id", "title": "package_title"})
tag_df = tag_df.drop(["id_package"], axis=1)

# save table
tag_df.to_csv("data/tags.csv", index=False)

