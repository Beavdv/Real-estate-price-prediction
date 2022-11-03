from bs4 import BeautifulSoup
from lxml import etree
from usp.tree import sitemap_tree_for_homepage
import requests
from csv import writer
from bs4 import BeautifulSoup
import json
import flatdict
import re
from pprint import pprint
import collections 
import itertools
import numpy as np
import pandas as pd
# url="https://www.immoweb.be/"
# substring1=str("https://www.immoweb.be/nl/zoekertje")
def flatten(new_list=[],link=str,strmatch=list[str]):
    if isinstance(link,strmatch) and not isinstance(link, str): 
        for subc in flatten(link):
            yield subc
    else:
            yield link

def get_charateristics_for_properties():
    strmatch=get_links_from_sitemap(url=str,substring=str)
    get_properties_from_links(strmatch)

def get_links_from_sitemap(url=str, substring=str):
    ##use sitemap xml to get all the links on immoweb
    tree = sitemap_tree_for_homepage("https://www.immoweb.be/")
    ##go over all the links in the pages of the sitemap
    urls = [page.url for page in tree.all_pages()]
    ### if the beginning of the link matches  https://www.immoweb.be/nl/zoekertje we keep it 
    prop_list=["huis","appartement","industrie","grond","handelszaak","kantoor",
    "nieuwbouwproject-huizen","nieuwbouwproject-appartementen","garage","vakantiehuis",
    "opbrengsteigendom","andere","bed-and-breakfast","stacaravan","hotel","camping",
    "woonboot","vakantiepark","ander-huis"]
    i=0
    strmatch=list([str])             
    for s in urls:
        for value in prop_list:
            substring=(f'https://www.immoweb.be/nl/zoekertje/{value}/te-koop')
            if substring in s:
                i+=1
                strmatch += [s]
    pprint(strmatch)
    print(i)
    return strmatch
    
def get_properties_from_links(strmatch=list[str]):
    #go over the links in the list and get the content for each link
    final_file = "final.csv"
    script={}
    new_list=[]
    flatten(strmatch)
    #open a writeable file
    with open(r'./data_acquisition/final.csv', 'w') as final_file:
        #for each link get info on the pages
        for link in new_list:           
            page1 = requests.get(link)
            soup = BeautifulSoup(page1.content, "html.parser")
            #find the right script: the second one
            script=soup.find_all('script')
            my_set=script[1].text
            #take out empty lines and spaces
            my_set=my_set.replace(' ','')
            my_set=my_set.replace('\n','')
            #take out the information you need
            result=re.search('\"classified\":(.+),(\"customer\")',my_set)
            #from the regex take everything that is between classified and customer=the middle group, group(1)
            result=result.group(1)
            #load string with json to make a usable dictionary and flatten it=because the result is dict in dict 
            json_string=json.loads(result)
            dict_property =  dict(flatdict.FlatDict(json_string, delimiter='_'))
            #dump it with json in a file 
            final_file.write(json.dumps(dict_property))
            results = pd.np.array(dict_property)
            print(results)
            return results

get_charateristics_for_properties()

