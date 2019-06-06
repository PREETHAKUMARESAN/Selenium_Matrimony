from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
from lxml import html
from requests.auth import AuthBase
from requests.auth import HTTPBasicAuth
import time
import re
import unittest
import pandas as pd
import urllib.request
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from robobrowser import RoboBrowser
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC


#get the path for the chromedriver and use the webdriver
path = r'C:/Users/Administrator/Desktop/chromedriver_win32/chromedriver.exe'
driver = webdriver.Chrome(executable_path = path)
driver.get('https://profile.oriyamatrimony.com/search/search.php?gaact=SEARCH&gasrc=MENUSUB')

#to check if webelement exists in the page
def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

#Do Login
login_button = driver.find_element_by_xpath('//*[@id="logindiv"]')
driver.execute_script("arguments[0].click();", login_button)
loginDetails = driver.find_element_by_id("ID")
loginDetails.send_keys('7339045740')
pwdDetails = driver.find_element_by_id("PASSWORD")
pwdDetails.send_keys('preetha17')
log_button = driver.find_element_by_xpath('//*[@id="loginpop"]/div/div/form/div[1]/div[7]/div[5]/input')
driver.execute_script("arguments[0].click();", log_button)

#to handle pop-ups
time.sleep(3)

#redirect to search window
#driver.get('https://profile.gujaratimatrimony.com/search/search.php?gaact=SEARCH&gasrc=MENUSUB')
search_button = driver.find_element_by_xpath('//*[@id="fixed-topnavbg"]/div/ul/div[1]/li[3]/div/div[1]/a')
driver.execute_script("arguments[0].click();", search_button)
time.sleep(1)

#handle for parent window
parent_han  = driver.window_handles     
windows_before  = driver.current_window_handle

#clik regular search tab
button = driver.find_element_by_id('reg')
button.click()

time.sleep(1)

#choose religion
select = Select(driver.find_element_by_id('RELIGION'))
select.select_by_value('1')

time.sleep(1)

#choose caste
caste_button = driver.find_element_by_xpath('//*[@id="castedivid"]/dd/div[1]')
driver.execute_script("arguments[0].click();", caste_button)
#caste_button = driver.find_element_by_xpath('//*[@id="CASTE_INinner_option_id_1"]')
#driver.execute_script("arguments[0].click();", caste_button)

#submit the search attributes
submit_button = driver.find_element_by_xpath('//*[@id="Form"]/form/dl/dd/span/input')
driver.execute_script("arguments[0].click();", submit_button)


'''wait(driver, 5).until(EC.number_of_windows_to_be(2))
all_han = driver.window_handles
new_han = [x for x in all_han if x != parent_han][1]    #get the register free window

driver.switch_to.window(new_han)    #close the register free window
driver.close()'''
time.sleep(1)

#the final dicitonary to hold the values
final_dict = {}
final_dict["caste"] = []
final_dict["surname"] = []
final_dict["religion"] = []

name_list=[]
caste_list=[]
religion_list=[]

#loop for as many pages as there are

'''def append_function(tries, name_list, caste_list, religion_list):

    print(name_list)
    print(caste_list)
    print(religion_list)
    i=0
    #get surnames, castes and religion
    time.sleep(10)
    element = driver.find_elements_by_css_selector(".fleft.opcity.link.normaltxt")
    c_element = driver.find_elements_by_css_selector(".srh-mediumtxt.opcity > div:nth-child(5) > span:nth-child(2)")
    r_element = driver.find_elements_by_css_selector(".srh-mediumtxt.opcity > div:nth-child(3) > span:nth-child(2)")
    size = len(element)

    #put surnames, castes, religion into the dicitonary
    for i in range(0,10):
        m = element[i].text
        print(m)
        if '. ' in m:
            name_list.append(m.split(' ',2)[2])
            caste_list.append(c_element[i].text)
            religion_list.append(r_element[i].text)
        elif ' ' in m:
            name_list.append(m.split(' ',1)[1])
            caste_list.append(c_element[i].text)
            religion_list.append(r_element[i].text)
    
    #go to the next page if it exists
    if check_exists_by_xpath('//*[@id="pagination"]/li[8]/a') or check_exists_by_xpath('//*[@id="pagination"]/li[9]/a'):
        if tries == 1:
            next_button = driver.find_element_by_xpath('//*[@id="pagination"]/li[8]/a')
            driver.execute_script("arguments[0].click();", next_button)
            tries = tries + 1
            append_function(tries, name_list, caste_list, religion_list)
            
        else:
            try:
                next_button = driver.find_element_by_xpath('//*[@id="pagination"]/li[9]/a')
            except NoSuchElementException:
                return name_list, caste_list, religion_list
            next_button = driver.find_element_by_xpath('//*[@id="pagination"]/li[9]/a')
            driver.execute_script("arguments[0].click();", next_button) 
            tries = tries + 1
            append_function(tries, name_list, caste_list, religion_list)
            
    else:
        return  name_list, caste_list, religion_list

tries = 1
name_list, caste_list, religion_list = append_function(tries, name_list, caste_list, religion_list)

#put the lists into the dicitonary
final_dict["surname"].append(name_list)
final_dict["caste"].append(caste_list)
final_dict["religion"].append(religion_list)
print(final_dict)

#changing the dictionary into dataframe   
df = pd.DataFrame(final_dict)
print(df)'''

i =0
for i in range(1,106):
    basic = '//*[@id="smartignore_'+str(i)+'"]'
    basic1 = '//*[@id="phsmartignore_'+str(i)+'"]'
    #get surnames, castes and religion
    time.sleep(1)
    xpath = basic + '/div[1]/div[2]/div[1]/div[1]'
    xpath1 = basic1 + '/div/div/div[1]/div[2]/div[1]/div[1]'
    try:
        element = driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        element = driver.find_element_by_xpath(xpath1)
    
    xpath = basic + '/div[2]/div[3]/div[1]/div[3]/span[2]'
    xpath1 = basic1 + '/div/div/div[2]/div[3]/div[1]/div[3]/span[2]'
    try:
        c_element = driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        c_element = driver.find_element_by_xpath(xpath1)
    
    xpath = basic + '/div[2]/div[3]/div[1]/div[2]/span[2]'
    xpath1 = basic1 + '/div/div/div[2]/div[3]/div[1]/div[2]/span[2]'
    try:
        r_element = driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        r_element = driver.find_element_by_xpath(xpath1)

    #put surnames, castes, religion into the dicitonary
    
    m = element.text
    if '. ' in m:
        name_list.append(m.split(' ',2)[2])
        caste_list.append(c_element.text)
        religion_list.append(r_element.text)
    elif ' ' in m:
        name_list.append(m.split(' ',1)[1])
        caste_list.append(c_element.text)
        religion_list.append(r_element.text)
    
    #go to the next page if it exists
    try:
        driver.find_element_by_xpath('//*[@id="pagination"]/li[8]/a') or driver.find_element_by_xpath('//*[@id="pagination"]/li[9]/a')
        if i%10 == 0 and i > 11:
            print(i)
            next_button = driver.find_element_by_xpath('//*[@id="pagination"]/li[9]/a')
            driver.execute_script("arguments[0].click();", next_button)
        elif i%10 == 0 and i != 0:
            print(i)
            next_button = driver.find_element_by_xpath('//*[@id="pagination"]/li[8]/a')
            driver.execute_script("arguments[0].click();", next_button)
    except NoSuchElementException:
        break
  
#put the lists into the dicitonary
final_dict["surname"]=name_list
final_dict["caste"]=caste_list
final_dict["religion"]=religion_list
print(final_dict)

#changing the dictionary into dataframe   
df = pd.DataFrame(final_dict)
print(df)
df.to_csv('trial.csv')




'''br = RoboBrowser()
br.open('https://www.gujaratimatrimony.com/#loginpopup')
form = br.get_form()
form['ID'] = "9176755064"
form['PASSWORD'] = "preetha17"
br.submit_form(form)
print(br.parsed)'''
#html = urlopen("https://www.gujaratimatrimony.com/#loginpopup")
#bs = BeautifulSoup(html.read(), 'html.parser')
#print(bs)

'''response = urllib.request.urlopen('http://example.webscraping.com/places/default/search')
html = response.read()
text = html.decode()
re.findall('(.*?)',text)'''
'''session_requests = requests.Session()
login_details = {
		'ID' : '9176755064',
		'PASSWORD' : 'preetha17'
}

result = session_requests.post(
	'https://www.gujaratimatrimony.com/#loginpopup' , 
	login_details
)
print(result.text)

print('Cookie is set to:')
print(result.cookies.get_dict())
print('Going to profile page...')
result  = session_requests.get('https://profile.gujaratimatrimony.com/login/myhome.php')'''


