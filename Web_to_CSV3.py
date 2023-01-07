# We need to extract headers, textboxes and dropdown lists and tables
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select
from html_table_parser.parser import HTMLTableParser
import pandas as pd
import re
import time

def clean_text(text_list):
    clean_text_list = list()
    for text in text_list:
        text = text.encode('unicode_escape').decode('ascii')
        text = re.sub(r'\\u([0-9]{3})[a-z]', '', text)
        text = re.sub(r'\\xa0', '', text)
        text = re.sub(r'\\n', ' ', text)
        text = text.strip()
        text = re.sub(r' +', ' ', text)
        clean_text_list.append(text.encode('ascii').decode('unicode_escape'))
    return clean_text_list

if __name__ == "__main__":

    # Setting up Selenium Chromedriver
    s = Service("C:\\Users\\varun\\AppData\\Local\\Programs\\Python\\Python39\\Lib\\site-packages\\chromedriver.exe")
    driver = webdriver.Chrome(service=s)
    uri = input("Enter URI")
    driver.get(uri)

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    req = urllib.request.Request(url=uri, headers=headers)
    xhtml = urllib.request.urlopen(req).read().decode('utf-8')
    driver.implicitly_wait(20)
    # Logging in
    # id = input("Enter user ID")
    # pwd = input("Enter pwd")
    # IDbox = driver.find_element_by_xpath('//*[@id="username"]')
    # pwdbox = driver.find_element_by_xpath('//*[@id="password"]')
    # signinbutton = driver.find_element_by_xpath('//*[@id="submit"]')
    # driver.execute_script(f"arguments[0].value='{id}';", IDbox)
    # driver.execute_script(f"arguments[0].value='{pwd}';", pwdbox)
    # driver.execute_script("arguments[0].click();", signinbutton)
    # button1 = driver.find_element_by_xpath('//*[@id="div2"]')
    # driver.execute_script("arguments[0].click();", button1)
    # button2 = driver.find_element_by_xpath('//*[@id="menu2"]/div[1]')
    # driver.execute_script("arguments[0].click();", button2)
    # button3 = driver.find_element_by_xpath('//*[@id="scal1"]/a[1]')
    # driver.execute_script("arguments[0].click();", button3)
    # xpath of anchor tag= //*[@id="scal1"]/a[1]    

    # Headers
    header_text_list = list()
    header_tag_list = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span']
    for header_tag in header_tag_list:
        tags = driver.find_elements_by_tag_name(header_tag)
        header_text_list.append([f'Headers {header_tag} tag'] + clean_text(tag.get_attribute('textContent') for tag in tags if tag.get_attribute('innerText')!= ''))
    print(header_text_list)

    # Text boxes
    text_box_list = list()
    text_boxes = driver.find_elements_by_tag_name("input")
    for text_box in text_boxes:
        if text_box.is_displayed() == True:
            text_box_list.append([f'Textbox {text_boxes.index(text_box)+1}'] + [text_box.get_attribute('type')])
    print(text_box_list)

    # Dropdown lists
    drop_down_list = list()
    drop_downs = driver.find_elements_by_tag_name("select")
    for drop_down in drop_downs:
        select_obj = Select(drop_down)
        options_obj = [f'Dropdown list {drop_downs.index(drop_down)+1}'] + clean_text(option.get_attribute('textContent') for option in select_obj.options)
        drop_down_list.append(options_obj)
    print(drop_down_list)

    # Tables
    # Defining the HTMLTableParser object
    p = HTMLTableParser()
    p.feed(xhtml)
    try:
        p.tables[0].insert(0, ['Tables'])
    except:
        pass

    # Making csv file
    header_df = pd.DataFrame(header_text_list)
    text_box_df = pd.DataFrame(text_box_list)
    drop_down_df = pd.DataFrame(drop_down_list)
    df2 = header_df.append(text_box_df, ignore_index=False, sort=False)
    df2 = df2.append(drop_down_df, ignore_index=False, sort=False)
    for table in p.tables:
        print(table)
        df2 = df2.append(pd.DataFrame(table), ignore_index=False, sort=False)

    # Converting the dataframe into the csv file
    df2.to_csv('Webpage.csv')

    time.sleep(5)
    driver.quit()