#!/usr/local/bin/python3
# LAST DATE DEVELOPED: 2021/02/20
# WRITTEN BY: Raul Rasciclal(rr355)
# Date Tested: YYYY/MM/DD
# Description: Generate list of links based on the search term
#   
# Version 1.2:
# ~ Changed variable names
# ~ Filter added so no duplicates are added and a domain is added only once.
# ~ Fixed issue on crawler only crawling the first page.
# ~ cleaned up code, removed unessessery bits
# ~ Added functionality for the user to edit the filters   
# 
# Version 1.1 chanegs made:
# ~ Fixed issues with the search filters not working
# ~ cleaned up code
#
#
# Version 1.0 chanegs made: 
# ~ corrected variable names using the convetion applied
# ~ Changed output file to csv file  
# ~ Added user input gui to enable interaction with user.

"""gathers_Links from google or bing and writes them to a file

opens bing or google and searches for the query
will search google or bing and search for the query until the required number of urls are gathered
then write to file once urls are gathered.

typical usage case:
import gather_Links
arr = []
gather_Links.search("Account",10,True,["register","create"])
"""
from selenium import webdriver
import time
from urllib.parse import urlparse
from selenium.webdriver.chrome.options import Options
import os
import cgi
import cgitb
cgitb.enable(display=0,logdir='scripts/data/')

options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-error")
options.add_argument("--ignore-ssl-errors")
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
caps = webdriver.DesiredCapabilities.CHROME.copy()
caps['acceptInsecureCerts'] = True
caps['acceptSslCerts'] = True
# Array of collected links
links = []
driver = None


#Create a collection of websites for the search term using the one of the search engine. 
class Search:
    """opens bing or google and searches for the query
    will search google or bing and search for the query until the required number of urls are gathered
    then write to file once urls are gathered.
    
    Args:
        query (str): string of primary keyword
        urls (int): number of urls to gather
        engine (Boolean/str):boolean or string value to say what search engine to use True=google False=bing
        new_sub_search_terms (str): a string or array of strings to use in combination withh the query to gather extra urls. 
    """
    

    #main
    def __init__(self, query, urls, engine, new_sub_search_terms):
        self.query = query
        self.urls = urls
        self.engine = engine

        global driver; driver = webdriver.Chrome(options=options, desired_capabilities=caps)

        if new_sub_search_terms !="":
            sub_search_terms = new_sub_search_terms.split(",")
            sub_search_terms.insert(0, "")
        else:
            sub_search_terms = [""]
        
        #sets an even limit to how many sites each filter produces
        self.urls_for_filter = urls/len(sub_search_terms)
        on_page = 0
        count = 0
        i=0
        tmp =0
        #using the desired search engine, search the query for websites 
        while len(links) < urls:
            count = len(links)
            #Check if count is the same number as the urlsForFilter, if it is change filter
               
            if tmp != int(count/self.urls_for_filter) and tmp != len(sub_search_terms):
                i = i+1
                on_page =0
                tmp = int(count/self.urls_for_filter)
                query = self.query + sub_search_terms[i]
            if engine == "true" or engine == "google"or engine ==True:
                self.search_google(query,on_page)
            elif engine == "false" or engine =="bing"or engine == False:
                self.search_bing(query,on_page)
            else:
                raise Exception("engine value not defined or not in range")
            on_page += 10
        self.write_file()
        self.return_array()
        

    
    def search_bing(self,query, onPage):
        """opens bing and gathers links
        
        search bing for the query and return a list of all links
        Args:
            query (str): string of search term to find
            onPage (int): offset number of urls to request back
        """

        searching = 'https://www.bing.com/search?q='+ query +'&first=' + str(onPage)
        self.browse_link(searching)
        results = driver.find_elements_by_class_name('b_algo')
        self.print_links(results)

    
    def search_google(self, query, onPage):
        """opens google and gathers links
        
        search google for the query and return a list of all links
        Args:
            query (str): string of search term to find
            onPage (int): offset number of urls to request back
        """

        searching = 'https://www.google.com/search?q='+ query + '&start='+ str(onPage)
        self.browse_link(searching)
        results = driver.find_elements_by_class_name('g')
        self.print_links(results)


        
    def browse_link(self, link):
        """Search the search term and return page source  
        
        Search the search term and return page source  
        Args:
            query (str): string of search term to find
            onPage (int): offset number of urls to request back
        """

        driver.get(link)

        
    
       
    def print_links(self, results):
        """filter the page source code and collect website links 
        
        filter the page source code and collect website links 
        Args:
            results [arr]: all link from websource in an arr of strings
        """

        #select all links from the web source and add them to an array
        for res in results:
            if len(links) < self.urls:
                # Checks if each link is present and not already in the array, else, raise exception
                try:
                    link = res.find_element_by_tag_name('a').get_attribute("href")
                    check1 = urlparse(link).netloc
                    check2 = ('.'.join(check1.split('.')[1:]))
                    
                    if any(check2 in  i for i in links):
                        continue
                    else:
                        links.append(link)
                except Exception as e:
                    print(e)
                    continue
        print("Gathered " + str(len(links)) +" links")

      
    def return_array(self):
        """return array of links gathered
        returns
            links [arr]: array of strinngs containing urls
        """

        # return links when collection amount met.
        
        #driver.close()
        driver.quit()
        return links
            
      
    def write_file(self):
        """save collected links into a cvs file
        outputs array values of links to a given file
        """

        file = open('/scripts/data/queue.txt', "w")
        for item in links:
            file.write(str(item+"\n"))
        file.close()
