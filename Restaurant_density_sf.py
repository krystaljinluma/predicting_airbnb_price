#!/usr/bin/env python
# coding: utf-8

# In[213]:


#Extra all the zip codes
import pandas as pd
import math

listings = pd.read_csv('listings_sf.csv')
listings.head(5)
zc = list(set(listings.zipcode))
zc = list(map(lambda zc: str(zc), zc))
print(list(zc))

zipcode = []

for c in zc:
    if ("CA" in c):
        c = c.replace('CA', '')
    
    if (c == '' or c == 'nan'):
        continue
    else:
        c = c.strip()
        zipcode.append(c)
     

# In[214]:


len(zipcode)


# In[21]:


from yelpapi import YelpAPI

key = 'V3JH2VwM_qevSc31z_rmUws_m2ZwIs88jbEM9YP5ivI-XyCoo9abh8tlcIG3w1Kgn5arpKDj0Ce2bUAIG40yCIMC_ZPwR6ADQJLZOVNVyl0qufQAlbiLt4SXSZf2XXYx'
yelp_api = YelpAPI(key)


# In[230]:


def extract_zip(entry):
    return entry['location']['zip_code']
    
density = {}

for code in zipcode[30:]:
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
#     print("df: ", df.shape)
    df.drop_duplicates(subset="id", inplace=True)            
    df = df[['name','location']]            

    df['zip'] = df.apply(extract_zip, axis = 1)  
#     print(df.head(5))
    new_df = df.drop(df[df.zip!=code].index) 
#     print("new df: ", new_df.shape)
    density[code] = len(new_df)

print(density)


# In[222]:


density_out = density.copy()


# In[231]:


density_out.update(density)
print(density_out)


# In[232]:


len(density_out.keys())


# In[235]:


import csv

with open('density_sf.csv','w') as f:
    w = csv.writer(f)
    w.writerows(density_out.items())


