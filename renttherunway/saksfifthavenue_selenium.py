
# Import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import csv
import re
import time
import math




# Set pause time
PAUSE_TIME = 2.0
driver = webdriver.Chrome()

# Write csv file

csv_file = open('saksfifthavenue.csv', 'w', encoding='utf-8', newline='')
writer = csv.writer(csv_file)

writer.writerow(['website','brand_name','product_name', 'category', 'price', 'discount_price'])

category_list = ['women-s-apparel/dresses']


for category in category_list:
    category_url = f'https://www.saksfifthavenue.com/c/{category}?prefn1=isSale&prefv1=Sale'
    driver.get(category_url)
    time.sleep(4)
    
    # ignore the pop up screen
    try:
        popup = driver.find_element_by_xpath('//span[@class="consent-tracking-close svg-13-avenue-large-close svg-13-avenue-large-close-dims"]')
        popup.click()
    except:
        pass

    # number of total pages in each category
    num_item = driver.find_element_by_xpath('//span[@class="search-count d-none d-lg-inline-block"]').text
    num_item = int(re.search('(\d+)',num_item.replace(',','')).group(1))
    num_page = math.ceil(num_item/96)
    
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
                original_price = driver.find_element_by_xpath('//span[@class="value"]').get_attribute('content')
                if not original_price:
                    original_price = driver.find_element_by_xpath('//span[@class="formatted_price bfx-price bfx-list-price"]').get_attribute('data-unformatted-price')
                    if not original_price:
                        original_price = driver.find_element_by_xpath('//span[@class="formatted_price bfx-price bfx-list-price"]').text
                original_price = float(re.search('(\d+\.*\d+)',original_price).group(1))
            except:
                original_price = None
            
            try:
                discount_price = driver.find_element_by_xpath('//span[@class="value bfx-price"]').get_attribute('content')
                if not discount_price:
                    discount_price = driver.find_element_by_xpath('//span[@class="formatted_sale_price formatted_price js-final-sale-price bfx-price bfx-sale-price"]').text
                    if not discount_price:
                        discount_price = driver.find_element_by_xpath('//span[@class="formatted_sale_price formatted_price js-final-sale-price bfx-price bfx-list-price"]').text
                discount_price = float(re.search('(\d+\.*\d+)',discount_price).group(1))
            except:
                original_price = None           
        
        
            # final csv file
            item['website'] = website
            item['brand_name'] = brand_name
            item['product_name'] = product_name
            item['category'] = re.search('\w*\/*\w+\/((\w+-*)+)',cat).group(1)
            item['sex'] =  re.search('((\w+-*)+)\/',cat).group(1)
            item['original_price'] = original_price
            item['discount_price'] = discount_price
            
            writer.writerow(item.values())
            csv_file.flush()

csv_file.close()