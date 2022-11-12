from usp.tree import sitemap_tree_for_homepage
import requests
from bs4 import BeautifulSoup
import json
import flatdict
import re
from pprint import pprint
import pandas as pd


def get_links_from_sitemap(homepage_url: str):
    ##use sitemap xml to get all the links on immoweb
    tree = sitemap_tree_for_homepage(homepage_url)
    ##go over all the links in the pages of the sitemap
    urls = [page.url for page in tree.all_pages()]
    ### if the beginning of the link matches  https://www.immoweb.be/nl/zoekertje we keep it
    prop_list = ["huis", "appartement", "industrie", "grond", "handelszaak", "kantoor",
                 "nieuwbouwproject-huizen", "nieuwbouwproject-appartementen", "garage", "vakantiehuis",
                 "opbrengsteigendom", "andere", "bed-and-breakfast", "stacaravan", "hotel", "camping",
                 "woonboot", "vakantiepark", "ander-huis"]
    i = 0
    strmatch = list([str])
    new_filename = "./data_new.csv"
    file = open(new_filename, "w")
    for s in urls:
        for value in prop_list:
            substring = (f'https://www.immoweb.be/nl/zoekertje/{value}/te-koop')
            if substring in s:
                i += 1
                s=s.strip("https://")
                file.write(f'{s}\n')
                strmatch += [s]
    pprint(strmatch)
    print(i)
    return strmatch
def get_properties_from_link():
    #go over the links in the list and get the content for each link
    final_file = "final.csv"
    #flatten(strmatch)
    #open a writeable file
    with open(r"./data_new.csv", "r") as my_file:
        my_file=my_file.readlines()
        with open(r'./final.csv', 'w') as final_file:
            #for each link get info on the pages
            #for url in strmatch:
            for url in my_file:
                url="https://"+'url'
                page1 = requests.get(url)
                soup = BeautifulSoup(page1.content, "html.parser")
                # find the right script: the second one
                script = soup.find_all('script')
                my_set = script[1].text
                # take out empty lines and spaces
                my_set = my_set.replace(' ', '')
                my_set = my_set.replace('\n', '')
                # take out the information you need
                result = re.search('\"classified\":(.+),(\"customer\")', my_set)
                # from the regex take everything that is between classified and customer=the middle group, group(1)
                result = result.group(1)
                # load string with json to make a usable dictionary and flatten it=because the result is dict in dict
                json_string = json.loads(result)
                dict_property = dict(flatdict.FlatDict(json_string, delimiter='_'))
                # dump it with json in a file
                final_file.write(json.dumps(dict_property))
                results = pd.np.array(dict_property)
                pprint(results)
                return results

get_properties_from_link()


# def get_charateristics_for_properties():
#     strmatch=get_links_from_sitemap(homepage_url='https://www.immoweb.be/')
#     get_properties_from_link(strmatch)


#get_charateristics_for_properties()






