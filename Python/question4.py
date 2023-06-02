# Importing Libraries

import pandas as pd
import numpy as np
import json
import urllib.request

# Retreive Data from URL

my_url = 'https://data.nasa.gov/resource/y77d-th95.json'

with urllib.request.urlopen(my_url) as url:
    mt_data = json.loads(url.read().decode())


# Convert Json into Dataframe

mt_data_normalized = pd.json_normalize(mt_data)



# Convert Numeric columns from String to Numeric

num_cols = ['id','mass','reclat','reclong']

for item in num_cols:
    mt_data_normalized[item] =  pd.to_numeric(mt_data_normalized[item],errors='coerce')


# Drop Unnecessary Columns

drop_cols = [':@computed_region_cbhk_fwbd',':@computed_region_nnqa_25f4']

for item in drop_cols:
    mt_data_normalized.drop([item],axis=1,inplace=True)


# Convert Co-ordinate list into a list of int

for item in mt_data_normalized['geolocation.coordinates']:
    if item is not np.NaN:
           for i in range(len(item)):
                item[i] = int(item[i])


# Convert Year into datetime format

mt_data_normalized['year'] = pd.to_datetime(mt_data_normalized['year'],
               format='%Y-%m-%d %H:%M:%S.%f',errors='coerce')

# Convert Dataframe into CSV file

mt_data_normalized.to_csv('meteorite.csv',index=False)