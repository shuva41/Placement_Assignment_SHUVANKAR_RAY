# Importing Libraries

import pandas as pd
import numpy as np
import json
import urllib.request



# Retreive Data from URL

my_url = 'https://raw.githubusercontent.com/Biuni/PokemonGO-Pokedex/master/pokedex.json'

with urllib.request.urlopen(my_url) as url:
    data = json.loads(url.read().decode())

new_json = list(data.values())[0]                # List of Json



# Function to flatten JSON

def flatten_json(nested_json):

    """
        Flatten json object with nested keys into a single level.
        Args:
            nested_json: A nested json object.
        Returns:
            The flattened json object if successful, None otherwise.
    """

    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                if a == 'next_evolution' or a == 'prev_evolution':
                    out[a] = x[a]
                else:
                    flatten(x[a], name + a + '_')              # Recursion
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x
            
    
   
    flatten(nested_json)                                       # Calling the function
    return out




# Flattening the List of Json using above function 

flattened_json = []

for item in new_json:
    if 'next_evolution' not in item.keys():
        item['next_evolution'] = [{'num':'','name':''}]
    if 'prev_evolution' not in item.keys():
        item['prev_evolution'] = [{'num':'','name':''}]
    new_dict = flatten_json(item)
    flattened_json.append(new_dict)


# Normalizing 'next_evolution' column
normalized_df1 = pd.json_normalize(flattened_json,'next_evolution',['id','num','name','img','type_0','type_1','height','weight','candy','candy_count','egg','spawn_chance','avg_spawns','spawn_time','multipliers_0','multipliers_1','multipliers','weaknesses_0','weaknesses_1','weaknesses_2','weaknesses_3','weaknesses_4','weaknesses_5','weaknesses_6'],errors='ignore',record_prefix='next_evolution')

# Normalizing 'prev_evolution' column
normalized_df2 = pd.json_normalize(flattened_json,'prev_evolution',['id','num','name','img','type_0','type_1','height','weight','candy','candy_count','egg','spawn_chance','avg_spawns','spawn_time','multipliers_0','multipliers_1','multipliers','weaknesses_0','weaknesses_1','weaknesses_2','weaknesses_3','weaknesses_4','weaknesses_5','weaknesses_6'],errors='ignore',record_prefix='prev_evolution')

# Merging the two dataframes, on the common columns
final_normalized_df = pd.merge(normalized_df1,normalized_df2,how='outer',on=['id','num','name','img','type_0','type_1','height','weight','candy','candy_count','egg','spawn_chance','avg_spawns','spawn_time','multipliers_0','multipliers_1','multipliers','weaknesses_0','weaknesses_1','weaknesses_2','weaknesses_3','weaknesses_4','weaknesses_5','weaknesses_6'])
final_normalized_df.drop(['multipliers'],axis=1,inplace=True)

# Re-arranging the Columns
final_normalized_df = final_normalized_df[['id', 'num', 'name', 'img',
       'type_0', 'type_1', 'height', 'weight', 'candy', 'candy_count', 'egg',
       'spawn_chance', 'avg_spawns', 'spawn_time', 'multipliers_0',
       'multipliers_1', 'weaknesses_0', 'weaknesses_1', 'weaknesses_2',
       'weaknesses_3', 'weaknesses_4', 'weaknesses_5', 'weaknesses_6',
       'prev_evolutionnum', 'prev_evolutionname','next_evolutionnum', 'next_evolutionname']]


# Saving the final dataframe into excel file
final_normalized_df.to_excel('final.xlsx',index=False)


