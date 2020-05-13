#!/usr/bin/env python
# coding: utf-8

# In[8]:


#Extra all the zip codes
import pandas as pd
import math

listings = pd.read_csv('x+income+commute+sentiment.csv')
listings.head(5)
zipcode = list(set(listings.zipcode))
zipcode = list(map(lambda zipcode: str(zipcode), zipcode))


# In[9]:


len(zipcode)


# In[21]:


from yelpapi import YelpAPI

# krystal_key = 'V3JH2VwM_qevSc31z_rmUws_m2ZwIs88jbEM9YP5ivI-XyCoo9abh8tlcIG3w1Kgn5arpKDj0Ce2bUAIG40yCIMC_ZPwR6ADQJLZOVNVyl0qufQAlbiLt4SXSZf2XXYx'
key = 'IQvVZglBngcRE_S3Bp21PQEYQmHqo0Zd5FyCiNj0esyiEB-7aMKO0hQjb3JQ3VvfcJdXmvQ_mUuNvevxqbGX_o6JoIFVDbJ9-xwH4lsmZPgkO3EUIbjyuUBlm8DKXXYx'
yelp_api = YelpAPI(key)


# In[32]:


def extract_zip(entry):
    return entry['location']['zip_code']
    
density = {}

for code in zipcode[170:]:
    search_results = {}

    for i in range(0, 20):
        offs = i * 50
        results = yelp_api.search_query(term = "food", offset = offs, location = code, limit = 50)

        if not search_results:
            search_results.update(results)               
        else:
            for elem in results['businesses']:
                search_results['businesses'].append(elem)    

    restaurants = search_results['businesses']
    df = pd.DataFrame(restaurants)
    df.drop_duplicates(subset="id", inplace=True)            
    df = df[['name','location']]            

    df['zip'] = df.apply(extract_zip, axis = 1)  
    new_df = df.drop(df[df.zip!=code].index) 
    density[code] = len(new_df)

print(density)


# In[12]:


density_out = density.copy()
print(density_out)


# In[33]:


density_out.update(density)
print(density_out)


# In[34]:


len(density_out.keys())


# In[35]:


import csv

with open('density_nyc.csv','w') as f:
    w = csv.writer(f)
    w.writerows(density_out.items())


