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
    filepath = '/Users/kaushik/Desktop/Photo on 8-25-20 at 1.41 PM #2.jpg'

    message = ("In GVW, there is a speeding car at {} on {}, {} {}, {}.".format(now.strftime("%X"),now.strftime("%A"),
                now.strftime("%B"), now.strftime("%d"),now.strftime("%Y") ))

    user = driver.find_element_by_xpath('//span[@title = "{}"]'.format(to))                                     # finds the name of the group chat
    user.click()                                                                                                # clicks on the name of the group chat
    messagebox = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')                # finds the message box
    messagebox.send_keys(message)                                                                               # pastes the message into the message box
    textsendbutton = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[3]')                       # finds the button to send the message
    textsendbutton.click()                                                                                      # clicks the button to send the message

    attachmentbox = driver.find_element_by_xpath('//div[@title = "Attach"]')                                    # finds the attatchment box
    attachmentbox.click()                                                                                       # clicks on the attatchment box
    imagebox = driver.find_element_by_xpath('//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')  # finds the image attatchment box
    imagebox.send_keys(filepath)                                                                                # inserts the image using its file path
    time.sleep(3)
    imagesendbutton = driver.find_element_by_xpath('//span[@data-testid="send"]')                               # finds the button to send the image
    imagesendbutton.click()                                                                                     # clicks the button to send the image

Sendmessage()





