import json
import os
__package__

def dump_JSON_data(name, url, chapters):
    dictonary = {
        "name": name,
        "url": url,
        "chapters": [chapters]
    }
    write_location = "../json_data/{}.json".format(name)
    try:
        if not os.path.exists(write_location):
            with open(write_location, "w") as file:
                json.dump(dictonary,file,indent=4) 
        else:
            with open(write_location, "w+", encoding="utf-8") as file:
                json.dump(dictonary,file,indent=4) 
    except Exception as e:
        print("somthing went wrong", e)


def update_JSON_data():
    pass
def get_JSON_data():
    directory = "../json_data"
    data_dict = {}
    for filename in os.listdir(directory):
        f = os.path.join(directory,filename)
        with open(f) as file:
            json_data = json.load(file)
            
            data_dict[json_data['name']] = json_data
    
    return data_dict
