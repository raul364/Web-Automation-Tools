# DATE DEVELOPED: 2020/16/10
# Version 1
# WRITTEN BY: Rahul Patel (Rpp20)
# Date Tested: 
# Description: Loops through URLS and attempts to automatically fill in registration forms
#              and create accounts. Some boxes are unable to be identified and so there will be 
#              time for manual intervention to complete registration for each url 
#              

"""a bot that attempts to create accounts on various websites automatically with the potential need for human interaction

takes URLS in the form of an array variable or file and begins by navigating to the signup page, filling out the generic form fields
and submitting the form in an attempt to create account. 15 Seconds is also given at the end for human interaction if the full form could not 
done so automatically. 

will return a array of websites that accounts were not created for as well as 2 text files. 1 with completed urls
and 2 with websites that were successful.
    Typical useage example:
    sendString(["https://signup.com/", "https://accounts.google.com/signup?hl=en"]
    OR
    sendFile() - Where the filepath variable on line 68 is changed to locate a .txt file containing URLS OR the filepath is entered in the brackets


"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import pandas as pd
from bs4 import BeautifulSoup
import time
import re
#from find_signup_page import *
from ..audio_captcha_solver import *

HumanInteractionRec = []
global arr 

###############Variables#################
first_name = "John"
last_name = "Smith"
emoji_pass = "🍩🍩🍩🍩🍩🍩🍩🍩🍩🍩"

#Remove # at start of line below to allow user to enter their own email to be used and remove hard coded email line (2 below)
#email = input("Please enter your email address: ")
email = "EMAIL

#strong_pass = input("Please enter a strong password (min 8 characters, include min 1 upper case, number and symbol): ")
strong_pass = "V3ryStrongP4ssword@!"

#Initilisation (Change PATH when running on new machine)
PATH = 'PATH TO CHROMEDRIVER'

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)
browser = webdriver.Chrome(PATH,chrome_options=chrome_options)

#If you wish to run program using array, then list urls here below
#OR run command sendString(Array) where Array is your Array of URLS all in command line
#eg sendString(["https://signup.com/"] OR sendString(URLS)
URLS = ["https://signup.com/", "https://accounts.google.com/signup?hl=en"]

#Program can also be run with a file, simply change the file path below to file location
#run sendFile()
filepath = 'FILEPATH FOR WEBSITES


###########################################
def sign_up():
    
    """
    check if CAPTCHA is present on the current page

    returns:
        bool
    """

    # Check if captcha is on the page
    def check_captcha():
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
                pass
        return False
    # Interact With Captcha

    """
    Interact with CAPTCHA audio segment and solve the CAPTCHA.
    """
    def get_captcha_sound():
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
                time.sleep(6)
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

    ###########################################################################

    #Clears the text document everytime the program is run
    f = open("manual_intervention_required.txt", "w")
    f.write("")
    f.close()

    

    #signup_page = Auto_Login()

    #loops URLS
    #file = open('queuet.txt')
    #with file:
    for url in arr:
        #page = signup_page.get_signup_Page(url)
        browser = webdriver.Chrome(PATH)
        browser.get(url)
        time.sleep(2)
        is_captcha = check_captcha()
        if is_captcha == True:
            get_captcha_sound()
        # SECTION WRITTEN BY: RAUL RAS (RR355) EDITED BY Rahul P (RPP20)
        # This code accepts cookie popups that some websites may display 
        # Which need to be accpeted before we can interact with it.

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
        #################################
        time.sleep(3)


        """Finds the sign up page from base url

        Loops over an array of filters which are generically buttons that navigate the user to the
        sign up page where a user can create an account. If it finds the button, it will click it to be taken to the page
        This function will only be called if the filters are not found in the URL of the current base page.

        """

        #Searches the URL for the login filters and if it finds it, clicks it
        #Idea is if URLS entered are to base - it will search for register page by clicking link
        def findRegister():
            login_filters = ["reate account", "egister", "ign up","ign-up", "SIGN UP"]
            # Try all filters till login button is found
            for i in login_filters:
                try:
                    check = browser.find_elements_by_xpath("//*[contains(text(), '{}')]".format(i))
                    if check != None:
                        for element in check:
                            try:
                                element.click()
                            except:
                                pass
                except:
                    print(failed)
        #Check URL to see if its already on signup page
        #If not, it will call the above function to search for registration page
        if "ignup" in url or "egister" in url or "ignUp" in url or "ign-up" in url:
            print("URL okay")
        else:
            print("Clicking button on page to navigate")
            findRegister()
        
        #################################
        #Check current URL of form to compare after form has been filled automatically to see if
        #it differs to new URL
        signup_url = browser.current_url
        ################################################################
        # This section attempts to fill in the registration form fields automatically
        # WRITTEN BY: Rahul Patel (Rpp20)
        ################################################################
        time.sleep(2)
        
        #Firstname 
        try:
            WebDriverWait(browser, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='First name'][type='text']"))).send_keys(first_name)
        except:
            try:
                WebDriverWait(browser, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='First Name'][type='text']"))).send_keys(first_name)
            except:
                try:
                    WebDriverWait(browser, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='firstName'][type='text']"))).send_keys(first_name)
                except:
                    try:#Note
                        WebDriverWait(browser, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input[name*='first'i][type='text']"))).send_keys(first_name)
                    except:
                        print("Unable to detect 'Firstname' field")  
        #Lastname
        try:
            WebDriverWait(browser, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Last name'][type='text']"))).send_keys(last_name)
        except:
            try:
                WebDriverWait(browser, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Last Name'][type='text']"))).send_keys(last_name)
            except:
                try:
                    WebDriverWait(browser, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='lastName'][type='text']"))).send_keys(last_name)
                except:
                    try:
                        WebDriverWait(browser, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input[name*='last'i][type='text']"))).send_keys(last_name)
                    except:
                        print("Unable to detect 'Lastname' field")  
    #Age
        try:
            selectOption = Select(browser.find_element_by_class_name("selectInput-module_select__3mCI2"))
            selectOption.select_by_visible_text("17")
        except:
            print("Unable to detect age field") 
        #Username
        try:
            u1 = WebDriverWait(browser, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='Username'][type='email']")))
            u1.send_keys(email)
        except:
            try:
                u2 = WebDriverWait(browser, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Username'][type='text']")))
                u2.send_keys(email)
            except:
                print("Unable to detect username field")
        #Email
        try:
            e1 = WebDriverWait(browser, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='New email'][type='text']")))
            e1.send_keys(email)
        except:
            try:
                e2 = WebDriverWait(browser, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Email'][type='email']")))   
                e2.send_keys(email)
            except:
                try:
                    e3 = WebDriverWait(browser, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='email']")))
                    e3.send_keys(email)
                except:
                    try:
                        e4 = WebDriverWait(browser, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='text'][name='Email']")))
                        e4.send_keys(email)
                    except:
                        try:
                            e5 = WebDriverWait(browser, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='text'][placeholder='Email Address']")))
                            e5.send_keys(email)
                        except:
                            print("Unable to detect 'Email' field")
        #Password
        try:
            p1 = WebDriverWait(browser, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Password'][type='password']")))
            p1.clear()
            p1.send_keys(strong_pass)
            p1.send_keys(Keys.ENTER)
        except:
            try:
                p2 = WebDriverWait(browser, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Create password'][type='password']")))
                p2.clear()
                p2.send_keys(strong_pass)
                p2.send_keys(Keys.ENTER)
            except:
                try:
                    p3 = WebDriverWait(browser, 1).until(EC.elements_to_be_clickable((By.CSS_SELECTOR, "input[type='password']")))
                    fields.clear()
                    fields.send_keys(strong_pass)
                    fields.send_keys(Keys.ENTER)
                except:
                    try:
                        #Facebook website (Generic code not working for some reason)
                        p4 = WebDriverWait(browser, 1).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='password_step_input']")))
                        p4.send_keys(strong_pass)
                    except:
                        print("Unable to detect 'Password' field")  
        is_captcha = check_captcha()
        if is_captcha == True:
            get_captcha_sound()
        #ConfirmPassword (research common fields for this and update)
        try:
            cp1 = WebDriverWait(browser, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Confirm Password'][type='password']")))
            cp1.clear()
            cp1.send_keys(strong_pass)
            cp1.send_keys(Keys.ENTER)
        except:
            try:
                cp2 = WebDriverWait(browser, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='ConfirmPasswd'][type='password']")))
                cp2.clear()
                cp2.send_keys(strong_pass)
                cp2.send_keys(Keys.ENTER)
            except:
                try:
                    cp3 = WebDriverWait(browser, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='password']")))
                    cp3.clear()
                    cp3.send_keys(strong_pass)
                    cp3.send_keys(Keys.ENTER)
                except:
                    print("Unable to detect 'Confirm Password' field")
        
        is_captcha = check_captcha()
        if is_captcha == True:
            get_captcha_sound()
        ############################################################            
        #Check if automated signup was completed
        #List of URLS which were not automatically completed, will be placed in text file which can be run again with human intervention
        time.sleep(3)
        new_url = browser.current_url
        if new_url == signup_url:
            f = open("manual_intervention_required.txt", "a")
            f.write(signup_url + "\n")
            f.close()
            HumanInteractionRec.append(signup_url)
        else: #Testing purposes only
            f = open("accounts_created_automatically.txt", "a")
            f.write(new_url + "\n")
            f.close()
        #time to manually 
        time.sleep(15)
        #Add disclaimer
  
    return HumanInteractionRec

###############################

"""allows the program to be run with a file as input

the program can be called with sendFile(filepath) to run using a .txt file containing URLS
where filepath is the location. This can be editied on line 68 or entered in the terminal.

"""

def sendFile(filepath):
    file = open(filepath)
    ar = []
    for elem in file:
      ar.append(elem)

    global arr; arr = ar
    return sign_up()

"""allows the program to be run with a array of urls as a string

the program can be called with sendString(arrList) to use an arrray of URLS as input.

Typical useage:
    sendString(["https://signup.com/"] OR sendString(URLS)

"""
def sendString(arrList):
    global arr; arr = arrList
    return sign_up()
