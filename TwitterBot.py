
# Twitter Bot - Get Followers, Followings and Followers that are Not Followed

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import secrets

class TwitterBot():
    ## Class Variables
    sleep_time_sec = 5
    wait_time_sec = 90
    
    def __init__(self, username, pwd):
        self.username = username
        self.pwd = pwd
        #self.wait_time = 90
		self.chromeDriverPath = 'C:\\chromedriver_win32\\chromedriver.exe' ## Download Chrome Driver for Selenium and give path here
        self.driver = webdriver.Chrome(self.chromeDriverPath)  # Optional argument, if not specified will search path.
        #self.driver.maximize_window()
        self.driver.get('https://twitter.com/login')
        time.sleep(TwitterBot.sleep_time_sec)
        
    def __login(self):

        ## Waiting till element "session[username_or_email]" shows up
        username_search_box = WebDriverWait(self.driver, self.wait_time_sec).until(
            EC.presence_of_element_located((By.NAME, "session[username_or_email]"))
        ).send_keys(self.username)

        time.sleep(1)

        # Password Text Box
        pwd_search_box = self.driver.find_element_by_name("session[password]").send_keys(self.pwd + Keys.ENTER)

    def __goToProfile(self):   
        
        time.sleep(TwitterBot.sleep_time_sec)
        
        # Profile Link
        profile_link = WebDriverWait(self.driver, self.wait_time_sec).until(
            EC.presence_of_element_located((By.XPATH, f"//a[@href='/{self.username}']"))
        ).click()
        
        time.sleep(TwitterBot.sleep_time_sec)
        

    def goToFollowersLink(self):    
        
        ## Scroll to Top
        self.driver.execute_script("window.scrollTo(0, 0);")
        
        time.sleep(TwitterBot.sleep_time_sec)
        
        # Followers Link
        followers_link = WebDriverWait(self.driver, self.wait_time_sec).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/div[1]/div[2]/div[5]/div[2]/a"))
        ).click()
        
        time.sleep(TwitterBot.sleep_time_sec)

    def __getUsers(self, section_div, users_xpath):   
        ## Scrolling
        SCROLL_PAUSE_TIME = TwitterBot.sleep_time_sec
        
        ## Initialize list of users, will be Extended on each scroll
        lstofUsers = []
        
        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        
        while True:
            ## Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            ## Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)
            
            ## Find user id details using provided 'section_div' and 'users_xpath' 
            all_users_div = section_div.find_elements_by_tag_name(users_xpath)
            
            ## Extend Users after Each Scroll and Dont Add Duplicates
            lstnames = [x.text.replace('@', '') for x in all_users_div if x.text.startswith('@') and x.text.replace('@', '') not in lstofUsers]
            lstofUsers.extend(lstnames)
            
            ## Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        
        return lstofUsers
    
    def getFollowers(self):
        section_div = WebDriverWait(self.driver, self.wait_time_sec).until(
            EC.presence_of_element_located((By.XPATH, '//section/div[@aria-label="Timeline: Followers"]/div/div'))
        )
        return self.__getUsers(section_div, 'span.css-901oao.css-16my406.r-1qd0xha.r-ad9z0x.r-bcqeeo.r-qvutc0')
    
    def goToFollowingLink(self):    
        
        ## Scroll to top
        self.driver.execute_script("window.scrollTo(0, 0);")
        
        time.sleep(TwitterBot.sleep_time_sec)
        
        # Following Link
        following_link = WebDriverWait(self.driver, self.wait_time_sec).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[1]/div[2]/nav/div[2]/div[2]/a'))
        ).click()
        
        time.sleep(TwitterBot.sleep_time_sec)
        
    def getFollowingList(self):
        section_div = WebDriverWait(self.driver, self.wait_time_sec).until(
            EC.presence_of_element_located((By.XPATH, '//section/div[@aria-label="Timeline: Following"]/div/div'))
        )
        return self.__getUsers(section_div, 'span.css-901oao.css-16my406.r-1qd0xha.r-ad9z0x.r-bcqeeo.r-qvutc0')
    
    def stopBot(self):
        ## Click Side More Menu
        self.driver.find_element_by_xpath('//div[@data-testid="AppTabBar_More_Menu"]').click()
        
        time.sleep(2)
        
        ## Click Logout Option
        logout_link = WebDriverWait(self.driver, self.wait_time_sec).until(
            EC.presence_of_element_located((By.XPATH, '//a[@href="/logout"]'))
        ).click()
        
        time.sleep(1)
        
        ## Click Confirm Logout Button
        logout_conirm_btn = WebDriverWait(self.driver, self.wait_time_sec).until(
            EC.presence_of_element_located((By.XPATH, '//div[@data-testid="confirmationSheetConfirm"]'))
        ).click()
        
        time.sleep(TwitterBot.sleep_time_sec)
        
        self.driver.quit()
        
    
    ## Main start method, will be called 
    def startBot(self):
        self.__login()
        self.__goToProfile()
        


tb = TwitterBot(secrets.uname, secrets.pwd)

tb.startBot() ## Start Bot

tb.goToFollowersLink() ## Move to Followers Link and click

## Get Followers List
follwersList = tb.getFollowers()

tb.goToFollowingLink() # Move to Following Link

## Get Following List
follwingList = tb.getFollowingList()

tb.stopBot() ## Will signout and close browser

print(f'Total Followers == {len(follwersList)}')
print(", ".join(follwersList))

print('\n')
print("**********************************************************")
print("\n")

print(f'Total Following == {len(follwingList)}')
print(", ".join(follwingList))

## Me Not Following these Users
NotFollowingList = [x for x in follwersList if x not in follwingList]

print('\n')
print("**********************************************************")
print("\n")

print(f'My Followers that I am not Following == {len(NotFollowingList)}')
print(", ".join(NotFollowingList))

