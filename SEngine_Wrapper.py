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


from selenium import webdriver
import time
from urllib.parse import urlparse
from selenium.webdriver.chrome.options import Options

options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-error")
options.add_argument("--ignore-ssl-errors")
caps = webdriver.DesiredCapabilities.CHROME.copy()
caps['acceptInsecureCerts'] = True
caps['acceptSslCerts'] = True
PATH = 'C:/Users/raul3/Desktop/Computer science/Year 3/chromedriver.exe'
global driver 
# Array of collected links
links = []


#Create a collection of websites for the search term using the one of the search engine. 
class Search:
    

    #main
    def __init__(self, query, urls, engine, new_sub_search_terms):
        self.query = query
        self.urls = urls
        self.engine = engine

        global driver; driver = webdriver.Chrome(PATH, options=options, desired_capabilities=caps)

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

            if engine == "google":
                self.search_google(query,on_page)

            if engine == "bing":
                self.search_bing(query,on_page)
            
            on_page += 10





    def search_bing(self,query, onPage):
        searching = 'https://www.bing.com/search?q='+ query +'&first=' + str(onPage)
        self.browse_link(searching)
        results = driver.find_elements_by_class_name('b_algo')
        self.print_links(results)



    def search_google(self, query, onPage):
        searching = 'https://www.google.com/search?q='+ query + '&start='+ str(onPage)
        self.browse_link(searching)
        results = driver.find_elements_by_class_name('g')
        self.print_links(results)


        
    #Search the search term and return page source  
    def browse_link(self, link):
        driver.get(link)

        
    



    #filter the page source code and collect website links 
    def print_links(self, results):
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
        if len(links) >= self.urls :
            print(links)
            print(len(links))
            self.write_file(links)
            driver.quit()



    # save collected links into a cvs file
    def write_file(self, list):
        file = open('queue.txt', "w")
        with file  as output:
            for item in list:
                output.write(str(item+"\n"))
        file.close()




# Inputs
search_term = input("Please enter search term\n")
get_links = input("Please enter how many sites you want to gather\n")
search_engine = input("Please select google or bing\n")
get_links = int(get_links)

sub_search_terms = input("If you'd like to change filters, write the new filters. to keep the original filters, press enter\n")

Search(search_term, get_links,search_engine,sub_search_terms )