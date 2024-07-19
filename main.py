from asyncio import sleep
from os import write
import os
import time
import requests
from html.parser import HTMLParser
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pdb
import json
import argparse
import sys
def determine_website(url):
    split_string = url.split("/")
    #split a string get the website
    #get the relevent json return it

    return split_string[2]

def get_website_json():
    directory = "website_info"
    data_dict = {}
    for filename in os.listdir(directory):
        f = os.path.join(directory,filename)
        with open(f) as file:
            json_data = json.load(file)
            
            data_dict[json_data['website']] = json_data
    
    return data_dict

def get_chapter_info(url, wesbite_info):
    html = requests.get(url)
    website = determine_website(url)

    tag = wesbite_info[website]['tag']
    html_class = wesbite_info[website]['class']
    sub_tag = wesbite_info[website]['sub-tag']

    if(html.status_code != 200):
        return None
    soup = BeautifulSoup(html.text, "lxml")
    table = soup.find_all(tag, class_ = html_class)
    data_table = []
    x = 0
    for item in table:
        if(x == 5):
            break

        link = item.find(sub_tag)
        if link:
            link_text = link.text.replace('\n', '').strip()
            data_table.append(link_text)
            x += 1
    
    return data_table

def dump_JSON_data(name, url, chapters):
    dictonary = {
        "name": name,
        "url": url,
        "chapters": [chapters]
    }
 
    write_location = "json_data/{}.json".format(name)
    with open(write_location, 'w') as file:
        json.dump(dictonary,file,indent=4)
        
    
def update_JSON_data():
    pass
def get_JSON_data():
    directory = "json_data"
    data_dict = {}
    for filename in os.listdir(directory):
        f = os.path.join(directory,filename)
        with open(f) as file:
            json_data = json.load(file)
            
            data_dict[json_data['name']] = json_data
    
    return data_dict

def output_updates(updates):
    for key in updates:
        print("{} has {} updates\n".format(key, updates[key]))
    return

def add_manga(url,name):
    chapters = get_chapter_info(url)
    dump_JSON_data(name,url,chapters)

def check():
   #determine command type
    updates = {}
    json_data = get_JSON_data()
    get_chapters = {}
    print("Retrieving data...\n")

    wesbite_info = get_website_json()
    
    for key in json_data:  
        get_chapters[key] = get_chapter_info(json_data[key]['url'],wesbite_info)
        time.sleep(3) 
    for check in get_chapters:
        if(get_chapters[check] == json_data[check]['chapters']):
            updates[check] = 0
        else:
            i,count = 0,0
            list1 = get_chapters[check]
            list2 = json_data[check]['chapters'][0]
            for y in list1:
                for x in list2:
                    if(y != x):
                        i += 1
                        continue
                    else:
                        break;
                if(i == 5):
                    count += 1

                i = 0
            updates[check] = count 
    for key in updates:
        if(updates[key] > 0):
            #update
            dump_JSON_data(json_data[key]['name'], json_data[key]['url'], get_chapters[key])
        
    output_updates(updates)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some arguments.")
    
    # Create a mutually exclusive group
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--check', action='store_true', help='Check the status')
    group.add_argument('--add', action='store_true', help='Add data')

    parser.add_argument('--url', help='URL of the manga')
    parser.add_argument('--name', help='Name of the manga')
    
    args = parser.parse_args()

    if args.check:
        check()
    elif args.add:
        if not args.url or not args.name:
            parser.error("--url and --name are required when --add is specified")
        add_manga(args.url, args.name)
 
