from usp.tree import sitemap_tree_for_homepage
import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
import flatdict
import re
from pprint import pprint

url=str("https://www.immoweb.be/")
substring1=str("https://www.immoweb.be/nl/zoekertje") 

def get_links_from_sitemap(url=str, substring1=str):
    ##use sitemap xml to get all the links on immoweb
    tree = sitemap_tree_for_homepage(url)
    ##go over all the links in the pages of the sitemap
    urls = [page.url for page in tree.all_pages()]
    ### if the beginning of the link matches  https://www.immoweb.be/nl/zoekertje we keep it 
    #substring1="https://www.immoweb.be/nl/zoekertje"
    str_match = [s for s in urls if substring1 in s]
     #clean data for doubles and empty values
    urls_final = list(dict.fromkeys(str_match))
    urls_final = list(filter(None, urls_final)) 
    pprint(urls_final)
    return urls_final

def get_properties_from_link(urls_final):
    #go over the links in the list and get the content for each link
    final_file = "final.csv"
    script={}
    #open a writeable file
    with open(r'./data_acquisition/final.csv', 'w')as final_file:
        #for each link get info on the page
        for link in urls_final:
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
            df=pd.DataFrame(dict_property)
    return df
                              
def get_charateristics_for_properties():
    get_links_from_sitemap(url=str,substring1=str)
    get_properties_from_link(urls_final=list[str])