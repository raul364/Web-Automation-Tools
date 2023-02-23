# Web-Automation & Password security tools
Tools designed for automating web scrapping, account creation and logging in, CAPTCHA solving, and extracting password policies on the web.


The tools were desguned for Scraping password requirements on large number of websites for cyber security researchers and practioners however, most of the tools are open ended therefore, can be used for any web purposes by tweaking the parameters.

<h1>CAPTCHA</h1>
Designed to complete and bypass audio Captcha's by utilising Google speech to text libraries.
It will download the audio file, convert the speech to text and return the text.
You must then implement a way to input the text to the correct field.

HOW TO USE
Provide link to the audio file.

<h1>SEngineWrapper</h1>
Designed to generate a list of links based on the search term you provide.
Will return a cvs file with websites based on search term

MUST PROVIDE PATH TO CHROMEDRIVER IN THE CODE

HOW TO USE
provide search term
number of links you want to gather
choose between google or bing to search from. (the search engine will be Google Chrome)


<h1>Login</h1>
Tool designed to login in to a page provided you give it link that goes directly to the login page.
you can give it a txt file with either 1 or multiple websites
It will return a browser with tabs open for each website you provided. Logged in to the site.

MUST PROVIDE PATH TO CHROMEDRIVER IN THE CODE

HOW TO USE
provide username and password and txt file


<h1>AutoLogin</h1>
Tool designed to navigate to the login page/ login from the base URL.
This tool is semi-automated. It will give user 15 seconds to manually navigate to the login page to aid the bot in parsing login details. For the difficult webpages.
The Bot will attempt to navigate to the login page. If it fails there will be a 15 second window whre there is no movement, this is for the user to manually navigate from the current state to the login page... after which the bot will resume control and attempt to login.
This tool was made semi-automated to increase the success rate of logging in to 95% from base URL.

The tool includes a cookie acceptor to remove cookeis that block access to the page.
The tool also includes method to interact with CAPTCHA's and extract the audio file link for the CAPTHCA solver tool, as well as input the result from the tool.

MUST PROVIDE PATH TO CHROMEDRIVER IN THE CODE

HOW TO USE
provide username, password, and boolean if you want to stay logged in.
Auto_Login(user, pass, stayLoggedIn)
