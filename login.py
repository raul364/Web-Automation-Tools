# DATE DEVELOPED: 2021/02/19
#
# Version 1.0 chanegs made: 
# ~ Added ability to login to a website or a list of websites.
#
#
# WRITTEN BY: Raul Rasciclal(rr355)
# Date Tested: 2021/02/19
# Description: login into given website




from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.request import urlopen
import time
from selenium.common import exceptions
from urllib import parse
from autoLogin import *




# Path to chrome driver
PATH = 'ENTER PATH TO CHROME DRIVER'
chrome_options = webdriver.ChromeOptions()

#remove notification alert which blocks interactivity with selenium
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)
#browser = webdriver.Chrome(PATH,chrome_options=chrome_options)
global browser

def login_to_site(user, passwrd):
    tmp = open('manualLogin.txt', "w")
    tmp.close()

    post_login = Auto_Login(user, passwrd, True)
    file =  open('queue.txt')
    with file:
        for url in file:
            # timer to slow down the loop to see what is happening
            time.sleep(2)
            page = post_login.get_Login_Page(url)
            


#user = input("Enter username for login")
#passwrd = input("Enter password for login")
login_to_site(user, passwrd)
