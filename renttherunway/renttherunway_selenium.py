# Import Selenium

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import csv
import re
import time
import math


PAUSE_TIME = 1.8

driver = webdriver.Chrome()
driver.get("https://www.renttherunway.com/c/dresses?filters%5Bzip_code%5D=08901&sort=recommended&page=1&_=1604176342590#1604201758942")

csv_file = open('renttherunway.csv', 'w', encoding='utf-8', newline='')
writer = csv.writer(csv_file)



# Close pop up window
try:
    popup = driver.find_element_by_xpath('')
    popup.click()
except:
    pass


for category in category_list:
    category_url = f'https://www.saksfifthavenue.com/c/women-s-apparel/{category}'
    driver.get(category_url)
    time.sleep(4)
    num_item = driver.find_element_by_xpath('//span[@class="search-count d-none d-lg-inline-block"]').text
    num_item = int(re.search('(\d+)',num_item.replace(',','')).group(1))
    num_page = math.ceil(num_item/96)

    try:
    	popup = driver.find_element_by_xpath('')
    	popup.click()
	except:
    	pass
    
    # accessing each pages
    for i in range(num_page):
        page_url = f'{category_url}&start={96*i}&sz=24'
        driver.get(page_url)
        time.sleep(PAUSE_TIME)    
        
        try:
            popup = driver.find_element_by_xpath('//span[@class="consent-tracking-close svg-13-avenue-large-close svg-13-avenue-large-close-dims"]')
            popup.click()
        except:
            pass
    
        # scroll down 
        while True:
            last_height = driver.execute_script("return document.body.scrollHeight")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(PAUSE_TIME+2)
            new_height = driver.execute_script("return document.body.scrollHeight")
        
            if new_height == last_height:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(PAUSE_TIME+2)
                new_height = driver.execute_script("return document.body.scrollHeight")

                if new_height == last_height:
                    break
                else:
                    last_height = new_height
                    continue
        

        item_url = driver.find_elements_by_xpath('//h3/a[@class="link"]')

        product_url = []
        for i in range(len(item_url)):
            if i%2 == 0:
                item_url = item_url[i].get_attribute("href")
                product_url.append(item_url)
        
        print(len(product_url))
        
        # product information from each link
        for link in product_url:
            item = {}
            driver.get(link)
            time.sleep(PAUSE_TIME)
        
            # product page -> collect information
            # category, brand name, product name, price, discount_price
            website = 'Saksfithavenue'
            cat = category
            try:
                brand_name = driver.find_element_by_xpath('//h1[@class="product-brand-name d-none d-sm-block"]').text
            except:
                brand_name = None
            
            try:
                product_name = driver.find_element_by_xpath('//div/h1[@class="product-name h2 d-none d-sm-block"]').text
            except:
                product_name = None
            
            try:
                price = driver.find_element_by_xpath('//span[@class="value"]').get_attribute('content')
                if not price:
                    price = driver.find_element_by_xpath('//span[@class="formatted_price bfx-price bfx-list-price"]').get_attribute('data-unformatted-price')
                    if not price:
                        price = driver.find_element_by_xpath('//span[@class="formatted_price bfx-price bfx-list-price"]').text
                price = float(re.search('(\d+\.*\d+)',price).group(1))
            except:
                price = None        
        
        
            # final csv file
            item['website'] = website
            item['brand_name'] = brand_name
            item['product_name'] = product_name
            item['category'] = re.search('\w*\/*\w+\/((\w+-*)+)',cat).group(1)
            item['sex'] =  re.search('((\w+-*)+)\/',cat).group(1)
            item['price'] = price
            
            writer.writerow(item.values())
            csv_file.flush()