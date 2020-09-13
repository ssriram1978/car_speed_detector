from selenium import webdriver
from datetime import datetime
import time

opts = webdriver.ChromeOptions()
opts.binary_location = '/Users/kaushik/Desktop/Google Chrome.app/Contents/MacOS/Google Chrome'
driver = webdriver.Chrome(executable_path='/Users/kaushik/Desktop/Drivers/chromedriver',options=opts)
driver.get('https://web.whatsapp.com')

now = datetime.now()
time.sleep(10)

def Sendmessage():
    to = ("Tw")
    message = ("From GVW, there is a speeding car at time = {} on date = {} - day = {}, month = {} , year = {}.".format(now.strftime("%X"),now.strftime("%d"),
            now.strftime("%A"),now.strftime("%B"),now.strftime("%Y")))

    # finds the name of the group chat
    user = driver.find_element_by_xpath('//span[@title = "{}"]'.format(to))
    # clicks on the name of the group chat
    user.click()
    # finds the message box
    messagebox = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
    # pastes the message into the message box
    messagebox.send_keys(message)
    # finds the button to send the message
    button = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[3]')
    # clicks the button to send the message
    button.click()

Sendmessage()

