from asyncore import write
from ftplib import all_errors
from tokenize import Number
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import sys
import json
import re
import csv
import flatdict

# get connection to chrome browser
driver = webdriver.Chrome(r"C:\Users\32467\OneDrive\Documents\Arai4_Projects\real-estate-price-prediction\data_acquisition\chromedriver.exe")


# # optimize the selenium
# options = webdriver.ChromeOptions()
# options.add_experimental_option('excludeSwitches', ['enable-logging'])
# #options.add_argument("--headless") 
# options.add_argument("--disable-infobars")
# options.add_argument("--disable-extensions")
# options.add_argument("--disable-gpu")
# prefs = {"profile.managed_default_content_settings.images":2,
#          "profile.default_content_setting_values.notifications":2,
        
#          "profile.managed_default_content_settings.stylesheets":2,
#          "profile.managed_default_content_settings.cookies":2,
#          "profile.managed_default_content_settings.javascript":1,
#          "profile.managed_default_content_settings.plugins":1,
#          "profile.managed_default_content_settings.popups":2,
#          "profile.managed_default_content_settings.geolocation":2,
#          "profile.managed_default_content_settings.media_stream":2,
# }
# options.add_experimental_option("prefs",prefs)

# # Configure Selenium browser
# driver = webdriver.Chrome(options=options)
# driver.minimize_window()
# set the url variables
root_url = "https://www.immoweb.be/en"
apartments_url = "https://www.immoweb.be/en/search/apartment/for-sale?countries=BE"
house_url = "https://www.immoweb.be/en/search/house/for-sale?countries=BE"
property_url = "https://www.immoweb.be/en/classified/apartment/for-sale/brussels-city/1000/10155621"
new_real_estate_apartment_url ="https://www.immoweb.be/en/search/new-real-estate-project-apartments/for-sale?countries=BE"
new_real_estate_house_url = "https://www.immoweb.be/en/search/new-real-estate-project-houses/for-sale?countries=BE"
house_and_apartment_url = "https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE"
data_headers =[]

    
def get_characterstics_from_url(property_url):
    """
    This function takes :param: property_url
    get the raw info from the link and clean it
    return the charactererstics of a property in dictionary as targeted_data
    """
    driver.get(property_url)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser") 
    scripts = soup.find_all("script", {"type": "text/javascript"})
    pattern1 = "window.classified ="
    pattern2 = "<script>"
    pattern3 = "</script>"
    pattern4 = ";"
    
    # loop over the content of the scipts tags and keep only those match the pattern
    
    for script in scripts:
        if pattern1 in script.text:
            targeted_script = script
            break
    compiled = re.compile("(%s|%s|%s|%s)" % (pattern1,pattern2,pattern3,pattern4))
    targeted_script_regexd = compiled.sub('',targeted_script.text)
    targeted_data = json.loads(targeted_script_regexd)
    # keep only the keys of the dic which have the data of our interest
    semi_selected_data = {k:v for k,v in targeted_data.items() if k in {'id','property','price','priceType','flags'}}

    #remove data which is word and obeviously not of interest 
    for key_element in ['description','alternativeDescriptions']:
        semi_selected_data['property'].pop(key_element)

    semi_selected_flatend_dic = flatdict.FlatDict(semi_selected_data)
    semi_selceted_dic =dict(semi_selected_flatend_dic)
     
    data_headers = ['id', 'flags:isNotarySale', 'flags:isLifeAnnuitySale', 'flags:isAnInteractiveSale', 'property:type', 'property:subtype', 'property:title', 'property:name', 'property:isHolidayProperty', 'property:bedroomCount', 'property:bedrooms', 'property:bathroomCount', 'property:bathrooms', 'property:location:country', 'property:location:region', 'property:location:province', 'property:location:district', 'property:location:locality', 'property:location:postalCode', 'property:location:street', 'property:location:number', 'property:location:box', 'property:location:propertyName', 'property:location:floor', 'property:location:latitude', 'property:location:longitude', 'property:location:distance', 'property:location:approximated', 'property:location:regionCode', 'property:location:type', 'property:location:pointsOfInterest', 'property:location:placeName', 'property:netHabitableSurface', 'property:roomCount', 'property:monthlyCosts', 'property:attic', 'property:hasAttic', 'property:hasBasement', 'property:hasDressingRoom', 'property:diningRoom', 'property:hasDiningRoom', 'property:building:annexCount', 'property:building:condition', 'property:building:constructionYear', 'property:building:facadeCount', 'property:building:floorCount', 'property:energy:heatingType', 'property:energy:hasHeatPump', 'property:energy:hasPhotovoltaicPanels', 'property:energy:hasThermicPanels', 'property:energy:hasCollectiveWaterHeater', 'property:energy:hasDoubleGlazing', 'property:energy:performance', 'property:kitchen:surface', 'property:kitchen:type', 'property:laundryRoom', 'property:hasLaundryRoom', 'property:livingRoom:surface', 'property:hasLivingRoom', 'property:hasBalcony', 'property:hasBarbecue', 'property:hasGarden', 'property:gardenSurface', 'property:showerRoomCount', 'property:showerRooms', 'property:specificities', 'property:toiletCount', 'property:toilets', 'property:hasFitnessRoom', 'property:hasTennisCourt', 'property:hasSwimmingPool', 'property:hasSauna', 'property:bedroomSurface', 'property:habitableUnitCount', 'property:fireplaceCount', 'property:fireplaceExists', 'property:hasTerrace', 'property:terraceSurface', 'priceType', 'price:type', 'price:mainValue', 'price:minRangeValue', 'price:maxRangeValue']
    selected_data_dic = {k:v for k,v in semi_selceted_dic.items() if k in data_headers}

    
    return selected_data_dic




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
                
    
    return list_of_page_url



def save_pages_urls():
    """
    this function pass the pages url to get_page_url function and save the links 
    """
    
    all_pages_url_list = []
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
                if number == 2:
                    property_page_url = property_type_url
                else:
                    property_page_url = property_type_url + '&page=' + str(Number) + '&orderBy=relevance'
                try:
                    all_pages_url_list.append(get_page_urls(property_page_url))
                    # track which page the program has reached
                    print('page number: ', str(number) + ' ', property_page_url)
                except:
                    print("can't access page maybe wrong page")
                    continue

        json.dump(all_pages_url_list, fp) 
    print(all_pages_url_list)


    save_properties()
            
            
def save_properties():     
    """
    save the properties characterstics into a csv file
    """
    # open the json file containing the properties url
    with open('property_page_urls.json', 'r') as fp:
        all_pages_list = json.load(fp)

    # initialize count, to count the number of properties
    count =0
    
    
    # create and open json file to write the properites characterstics
    list_of_properties = []
    with open ('property_characterstics_data_1.json','w' ) as jf:
        print('###############   property_characterstics.json  file opened  for write   #########################')
        
        # loop over the dictionary, get a property url, with that url get the property characterstics from other fn, and save it to csv file
        for group_of_url in all_pages_list:
            for url in group_of_url:
                count += 1 
                if count == 4000:
                    json.dump(list_of_properties, jf)  
                    sys.exit()

                try: 
                    list_of_properties.append(get_characterstics_from_url(url))
                    print('number of properties retireved so far  :' ,count)
                    print('property url: ',url)
                except:
                    print('############### url not found ##################')
                    continue
        json.dump(list_of_properties, jf) 
        print("####################  finished scraping  ############################## ")   
                
                

    



def start_scrapping():
    """
     Initialize the processes  of scraping 
     
    """

    save_pages_urls()
    #save_properties()


start_scrapping()
     
    



