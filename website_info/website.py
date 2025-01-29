import json
import os

__package__
def get_website_json(url):
    directory = "websites_json"
    data_dict = {}
  
    for filename in os.listdir(directory):
        f = os.path.join(directory,filename)
        with open(f) as file:
            json_data = json.load(file)
         
            if json_data['website'] in url:
                data_dict[json_data['website']] = json_data
                break
 
    return data_dict