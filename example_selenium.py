
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions as EX
import sqlite3
next_page = ''
def store_db(product_asin, product_name, product_price, product_ratings, product_ratings_num, product_link):
    conn = sqlite3.connect('amazon_search.db')
    curr = conn.cursor()

    # create table
    
    curr.execute('''CREATE TABLE IF NOT EXISTS search_result (ASIN text, name text, price real, ratings text, ratings_num text, details_link text)''')
    # insert data into a table
    curr.executemany("INSERT INTO search_result (ASIN, name, price, ratings, ratings_num, details_link) VALUES (?,?,?,?,?,?)", 
                    list(zip(product_asin, product_name, product_price, product_ratings, product_ratings_num, product_link)))
        
    conn.commit()
    conn.close()

items = dict()
class Item:
    def __init__(self, item_names, prices, ratings, rating_nums, links):
        self.prices = prices
        self.item_names = item_names
        self.ratings = ratings
        self.rating_nums = rating_nums
        self.links = links
def scrape_item(driver):

    product_asin = []
    product_name = []
    product_price = []
    product_ratings = []
    product_ratings_num = []
    product_link = []
    
    items = wait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "s-result-item s-asin")]')))
    for item in items:
        print("it's not entirely fucked")
        # find name
        name = item.find_element(By.XPATH, './/span[@class="a-size-medium a-color-base a-text-normal"]')
        product_name.append(name.text)

        # find ASIN number 
        data_asin = item.get_attribute("data-asin")
        product_asin.append(data_asin)

        # find price
        whole_price = item.find_elements(By.XPATH, './/span[@class="a-price-whole"]')
        fraction_price = item.find_elements(By.XPATH, './/span[@class="a-price-fraction"]')
        
        if whole_price != [] and fraction_price != []:
            price = '.'.join([whole_price[0].text, fraction_price[0].text])
        else:
            price = 0
        product_price.append(price)

        # find ratings box
        ratings_box = item.find_elements(By.XPATH, './/div[@class="a-row a-size-small"]/span')

        # find ratings and ratings_num
        if ratings_box != []:
            ratings = ratings_box[0].get_attribute('aria-label')
            ratings_num = ratings_box[1].get_attribute('aria-label')
        else:
            ratings, ratings_num = 0, 0
        
        product_ratings.append(ratings)
        product_ratings_num.append(str(ratings_num))
        
        # find link
        link = item.find_element(By.XPATH, './/a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]').get_attribute("href")
        product_link.append(link)
    store_db(product_asin, product_name, product_price, product_ratings, product_ratings_num, product_link)
    print(items.page_source)
    global next_page
    next_page = driver.find_element(By.XPATH, '//li[@class ="a-selected"]/following-sibling::a').get_attribute("href")

    # to check data scraped
    #print(product_name)
    #print(product_asin)
    #print(product_price)
    #print(product_ratings)
    #print(product_ratings_num)
    #print(product_link)
def scrape_amazon(keyword, max_pages):
    web = 'https://www.amazon.com'

    options = webdriver.ChromeOptions()
    #options.add_argument('--headless')
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))

    #getting past captcha (hopefully)
    #wait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']")))
    #wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[@id='recaptcha-anchor']"))).click()

    driver.get(web)
    html = driver.page_source
    print(html)
    counter = 1
    while True:
        try:
            search = driver.find_element(By.XPATH, "//*[@id='twotabsearchtextbox']")
            break
        except EX.NoSuchElementException:
            try:
                search = driver.find_element(By.XPATH, "//*[@id='nav-bb-search']")
                break
            except EX.NoSuchElementException:
                print('Fail.')
                counter += 1
                print(counter)

    search.send_keys(keyword)
    # click search button
    search_button = driver.find_element(By.ID, 'nav-search-submit-button')
    search_button.click()

    page_number = 1
    driver.implicitly_wait(5)
    while page_number <= max_pages:
        scrape_item(driver)
        page_number += 1
        driver.get(next_page)
        driver.implicitly_wait(5)
    driver.quit()

if __name__ == '__main__':
    keywords_list = ["rice cooker", "Pressure Cooker","Bowl Sets","Plate Sets","Knifeblock","Baking Sheets","Cups","Seasoning","Dish Soap","Dishwashing Brush","Cooking Oils","Water Filter","Kitchen Trash Can"]
    for keyword in keywords_list:
        scrape_amazon(keyword, 1)
        

    