from bs4 import BeautifulSoup
import requests
__package__

def determine_website(url):
    split_string = url.split("/")
    #split a string get the website
    #get the relevent json return it
    return split_string[2]

def get_chapter_info(url, wesbite_info):
    """
    Perfroms a HTML request to a URL, 
    determines the website E.g Manhwa.Plus

    Then,
    Seperates loads Json info about the website that was stored previously
    to guide the search to find what we want

    Next,
    Check if the status code is 200 

    After,
    Checks the HTML that was recieved in the request for teh information we need 
    using the JSON info we stored into variables

    Finally, 
    we store the chapters into a variable called data_table 
    which is finally returned
    """
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
