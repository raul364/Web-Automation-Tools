# Author: Raul Rasciclal (rr355)
# Last Date developed: 2021/02/18
# Version 1.0
# ~ Implemented Captcha interactor and solver
# ~ Implemented extra secuirty code
# ~ Implemented cookie acceptor
# ~ Added ability to make log of failed websites.
# ~ clicks any button resembling login from base url/any url
# ~ Added ability to skip search for login button if the url contains login
# ~ Integrated Cookie pop up acceptor
# ~ tidyed up the code, removed variables and imports which had no functionality
# ~Added login() function which logs the user into the website
#
# get login page from base url
##################################################################################
#
# ----------------------INSTRUCTIONS--------------
# 1. import this file (from autoLogin import *)
# 2. call autoLogin and parse username, password, boolean. parse False to give 15 seconds to user to navigate to a certain page.
# 3. call get_login_page and parse url.
#
#
#

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import urllib
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.parse import urlparse
from collections import defaultdict
import time
import re
from selenium.common import exceptions
from Captcha import *

# Path to chrome driver
PATH = 'C:/Users/raul3/Desktop/Computer science/Year 3/chromedriver.exe'

# Setup browser to be chrome and accept all notification
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--ignore-certificate-error")
chrome_options.add_argument("--ignore-ssl-errors")
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)
caps = webdriver.DesiredCapabilities.CHROME.copy()
caps['acceptInsecureCerts'] = True
caps['acceptSslCerts'] = True
browser = webdriver.Chrome(PATH, options=chrome_options, desired_capabilities=caps)



# VARIABLES
base = lambda x:'{uri.scheme}://{uri.netloc}/'.format(uri=x)

#############################################

class Auto_Login():

    def __init__(self, user, passwrd, stay_loggedin):
        self.user = user
        self.passwrd = passwrd
        self.stay_loggedin = stay_loggedin

        
        

    # get main page and then navigate to login page unless url is alreay at login page
    def get_Login_Page(self, site):


        # Check if url is already at login page
        if "signin" in site or "ogin" in site:
            try:
                browser.get(site)
                url = self.login()
                return url   
            except Exception as e:
                print(e)
        # get base url from the parsed url
        else:
            parsed_Url = urlparse(site)
            site = base(parsed_Url)
            try:
                browser.get(site)
            except Exception as e:
                print(e)


        ######################################################################################


        # If cookie popup comes up, accept them 
        Options = ['Accept', 'ACCEPT ALL', 'Agree', 'Yes','AGREE']
        for i in Options:
            cookies = browser.find_elements_by_xpath("//*[contains(text(), '{}')]".format(i))
            for cookie in cookies:
                if cookie != None:
                    try:
                        class1 = cookie.get_attribute('class')
                        if class1 != None or class1 != "":
                            accept_cookie =(By.XPATH, "//*[@class='{}']".format(class1))
                            WebDriverWait(browser, 3).until(EC.element_to_be_clickable(accept_cookie)).click()
                    except:
                        pass
                    
                    try:
                        id1 = cookie.get_attribute('id')
                        if id1 != None or id1 != "": 
                            accept_cookie =(By.XPATH, "//*[@id='{}']".format(id1))
                            WebDriverWait(browser, 3).until(EC.element_to_be_clickable(accept_cookie)).click()
                    except:
                        pass
                    

        #########################################################################################

        # wait until popup goes away 
        time.sleep(2)
        # Boolean to try different methods if one fails
        try_different =False    
        # From base url go to login page
        link = site
        soup = BeautifulSoup(browser.page_source, 'html.parser')

        # Filters to look for to find login button
        login_filters = ["Login", "login" "Log in", "log in", "Signin","Sign in", "signin"]

        # Try all filters till login button is found
        for i in login_filters:
            check = soup.findAll('a',text=re.compile(i,re.I))
            if check != None:
                for element in check:
                    href = element.get("href")
                    if href:
                        if "https://" in href:
                            browser.get(href)
                            try_different = False
                            break
                        else:
                            # If link doesn't have full address(www.xxxxxx.xxxx)
                            link = site + href
                            print(link)
                            browser.get(link)
                            try_different = False
                            break
                    else:
                        try_different = True
                        continue   
                    break 

        # if none of the filters worked, try injecting login to the url
        if(try_different == True):
            try:
                link= site + 'login'
                browser.get(link)
                try_different = False
            except urllib.error.HTTPError as err:
                if err.code == 404: print("Page not found")
                try_different = True
            if(try_different == True):
                try:
                    link= site + 'signin'
                    browser.get(link)
                    try_different = False
                except HTTPError as err:
                    if err.code == 404: print("Page not found")
                    try_different = True 
            if(try_different == True):
                print("can't find login page :"+ site)


        url = self.login()
        return url






    # Enter login details and login
    def login(self):
        # Check if captcha is on page and solve it
        is_captcha = self.check_captcha()
        if is_captcha == True:
            self.get_captcha_sound()
        login_url = browser.current_url

        get_names = defaultdict(list)
        get_id = defaultdict(list)

        fields = browser.find_elements_by_tag_name("input")

        for field in fields:
            # Get felid type and get name for sites that use name tag
            k = field.get_attribute('type')
            v = field.get_attribute('name')
            get_names[k].append(v)
            # Get feild type and get id for sites that use id
            k1 = field.get_attribute('type')
            v1 = field.get_attribute('id')
            get_id[k1].append(v1)
            
        # Enter Login details
        if 'email' in get_names:
            for i in get_names['email']:
                try:
                    user_login = (By.XPATH, "//*[@name='{}']".format(i))
                    username = WebDriverWait(browser, 5).until(EC.element_to_be_clickable(user_login))
                    username.clear()
                    username.send_keys(self.user)
                    username.send_keys(Keys.RETURN)
                except:
                    pass
                
        elif 'email' in get_id:
            for i in get_id['email']:
                try:
                    user_login = (By.XPATH, "//*[@id='{}']".format(i))
                    username = WebDriverWait(browser, 5).until(EC.element_to_be_clickable(user_login))
                    username.clear()
                    username.send_keys(self.user)
                    username.send_keys(Keys.RETURN)
                except:
                    pass
                
        else:
            if 'text' in get_id:
                for i in get_id['text']:
                    try:
                        user_login = (By.XPATH, "//*[@id='{}']".format(i))
                        username = WebDriverWait(browser, 5).until(EC.element_to_be_clickable(user_login))
                        username.clear()
                        username.send_keys(self.user)
                        username.send_keys(Keys.RETURN)
                    except:
                        pass
                    
            else:
                for i in get_names['text']:
                    try:
                        user_login = (By.XPATH, "//*[@name='{}']".format(i))
                        username = WebDriverWait(browser, 5).until(EC.element_to_be_clickable(user_login))
                        username.clear()
                        username.send_keys(self.user)
                        username.send_keys(Keys.RETURN)
                    except:
                        pass
                    
        # Check if captcha is on page and solve it
        is_captcha = self.check_captcha()
        if is_captcha == True:
            self.get_captcha_sound()

        if 'password' in get_names:
            for i in get_names['password']:
                try:
                    user_pass = (By.XPATH, "//*[@name='{}']".format(i))
                    password_element = WebDriverWait(browser, 10).until(EC.element_to_be_clickable(user_pass))
                    password_element.clear()
                    password_element.send_keys(self.passwrd)
                    password_element.send_keys(Keys.RETURN)
                except:
                    pass
                
        else:
            for i in get_id['password']:
                try:
                    user_pass = (By.XPATH, "//*[@id='{}']".format(i))
                    password_element = WebDriverWait(browser, 10).until(EC.element_to_be_clickable(user_pass))
                    password_element.clear()
                    password_element.send_keys(self.passwrd)
                    password_element.send_keys(Keys.RETURN)
                except:
                    pass
                
                
        # If unable to login, add url to manual login file.
        successful = True
        time.sleep(2)
        url = browser.current_url
        if url == login_url:
            file = open('manualLogin.txt', "a")
            with file  as output:
                output.write(url+"\n")
                file.close()
            successful = False
        
        is_captcha = self.check_captcha()
        if is_captcha == True:
            self.get_captcha_sound()



        # open new tab if stay_loggedin is True otherwise return url and cookies
        if self.stay_loggedin == True:
            browser.execute_script("window.open('');")
            tab = browser.window_handles
            browser.switch_to_window(tab[-1])
            return successful
        else:
            time.sleep(20)
            url = browser.current_url
            allCookies = browser.get_cookies()
            browser.execute_script("window.open('');")
            tab = browser.window_handles
            browser.switch_to_window(tab[-1])
            return successful, url, allCookies


        
        





    # Check if captcha is on the page
    def check_captcha(self):
        iframe = browser.find_elements_by_tag_name("iframe")
        for frame in iframe:
            try:
                browser.switch_to.frame(frame)
                captcha_box = browser.find_element_by_id("recaptcha-anchor")
                if captcha_box != None:
                    return True
                browser.switch_to.default_content()
            except:
                browser.switch_to.default_content()
                pass
        return False





    # Interact With Captcha
    def get_captcha_sound(self):
        iframe = browser.find_elements_by_tag_name("iframe")
        for frame in iframe:
            try:
                browser.switch_to.frame(frame)
                captcha_box = browser.find_element_by_id("recaptcha-anchor")
                if captcha_box != None:
                    captcha_box.click()
                browser.switch_to.default_content()
            except:
                browser.switch_to.default_content()
                pass


        iframe2 = browser.find_elements_by_tag_name("iframe")
        for frame in iframe2:
            try:  
                browser.switch_to.frame(frame)
                audio = browser.find_element_by_id("recaptcha-audio-button")
                if audio != None:
                    audio.click()
                browser.switch_to.default_content()
            except:
                browser.switch_to.default_content()
                pass
        solved = " "
        iframe3 = browser.find_elements_by_tag_name("iframe")
        for frame in iframe3:
            try:  
                browser.switch_to.frame(frame)
                download = browser.find_element_by_tag_name("audio")
                print(download.get_attribute("src"))
                src = download.get_attribute("src")
                solved = main(src) 
                browser.switch_to.default_content()
            except:
                browser.switch_to.default_content()
                pass
        iframe4 = browser.find_elements_by_tag_name("iframe")
        for frame in iframe4:
            try:  
                browser.switch_to.frame(frame)
                response = browser.find_element_by_id("audio-response")
                # Sleep so you dont get caught by google as bot
                time.sleep(5)
                response.send_keys(solved)
                browser.switch_to.default_content()
            except:
                browser.switch_to.default_content()
                pass
        iframe5 = browser.find_elements_by_tag_name("iframe")
        for frame in iframe3:
            try:  
                browser.switch_to.frame(frame)
                response = browser.find_element_by_id("recaptcha-verify-button")
                response.click()
                browser.switch_to.default_content()
            except:
                browser.switch_to.default_content()
                pass



    


#wait = input("Enter waiting time (seconds) for crawler")
#user = input("Enter username for login")
#passwrd = input("Enter password for login")
#iterate(wait, user, passwrd)
#Auto_Login('infinitysoftworks3@hotmail.com', 'softworks123',True)