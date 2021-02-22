# DATE DEVELOPED: 2021/02/019
# Version 1.2
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

from selenium import webdriver
from urllib.request import urlopen
import time
from selenium.common import exceptions
from urllib import parse
from autoLogin import *

# Path to chrome driver
PATH = 'C:/Users/raul3/Desktop/Computer science/Year 3/chromedriver.exe'
chrome_options = webdriver.ChromeOptions()

#remove notification alert which blocks interactivity with selenium
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)
#browser = webdriver.Chrome(PATH,chrome_options=chrome_options)
global browser


# scrape for keywords and export it into a txt file
def get_settings(user, passwrd, keyword1, keyword2):
    # Clear all content of these files
    tmp = open('xtraSettings.txt', "w")
    tmp.close()
    
    post_login = Auto_Login(user, passwrd, False)
    file =  open('queue.txt')
    with file:
        for url in file:
            # timer to slow down the loop to see what is happening
            time.sleep(3)
            page = post_login.get_Login_Page(url)
            

            # scrape for user defined keywords
            if page[0] == True:
                global browser; browser = webdriver.Chrome(PATH,chrome_options=chrome_options)

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
                    var1 = browser.find_elements_by_xpath("//*[contains(text(), '{}')]".format(keyword1))
                    if var1 != None:
                        for phrase in var1:
                            if keyword1 in phrase.text:
                                xpath = phrase.find_element_by_xpath("..")
                                found_text.append(xpath.get_attribute("outerHTML"))
                                found = True
                    if found == False:
                        var2 = browser.find_elements_by_xpath("//*[contains(text(), '{}')]".format(keyword2))
                        if var2 != None:
                            for phrase in var2:
                                if keyword2 in phrase.text:
                                    xpath = phrase.find_element_by_xpath("..")
                                    found_text.append(xpath.get_attribute("outerHTML"))
                                    found = True
                except:
                    pass    
                

                if found== False:
                    #try iframe if nothing found on normal frame
                    iframe = browser.find_elements_by_tag_name("iframe")
                    for frame in iframe:
                        try:
                            browser.switch_to.frame(frame)
                            var1 = browser.find_elements_by_xpath("//*[contains(text(), '{}')]".format(keyword1))
                            if var1 != None:
                                for phrase in var1:
                                    if keyword1 in phrase.text:
                                        xpath = phrase.find_element_by_xpath("..")
                                        found_text.append(xpath.get_attribute("outerHTML"))
                                        found = True
                            if found == False:
                                var2 = browser.find_elements_by_xpath("//*[contains(text(), '{}')]".format(keyword2))
                                if var2 != None:
                                    for phrase in var2:
                                        if keyword2 in phrase.text:
                                            xpath = phrase.find_element_by_xpath("..")
                                            found_text.append(xpath.get_attribute("outerHTML"))
                                            found = True
                            browser.switch_to.default_content()
                        except:
                            pass
      
                if found == False:
                    found_text.append("Keyword not found")
 
                # Add found security settings to file
                file = open('xtraSettings.txt', "a", encoding='utf-8')
                found = set(found_text)
                with file  as output:
                    output.write(url+"\n")
                    for data in found:
                        output.write(str(data + "\n"))
                    output.write("\n")
                    file.close()
                browser.close()






#user = input("Enter username for login")
#passwrd = input("Enter password for login")
#word1 = input("Enter keyword1")
#word2 = input("Enter replacement for keyword1")
get_settings('infinitysoftworks3@hotmail.com', 'softworks123', "verification", "authentication") 
#get_settings(user, passwrd, word1, word2)

#infinitysoftworks3@hotmail.com
#test.infinitysoftworks333@hotmail.com
#V3ryStrongP4ssword@!
#softworks123
