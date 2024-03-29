# Author: Raul Rasciclal (rr355)
# Last Date developed: 2021/04/01
# Version 1.0
# ~ Added documentation
# ~ Added missing feature to click button from base url
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
# EDIT PATH by adding path to your chrome driver
# 1. import this file (from autoLogin import *)
# 2. call autoLogin and parse username, password, boolean. parse False to give 15 seconds to user to navigate to a certain page.
# 3. call get_login_page and parse url.
#

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import urllib
from urllib.error import HTTPError
from urllib.parse import urlparse
from collections import defaultdict
import time
import re
from selenium.common import exceptions
from ..audio_captcha_solver import *

# Path to chrome driver
PATH = 'PATH TO CHROME DRIVER'

# Set webdriver to chrome and accept all notification
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--ignore-certificate-error")
chrome_options.add_argument("--ignore-ssl-errors")
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)
caps = webdriver.DesiredCapabilities.CHROME.copy()
caps['acceptInsecureCerts'] = True
caps['acceptSslCerts'] = True
browser = webdriver.Chrome(PATH, options=chrome_options, desired_capabilities=caps)




# Lambda function to extract base url (homepage) from given url
base = lambda x:'{uri.scheme}://{uri.netloc}/'.format(uri=x)

#############################################

class Auto_Login():
  
    def __init__(self, user, passwrd, stay_loggedin):
        """
        A class which attempts to log a user into a website given a url.
        returning a boolean indicating success or fail and a url if failed.

        Args:
            user (str): username
            passwrd (str): password
            stay_loggedin (bool): True if you want the tabs remain open after logging in
                                  False if you want to close the tabs after logging in.

        """
        self.user = user
        self.passwrd = passwrd
        self.stay_loggedin = stay_loggedin

        
        

    # get main page and then navigate to login page unless url is alreay at login page
    def get_Login_Page(self, site):
        """
        Attempt to navigate to the login page of the given website and login.
        
        Args:
            site (str): website to login to.

        returns:
            if staylogged in = True:
            successful(bool)
            failder_url (str/int): if succesful is True failed url is 0 
    
            if staylogged in = False:
            successful(bool)
            url (str/int) if succesful is True url is str 
            cookies (str)
            failed_url (str/int): if succesful is True failed url is 0 
        """


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
                        cookie.click()
                    except:
                        try:
                            class1 = cookie.get_attribute('class')
                            if class1 != None or class1 != "":
                                accept_cookie =(By.XPATH, "//*[@class='{}']".format(class1))
                                WebDriverWait(browser, 3).until(EC.element_to_be_clickable(accept_cookie)).click()
                        except:
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
        try_different = True    
        # From base url go to login page
        link = site
        soup = BeautifulSoup(browser.page_source, 'html.parser')


        inputs = browser.find_elements_by_tag_name("input")
        try:
            for i in inputs:
                check = i.get_attribute("type")
                if "password" == check:
                    url = self.login()
                    return url
        except:
            pass
       

        # Filters to look for to find login button
        login_filters = ["Login", "login","LOG IN", "Log in", "log in", "Signin","Sign in", "signin"]
        for i in login_filters:
            try:
                check = browser.find_elements_by_xpath("//*[contains(text(), '{}')]".format(i))
                if check != None:
                    for element in check:
                        try:
                            parent = element.find_element_by_xpath("..")
                            button = parent.find_element_by_tag_name("button")
                            button.click()
                            url = self.login()
                            return url
                        except:
                            pass
            except:
                pass


            check = soup.findAll('a',text=re.compile(i,re.I))
            if check != None:

                for element in check:
                    try:
                        parent = element.find_element_by_xpath("..")
                        button = parent.find_element_by_tag_name("button")
                        button.click()
                        url = self.login()
                        return url
                    except:
                        pass

                    href = element.get("href")
                    if href:
                        if "https://" in href:
                            browser.get(href)
                            try_different = False
                            break
                        else:
                            # If link doesn't have full address(www.xxxxxx.xxxx)
                            if site[-1:] == '/':
                                site = site[:-1]
                            link = site + href
                            print(link)
                            print("line 186")
                            browser.get(link)
                            try_different = False
                            break
                    else:
                        try_different = True
                        continue   

            if try_different ==  False:
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
        """
        helper function for get_login_page()
        attempts to login by parsing user details into the correct user and password fields on the page.

        returns:
            if staylogged in = True:
            successful(bool)
            failder_url (str/int): if succesful is True failed url is 0 

            if staylogged in = False:
            successful(bool)
            url (str/int) if succesful is True url is str 
            cookies (str)
            failed_url (str/int): if succesful is True failed url is 0 

        """
        # Check if captcha is on page and solve it
        is_captcha = self.check_captcha()
        if is_captcha == True:
            self.get_captcha_sound()
        login_url = browser.current_url

        get_names = defaultdict(list)
        get_id = defaultdict(list)
        get_class = defaultdict(list)

        fields = browser.find_elements_by_tag_name("input")

        for field in fields:
            # find type, name, id, and class attributes and add to dictionaries.
            k = field.get_attribute('type')
            v = field.get_attribute('name')
            v1 = field.get_attribute('id')
            v2 = field.get_attribute('class')

            get_names[k].append(v)
            get_id[k].append(v1)
            get_class[k].append(v2)

        worked = False


        # Enter Login details
        if 'email' in get_names and not '' in get_names['email']:
            print("line 255")
            for i in get_names['email']:
                try:
                    user_login = (By.XPATH, "//*[@name='{}']".format(i))
                    username = WebDriverWait(browser, 5).until(EC.element_to_be_clickable(user_login))
                    username.clear()
                    username.send_keys(self.user)
                    username.send_keys(Keys.RETURN)
                except:
                    pass
                
        elif 'email' in get_id and not '' in get_id['email']:
            print("line 267")
            for i in get_id['email']:
                try:
                    user_login = (By.XPATH, "//*[@id='{}']".format(i))
                    username = WebDriverWait(browser, 5).until(EC.element_to_be_clickable(user_login))
                    username.clear()
                    username.send_keys(self.user)
                    username.send_keys(Keys.RETURN)
                except:
                    pass


        elif 'email' in get_class:
            for i in get_class['email']:
                try:
                    print("line 281")
                    user_login = (By.XPATH, "//*[@class='{}']".format(i))
                    username = WebDriverWait(browser, 5).until(EC.element_to_be_clickable(user_login))
                    x = browser.find_element_by_class_name(i).click()
                    username.click()
                    username.clear()
                    username.send_keys(self.user)
                    username.send_keys(Keys.RETURN)
                except:
                    pass
                
        else:
            
            if 'text' in get_id and not '' in get_id['text']:
                for i in get_id['text']:
                    try:
                        user_login = (By.XPATH, "//*[@id='{}']".format(i))
                        username = WebDriverWait(browser, 5).until(EC.element_to_be_clickable(user_login))
                        username.clear()
                        username.send_keys(self.user)
                        username.send_keys(Keys.RETURN)
                    except:
                        pass

                    
            elif 'text' in get_names and not '' in get_names['text']:
                for i in get_names['text']:
                    try:
                        user_login = (By.XPATH, "//*[@name='{}']".format(i))
                        username = WebDriverWait(browser, 5).until(EC.element_to_be_clickable(user_login))
                        username.clear()
                        username.send_keys(self.user)
                        username.send_keys(Keys.RETURN)
                    except:
                        pass


            else:
                for i in get_class['text']:
                    try:
                        user_login = (By.XPATH, "//*[@class='{}']".format(i))
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



        if 'password' in get_names and not '' in get_names['password']:
            for i in get_names['password']:
                try:
                    user_pass = (By.XPATH, "//*[@name='{}']".format(i))
                    password_element = WebDriverWait(browser, 10).until(EC.element_to_be_clickable(user_pass))
                    password_element.clear()
                    password_element.send_keys(self.passwrd)
                    password_element.send_keys(Keys.RETURN)
                except:
                    pass

                
        elif 'password' in get_id and not '' in get_id['password']:
            for i in get_id['password']:
                try:
                    user_pass = (By.XPATH, "//*[@id='{}']".format(i))
                    password_element = WebDriverWait(browser, 10).until(EC.element_to_be_clickable(user_pass))
                    password_element.clear()
                    password_element.send_keys(self.passwrd)
                    password_element.send_keys(Keys.RETURN)
                except:
                    pass

        else:
            for i in get_class['password']:
                try:
                    user_pass = (By.XPATH, "//*[@class='{}']".format(i))
                    password_element = WebDriverWait(browser, 10).until(EC.element_to_be_clickable(user_pass))
                    password_element.click()
                    password_element.clear()
                    password_element.send_keys(self.passwrd)
                    password_element.send_keys(Keys.RETURN)
                except:
                    pass
                
                
        # If unable to login, add url to manual login file.
        successful = True
        time.sleep(2)
        url = browser.current_url
        failed_url = 0
        if url == login_url:
            failed_url = url
            successful = False

      
        is_captcha = self.check_captcha()
        if is_captcha == True:
            self.get_captcha_sound()



        # open new tab if stay_loggedin is True otherwise return url and cookies
        if self.stay_loggedin == True:
            browser.execute_script("window.open('');")
            tab = browser.window_handles
            browser.switch_to_window(tab[-1])
            return successful, failed_url
        else:
            time.sleep(20)
            url = browser.current_url
            allCookies = browser.get_cookies()
            browser.execute_script("window.open('');")
            tab = browser.window_handles
            browser.switch_to_window(tab[-1])
            return successful, url, allCookies, failed_url


       



    # Check if captcha is on the page
    def check_captcha(self):
        """
        check if CAPTCHA is present on the current page

        returns:
            bool
        """
        iframe = browser.find_elements_by_tag_name("iframe")
        for frame in iframe:
            try:
                browser.switch_to.frame(frame)
                captcha_box = browser.find_element_by_id("recaptcha-anchor")
                if captcha_box != None:
                    browser.switch_to.default_content()
                    return True
                browser.switch_to.default_content()
            except:
                browser.switch_to.default_content()
        return False





    # Interact With Captcha
    def get_captcha_sound(self):
        """
        Interact with CAPTCHA audio segment and solve the CAPTCHA.
        """

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
                

        time.sleep(2)
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
                
        iframe5 = browser.find_elements_by_tag_name("iframe")
        for frame in iframe3:
            try:  
                browser.switch_to.frame(frame)
                response = browser.find_element_by_id("recaptcha-verify-button")
                response.click()
                browser.switch_to.default_content()
            except:
                browser.switch_to.default_content()
                
