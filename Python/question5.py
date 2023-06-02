# Importing Libraries

import pandas as pd
import numpy as np
import json
import urllib.request
import re

from datetime import datetime


# Retreive Data from URL

my_url = ' http://api.tvmaze.com/singlesearch/shows?q=westworld&embed=episodes'

with urllib.request.urlopen(my_url) as url:
    api_data = json.loads(url.read().decode())



# Converting required data into dataframe

df = pd.json_normalize(api_data['_embedded']['episodes'])


# Deleting unnecessary columns

drop_cols=['airstamp','_links.self.href','_links.show.href']

for item in drop_cols:
    df.drop([item],axis=1,inplace=True)



# Converting 'airdate' column into datetime format

df['airdate'] = pd.to_datetime(df['airdate'],format='%Y-%m-%d',errors='coerce')


# Converting 'airtime' column into 12 Hour Time format

for i in range(len(df['airtime'])):
    time = datetime.strptime(df['airtime'][i],"%H:%M")
    df['airtime'][i] = time.strftime("%I:%M %p")


# Deleting html tags from 'summary' column

clean_data = '<.*?>'
for i in range(len(df['summary'])):
    df['summary'][i] = re.sub(clean_data,'',df['summary'][i])

print(df.head())