# Web-Automation & Password security tools
Tools designed for automating web scrapping, account creation and logging in, CAPTCHA solving, and extracting password policies on the web.


The tools were desguned for Scraping password requirements on large number of websites for cyber security researchers and practioners however, most of the tools are open ended therefore, can be used for any web purposes by tweaking the parameters.

<h1>Audio_Captcha_Solver</h1>
Designed to complete and bypass audio Captcha's by utilising Google speech to text libraries.
It will download the audio file, convert the speech to text and return the text.
You must then implement a way to input the text to the correct field.

HOW TO USE
Provide link to the audio file.

<h1>SEngine_Wrapper</h1>
Designed to generate a list of links based on the search term you provide.
Will return a cvs file with websites based on search term

MUST PROVIDE PATH TO CHROMEDRIVER IN THE CODE

HOW TO USE
provide search term
number of links you want to gather
choose between google or bing to search from. (the search engine will be Google Chrome)


<h1>Login</h1>
Caller file for AutoLogin.py to login a user with username and password over an array of urls and return the urls that failed

A list of URLs where the automated login bot didn't work will be generated in the end for you.

MUST PROVIDE PATH TO CHROMEDRIVER IN THE CODE

HOW TO USE
import login
arr = ["]
login.login_to_site("USERNAME1241", "Pa55word!", [array of URLs])


<h1>AutoLogin</h1>
Tool designed to navigate to the login page/ login from the base URL. This tool works in conjuction with Login tool and so it is provoked through Login.py
This tool is semi-automated. It will give user 15 seconds to manually navigate to the login page to aid the bot in parsing login details. For the difficult webpages.
The Bot will attempt to navigate to the login page. If it fails there will be a 15 second window whre there is no movement, this is for the user to manually navigate from the current state to the login page... after which the bot will resume control and attempt to login.
This tool was made semi-automated to increase the success rate of logging in to 95% from base URL.

The tool includes a cookie acceptor to remove cookeis that block access to the page.
The tool also includes method to interact with CAPTCHA's and extract the audio file link for the CAPTHCA solver tool, as well as input the result from the tool.

MUST PROVIDE PATH TO CHROMEDRIVER IN THE CODE


<h1>Post_Login_Sec_Scrape</h1>
Caller file for AutoLogin.py to login a user with username and password over an array of urls and return the urls that failed
This is another tool which utilises AutoLogin with the intention of scraping additional password policy data such as MFA if available.
This is a semi automated tool as it gives the user 15 seconds after the user is logged in to navigate to the password secrity page. After 15 seconds the bot resumes control and scarpes for additional password policy. 

typical usage case:
import post_login_sec_srape
arr = ["https://www.google.com","https://www.bing.com"]
post_login_sec_srape.get_settings("USERNAME1241","Pa55word!","secuirty","Account",arr)


<h1>Account_Create</h1>
A bot that attempts to create accounts on various websites automatically with the potential need for human interaction.

Takes URLS in the form of an array variable or file and begins by navigating to the signup page, filling out the generic form fields
and submitting the form in an attempt to create account. 15 Seconds is also given at the end for human interaction if the full form could not 
done so automatically. 

will return a array of websites that accounts were not created for as well as 2 text files. 1 with completed urls
and 2 with websites that were successful.
    Typical useage example:
    sendString(["https://signup.com/", "https://accounts.google.com/signup?hl=en"]
    OR
    sendFile() - Where the filepath variable on line 68 is changed to locate a .txt file containing URLS OR the filepath is entered in the brackets
