from asyncio import sleep
from os import write
import time
from html.parser import HTMLParser
from bs4 import BeautifulSoup
from urllib.request import urlopen
import argparse
import website as website
import chapter as chapter
import json_functions as json_func


def output_updates(updates):
    for key in updates:
        print("{} has {} updates\n".format(key, updates[key]))
    return


def add_manga(url,name):
    """
    Gets chapter information 
    then stores them into a json file for use in the future
    """
    website_info = website.get_website_json(url)
    chapters = chapter.get_chapter_info(url,website_info)
    json_func.dump_JSON_data(name,url,chapters)
def check():
    """
    Retrieves JSON data about stored mangas, fetches chapter info from a website,
    compares the new chapter data to the stored data, updates the JSON if needed,
    and finally outputs any updates found.
    """

    # A dictionary that will keep track of the update status (number of new chapters) for each manga
    updates = {}

    # Load the previously stored JSON data for all mangas we want to check
    json_data = json_func.get_JSON_data()

    # Dictionary to store newly retrieved chapter information for each manga
    get_chapters = {}

    print("Retrieving data...\n")

    # Get additional website-specific information in JSON format (perhaps rules for parsing, URLs, etc.)
    

    # For each manga in our stored JSON data:
    #   1. Fetch the latest chapter information from the website.
    #   2. Wait 3 seconds between each request (likely to avoid spamming the server).
    for key in json_data:
        wesbite_info = website.get_website_json(json_data[key]['url'])
        get_chapters[key] = chapter.get_chapter_info(json_data[key]['url'], wesbite_info)
        time.sleep(3)

    # Compare the newly retrieved chapters (get_chapters) with the stored chapters (json_data)
    # to figure out if there have been any updates.
    for check in get_chapters:
        # If the newly retrieved chapters match exactly with what we have stored, set updates to 0.
        if get_chapters[check] == json_data[check]['chapters']:
            updates[check] = 0
        else:
            # Otherwise, we check how many new chapters we might have:
            i, count = 0, 0
            list1 = get_chapters[check]            # New chapter list
            list2 = json_data[check]['chapters'][0]  # The first element of the stored chapters list

            # Compare each chapter in the new list (list1) to each chapter in the old list (list2).
            for y in list1:  # For every chapter in the new list
                for x in list2:  # Compare with every chapter in the old list
                    if y != x:
                        i += 1
                        continue
                    else:
                        # As soon as we find a match, stop this inner loop
                        break

                # If we reached 5 mismatches, consider that 1 new update
                if i == 5:
                    count += 1

                # Reset the mismatch counter for the next iteration
                i = 0

            # Store how many new chapters we found for this manga
            updates[check] = count

    # After determining the update counts, go through each manga. If there are updates, write new data.
    for key in updates:
        if updates[key] > 0:
            # Update the stored JSON data to reflect the new chapters
            json_func.dump_JSON_data(json_data[key]['name'], json_data[key]['url'], get_chapters[key])

    # Finally, output any updates that were found
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
 
