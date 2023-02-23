# DATE DEVELOPED: 2021/03/28
# Version 1.2
# ~ returns arrays instead of files now
# ~ Added ability to extract DOM of the keyword.
# ~ Moved login function into its ownn class 
# ~ Changed security scraping method to involve human intervention to find the correct page
# ~ Works with trainline, facebook, myprotien,
# ~ Modified the code, placed essential bits into a new files for high cohesion and avoid copy and pasting same code when needed.
#
# V1.1 changes made:
# ~ going to Login now works for all sites tested so far
# ~ got iframe access and now can access data from it
# ~ Can sigin into trainline - according to Shujun it is difficult
# ~ Cleaned up code
#
# Version 1.0 chanegs made: 
# ~ created a scraper to collect input feilds on a login page
# ~ enter login details using the input feilds 
# ~ added universal cookie accepter
# ~ cleaned up the code and removed duplicates to increase computational time
# ~ Added get_Login_Page function
# ~ Addedd get_Settings function (half finished):
# ~ Settings function gets the security/ settings page atm (still need to navigate to pasword section and collect all info)
# ~ Not able to access iframe content
# ~ changed chnagrd input scraper from dictionary to a default dictionary will allows the storeage lf multiple values for the same key(id or name)
#
#
# WRITTEN BY: Raul Rasciclal(rr355)
# Date Tested: 20201/02/19
# Description: scrape for keyword from logged in website
"""caller file for AutoLogin.py where it will login and scrape paramters passed on the given page.

Caller file for AutoLogin.py to login a user with username and password over an array of urls and return the urls that failed

Edit PATH by adding path to your chrome driver

typical usage case:
import post_login_sec_srape
arr = ["https://www.google.com","https://www.bing.com"]
post_login_sec_srape.get_settings("USERNAME1241","Pa55word!","secuirty","Account",arr)
"""
from selenium import webdriver
import time 
import auto_login 

# Path to chrome driver
PATH = 'PATH TO CHROME DRIEVR'
chrome_options = webdriver.ChromeOptions()

#remove notification alert which blocks interactivity with selenium
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)
#browser = webdriver.Chrome(PATH,chrome_options=chrome_options)
global browser


def get_settings(user, passwrd, keyword1, keyword2, stay_loggedin, sites ):
    """scrape for keywords and export it into a txt file

    logs into passed array of urls indivdualy records whether the array fails
    logs into site using Username and password values passed to function
    scrapes the website for a value passed to it once logged in.

    Args:
        user (str): username to login as 
        passwrd (str): password to login with
        keyword1 (str): primary keyword to search for on the webpage
        keyword2 (str): backup search term to look for on the webpage
        urls [arr]: array of strings containing urls

    Returns:
        failed_urls [arr]: array of strings of each url that failed to login for human review.
        extra_settings[arr]: array of details scraped from the webpage.
    """


    # Clear all content of these files
    st = stay_loggedin
    
    extra_settings = []

    failed_urls = []
    post_login = auto_login.Auto_Login(user, passwrd, False)


    if st == False:
        for url in sites:
            # timer to slow down the loop to see what is happening
            time.sleep(3)
            
            page = post_login.get_Login_Page(url)
            
            # scrape for user defined keywords
            if page[0] == True:
                global browser; browser = webdriver.Chrome(options=chrome_options)
                url = page[1]
                browser.get(url)
                # Add Cookies and log in
                for cookie in page[2]:
                    browser.add_cookie(cookie)
                browser.get(url)
                time.sleep(2)
                #~~~~~~~~~~~~~ Start navigating to the page where you want to extract info from~~~~~~~~~~~~~~~~~~~~~~
                # can extend time based on how long it takes to navigate, currently 15 seconds
                found_text = []
                found = False
                try:
                    body = browser.find_element_by_tag_name("body")
                    var1 = body.find_elements_by_xpath("//*[contains(text(), '{}')]".format(keyword1))
                    if var1 != None:
                        for phrase in var1:
                            if keyword1 in phrase.text:
                                a = phrase.find_element_by_xpath("..")
                                found_text.append(a.get_attribute("outerHTML"))
                                found = True
                    if found == False:
                        var2 = body.find_elements_by_xpath("//*[contains(text(), '{}')]".format(keyword2))
                        if var2 != None:
                            for phrase in var2:
                                if keyword2 in phrase.text:
                                    a = phrase.find_element_by_xpath("..")
                                    found_text.append(a.get_attribute("outerHTML"))
                                    found = True
                except:
                    pass    
                
                if found== False:
                    #try iframe if nothing found on normal frame
                    iframe = browser.find_elements_by_tag_name("iframe")
                    for frame in iframe:
                        try:
                            browser.switch_to.frame(frame)
                            body = browser.find_element_by_tag_name("body")
                            var1 = body.find_elements_by_xpath("//*[contains(text(), '{}')]".format(keyword1))
                            if var1 != None:
                                for phrase in var1:
                                    if keyword1 in phrase.text:
                                        a = phrase.find_element_by_xpath("..")
                                        found_text.append(a.get_attribute("outerHTML"))
                                        found = True
                            if found == False:
                                var2 = body.find_elements_by_xpath("//*[contains(text(), '{}')]".format(keyword2))
                                if var2 != None:
                                    for phrase in var2:
                                        if keyword2 in phrase.text:
                                            a = phrase.find_element_by_xpath("..")
                                            found_text.append(a.get_attribute("outerHTML"))
                                            found = True
                            browser.switch_to.default_content()
                        except:
                            pass
                        
                if found == False:
                    found_text.append("Keyword not found")

                extra_settings.append([url, found_text])
                browser.close()

            else:
                failed_urls.append(page[3])


    return extra_settings, failed_urls
