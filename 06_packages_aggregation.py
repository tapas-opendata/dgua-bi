#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


# upload packages_df and resources_df
resources_df = pd.read_csv("data/resources.csv")
packages_df = pd.read_csv("data/packages.csv")


# ## #1. Aggregate aditional variables

# In[3]:


# aggregate resources data by packages
# 1.1. package size
size_mb = resources_df.groupby("package_id", as_index=False).agg({"size_mb": pd.Series.sum})
# 1.2. number of resources in structured formats
num_resources_structured = resources_df.loc[resources_df["format_type"] == "Структуровані"].groupby("package_id", as_index=False).agg({"id": pd.Series.count})

# merge package_size_mb and num_resources_structured
agg = pd.merge(size_mb, num_resources_structured, left_on = "package_id", right_on = "package_id", how = "left")

# merge agg and packages_df
packages_df = pd.merge(packages_df, agg,
                       left_on = "id", right_on = "package_id", how = "left", suffixes= ("", "_agg"))


# rename columns
packages_df = packages_df.rename(index=str, columns={"size_mb": "resources_size_mb_sum",
                                                    "id_agg": "num_resources_structured"})

# drop doubling id
packages_df = packages_df.drop(["package_id"], axis=1)

# save csv
packages_df.to_csv("data/packages.csv", index=False)

