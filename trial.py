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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


#get the path for the chromedriver and use the webdriver
path = r'C:/Users/Administrator/Desktop/chromedriver_win32/chromedriver.exe'
driver = webdriver.Chrome(executable_path = path)
driver.get('https://profile.gujaratimatrimony.com/search/search.php?gaact=reg&gasrc=MENUSUB')

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
loginDetails.send_keys('9176755064')
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
driver.execute_script("arguments[0].click();", button)

time.sleep(1)

#choose religion
select = Select(driver.find_element_by_id('RELIGION'))
select.select_by_value('1')

time.sleep(1)

#choose caste
caste_button = driver.find_element_by_xpath('//*[@id="castedivid"]/dd/div[1]')
driver.execute_script("arguments[0].click();", caste_button)
#caste_button = driver.find_element_by_xpath('//*[@id="CASTE_INinner_option_id_2"]')
#driver.execute_script("arguments[0].click();", caste_button)

time.sleep(8)

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
final_dict["subcaste"] = []

name_list=[]
caste_list=[]
religion_list=[]
subcaste_list=[]

#loop for as many pages as there are

time.sleep(2)
for i in range(1,100000):
    notfound = 0
    premium = 0
    basic = '//*[@id="smartignore_'+str(i)+'"]'
    basic1 = '//*[@id="phsmartignore_'+str(i)+'"]'
    #get surnames, castes and religion

    xpath = basic + '/div[1]/div[2]/div[1]/div[1]'
    xpath1 = basic1 + '/div/div/div[1]/div[2]/div[1]/div[1]'
    try:
        element = driver.find_element_by_xpath(xpath)
        m = element.text
    except StaleElementReferenceException:
        time.sleep(1)
        print("stale")
        element = driver.find_element_by_xpath(xpath)
        m = element.text
    except NoSuchElementException:
        #element = driver.find_element_by_xpath(xpath1)
        premium=1
        print('nf name')
        
    xpath = basic + '/div[2]/div[3]/div[1]/div[3]/span[2]'
    xpath1 = basic1 + '/div/div/div[2]/div[3]/div[1]/div[3]/span[2]'
    try:
        c_element = driver.find_element_by_xpath(xpath)
    except StaleElementReferenceException:
        time.sleep(1)
        print("stale")
        c_element = driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        #c_element = driver.find_element_by_xpath(xpath1)
        print('nf caste')

    xpath = basic + '/div[2]/div[3]/div[1]/div[2]/span[2]'
    xpath1 = basic1 + '/div/div/div[2]/div[3]/div[1]/div[2]/span[2]'
    try:
        r_element = driver.find_element_by_xpath(xpath)
        driver.execute_script("arguments[0].scrollIntoView();", r_element)
    except StaleElementReferenceException:
        time.sleep(1)
        print("stale")
        r_element = driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        #r_element = driver.find_element_by_xpath(xpath1)
        print('nf religion')

    xpath = basic + '/div[2]/div[3]/div[1]/div[4]/span[2]'
    xpath_par = basic + '/div[2]/div[3]/div[1]/div[4]/span[1]'
    string1 = 'Sub Caste:'
    try:
        if driver.find_element_by_xpath(xpath_par).text == string1:
            sc_element = driver.find_element_by_xpath(xpath)
            driver.execute_script("arguments[0].scrollIntoView();", r_element)
        else:
            notfound = 1
    except NoSuchElementException:
        #r_element = driver.find_element_by_xpath(xpath1)
        print('nf sub caste')
  
    #extract surnames, castes, religion into the lists
    if premium == 0:
        if '. ' in m:
            try:
                name_list.append(m.split(' ',2)[2])
            except:
                print('why is this happening')
                name_list.append(" ")
            caste_list.append(c_element.text)
            religion_list.append(r_element.text)
            if notfound==0:
                subcaste_list.append(sc_element.text)
            else:
                subcaste_list.append('none')
        elif ' ' in m:
            name_list.append(m.split(' ',1)[1])
            caste_list.append(c_element.text)
            religion_list.append(r_element.text)
            if notfound==0:
                subcaste_list.append(sc_element.text)
            else:
                subcaste_list.append('none')
    else:
        print(i)
    
    #go to the next page if it exists by clicking next button
    size = len(driver.find_elements_by_css_selector('.fleft.opcity.link.normaltxt'))

    if i%10 == 0 and i > 11:
        try:
            next_button = driver.find_element_by_xpath('//*[@id="pagination"]/li[9]/a')
            #print(next_button.get_attribute("disabled"))
        except StaleElementReferenceException:
            time.sleep(1)
            print("stale")
            next_button = driver.find_element_by_xpath('//*[@id="pagination"]/li[9]/a')
        except NoSuchElementException:
            print("not found next buttton")
            break
##        next_button = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="pagination"]/li[9]/a')))
        ActionChains(driver).move_to_element(next_button).perform()
        driver.execute_script("arguments[0].scrollIntoView();", next_button)
        driver.execute_script("arguments[0].click();", next_button)
        #driver.execute_script("arguments[0].click();", next_button)        
        s="button clicked at "
        print(s+"{}".format(i))
        time.sleep(1)
        
    elif i%10 == 0 and i != 0:
        try:
            next_button = driver.find_element_by_xpath('//*[@id="pagination"]/li[8]/a')
        except StaleElementReferenceException:
            time.sleep(1)
            print("stale")
            next_button = driver.find_element_by_xpath('//*[@id="pagination"]/li[9]/a')
        except NoSuchElementException:
            print("not found next buttton")
            break
        driver.execute_script("arguments[0].click();", next_button)
        driver.execute_script("arguments[0].click();", next_button)
        time.sleep(2)
        
    elif i>11:
        try:
            next_button = driver.find_element_by_xpath('//*[@id="pagination"]/li[9]/a')
        except NoSuchElementException:
            print("not found next buttton")
            break
        
    elif i == size:
        break

    if i%100 == 0 and i!=0:
        final_dict["surname"]=name_list
        final_dict["caste"]=caste_list
        final_dict["religion"]=religion_list
        final_dict["subcaste"]=subcaste_list
        print(final_dict)

        #changing the dictionary into dataframe   
        df = pd.DataFrame(final_dict)
        print(df)
        #df.to_csv('trial.csv')
        with open('caste_surname_data.csv', 'a',newline='', encoding='utf-8') as f:
                     df.to_csv(f, index=False)

        final_dict = {}
        final_dict["caste"] = []
        final_dict["surname"] = []
        final_dict["religion"] = []
        final_dict["subcaste"] = []

        name_list=[]
        caste_list=[]
        religion_list=[]
        subcaste_list=[]
        
    if i%500 == 0 and i!=0:
        time.sleep(10)
            
  
#put the lists into the dicitonary
final_dict["surname"]=name_list
final_dict["caste"]=caste_list
final_dict["religion"]=religion_list
final_dict["subcaste"]=subcaste_list
print(final_dict)

#changing the dictionary into dataframe   
df = pd.DataFrame(final_dict)
print(df)
#df.to_csv('trial.csv')
with open('trial.csv', 'a',newline='') as f:
             df.to_csv(f, header=False, index=False)

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
