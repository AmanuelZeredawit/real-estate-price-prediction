from asyncore import write
from tokenize import Number
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
#import httplib2
from bs4 import SoupStrainer
import sys
import json
import re
import csv

# get connecting to chrome browser
driver = webdriver.Chrome(r"C:\Users\32467\OneDrive\Documents\Arai4_Projects\real-estate-price-prediction\data_acquisition\chromedriver.exe")

root_url = "https://www.immoweb.be/en"
apartments_url = "https://www.immoweb.be/en/search/apartment/for-sale?countries=BE"
house_url = "https://www.immoweb.be/en/search/house/for-sale?countries=BE"
property_url = "https://www.immoweb.be/en/classified/new-real-estate-project-houses/for-sale/berlaar/2590/10146116?searchId=633e93026eea3"
new_real_estate_apartment_url ="https://www.immoweb.be/en/search/new-real-estate-project-apartments/for-sale?countries=BE"
new_real_estate_house_url = "https://www.immoweb.be/en/search/new-real-estate-project-houses/for-sale?countries=BE"
house_and_apartment_url = "https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE"

#https://www.immoweb.be/en/search/apartment/for-sale?countries=BE&page=333&orderBy=relevance

    
def get_characterstics_from_url(property_url):
    """
    This function takes :param: property_url
    return the charactererstics of a property in dictionary as targeted_data
    """
    driver.get(property_url)
    #get_url = driver.current_url
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    
    scripts = soup.find_all("script", {"type": "text/javascript"})
    #print(scripts)
    pattern1 = "window.classified ="
    pattern2 = "<script>"
    pattern3 = "</script>"
    pattern4 = ";"
    
    
    for script in scripts:
        if pattern1 in script.text:
            targeted_script = script
            break
    compiled = re.compile("(%s|%s|%s|%s)" % (pattern1,pattern2,pattern3,pattern4))
    targeted_script_regexd = compiled.sub('',targeted_script.text)
    targeted_data = json.loads(targeted_script_regexd)
    required_data = targeted_data['property']
    required_data.pop('description')
    required_data.pop('alternativeDescriptions') 
    return required_data

#print(get_characterstics_from_url(property_url))



def get_page_urls(root_url):
    """
    It goes to each page and save the urls of a property
    takes :param: page_number, tag
    return a dictionary named proerty_urls
    """
    driver.get(root_url)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    links = soup.find_all('a')
    list_of_page_url = []
    for link in links:
        if link.has_key('href'):
            if '/classified/' in link['href']:
                list_of_page_url.append(link['href'])
                #print(link['href'])
    
    return list_of_page_url

#print(get_page_urls(appartments_url))

def save_pages_urls():
    """
    this function pass the pages url to get_page_url function and save the links 
    """
    
    # https://www.immoweb.be/en/search/apartment/for-sale?countries=BE&page=333&orderBy=relevance
    #number_of_pages = 10
    all_pages_url_dic = dict()
    # set a list of urls of the different category of property
    # property_types_urls = [apartments_url,house_url,new_real_estate_apartment_url,new_real_estate_house_url,house_and_apartment_url]
    property_types_urls = [apartments_url,house_url]
    # set a dictionary of type of property with the number of pages             
    #page_number_of_types = {apartments_url:333, house_url:333, new_real_estate_apartment_url:71,new_real_estate_house_url:32}
    page_number_of_types = {apartments_url:5, house_url:5}

    # open a json file to save the lists of properties urls
    with open('property_page_urls.json', 'w') as fp:
        print('############## json file opened for saving the urls  ####################')
        # loop over the pages of different property types and get url for each property
        for property_type_url in property_types_urls:
             # display for which type of propety we are getting the links
             print('###############',str(property_type_url) + '###################' )

             for number in range(1,page_number_of_types[property_type_url] + 1):
                # for the first page page_url is the same as the property_type_urls
                if number == 1:
                    property_page_url = property_type_url
                else:
                    property_page_url = property_type_url + '&page=' + str(Number) + '&orderBy=relevance'
                try:
                    all_pages_url_dic[number] = get_page_urls(property_page_url)
                    # track which page the program has reached
                    print('page number: ', str(number) + ' ', property_page_url)
                except:
                    print("can't access page maybe wrong page")
                    continue

             #load the all_pages_url_dic into a json file
             json.dump(all_pages_url_dic, fp)
    save_properties(all_pages_url_dic)
            
            
def save_properties(all_pages_url_dic):     
    """
    save the properties characterstics into a csv file
    """
    # open the json file containing the properties url
    #with open('property_page_urls.json', 'r') as fp:
     #
     #    all_pages_url_dic = json.load(fp)

    # initialize count, to count the number of properties
    count =0
    
    # create and open a csv file to write the properites characterstics
    with open ('properties_characterstics','w') as f:
        print('###############     csv file opened     #########################')
        # loop over the dictionary, get a property url, with that url get the property characterstics from other fn, and save it to csv file
        for list_of_url in [all_pages_url_dic[i] for i in all_pages_url_dic]:
            for url in list_of_url:
                count += 1 
                if count == 100:
                    sys.exit()
                try:
                    row = get_characterstics_from_url(url)
                    write = csv.writer(f)
                    write.writerows(row)
                    print('number of properties retireved so far  :' ,count)
                    print('property url: ',url)
                    
                except:
                    print('incorrect page url')
                    continue

    



def start_scrapping():
    """
     Initialize the processes  of scraping 
     
    """

    save_pages_urls()


start_scrapping()
     
    



