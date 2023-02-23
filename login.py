# DATE DEVELOPED: 2021/03/28
#
# Version 1.0 chanegs made: 
# ~ Returns an array of failed urls
# ~ Added ability to login to a website or a list of websites.
#
#
# WRITTEN BY: Raul Rasciclal(rr355)
# Date Tested: 2021/03/28
# Description: login into given website




from selenium import webdriver
import time
from auto_login import *
"""caller file for AutoLogin.py where it will login and wait

Caller file for AutoLogin.py to login a user with username and password over an array of urls and return the urls that failed

Edit PATH by adding path to your chrome driver 

typical usage case:
import login
arr = ["]
login.login_to_site("USERNAME1241", "Pa55word!", [array of URLs])
"""



# Path to chrome driver
PATH = 'PATH TO CHROME DRIVER'
chrome_options = webdriver.ChromeOptions()

#remove notification alert which blocks interactivity with selenium
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)
#browser = webdriver.Chrome(PATH,chrome_options=chrome_options)
global browser

def login_to_site(user, passwrd, urls):
    """login to site using paramters passed

    logs into passed array of urls indivdualy records whether the array fails
    logs into site using Username and password values passed to function
    
    Args:
        user (str): username to login as
        passwrd (str): password to login with
        urls [arr]: array of strings containing urls
    
    Returns:
        failed_urls [arr]: array of strings of each url that failed to login for human review.
    """




    # array of URLs which need revisiting
    failed_urls = []

    post_login = auto_login(user, passwrd, True)
    
    for url in urls:
        # timer to slow down the loop to see what is happening
        time.sleep(2)
        page = post_login.get_Login_Page(url)
        
        if page[1] != 0:
            failed_urls.append(page[1])

    return failed_urls
