from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC


options = Options()
options.add_argument('--headless')

driver = webdriver.Chrome(
    options=options,
    service=ChromeService(ChromeDriverManager().install())
    )
def get_price_amazon(item_link):
    """
    Scrapes the price from an amazon listing

    Input:
        String item_link --  the link as a string to scrape the price from
    Output:
        Float price -- the resulting price from the amazon page
    """
    if type(str) != type(" "):
        return "Wrong type! Make sure input is a string"
    driver.get(item_link)
    price_whole = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[9]/div[5]/div[4]/div[12]/div/div[1]/div[3]/div[1]/span[1]/span[2]/span[2]')
    price_fraction = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[9]/div[5]/div[4]/div[12]/div/div[1]/div[3]/div[1]/span[1]/span[2]/span[3]')
    price = float(price_whole.text + "." + price_fraction.text)
    print(price, type(price))
    return price


    """
    
    """

def scrape_item_on_amazon(search_item):
    # assign any keyword for searching
    driver.get('https://www.amazon.com/')
    keyword = search_item
    # create WebElement for a search box
    search_box = driver.find_element(By.ID, 'twotabsearchtextbox')
    # type the keyword in searchbox
    search_box.send_keys(keyword)
    # create WebElement for a search button
    search_button = driver.find_element(By.ID, 'nav-search-submit-button')
    # click search_button
    search_button.click()
    # wait for the page to download
    driver.implicitly_wait(5)

    product_asin = []
    product_name = []
    product_price = []
    product_ratings = []
    product_ratings_num = []
    product_link = []

    items = wait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "s-result-item s-asin")]')))
    for item in items:
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
        link = item.find_element(By.XPATH, './/a[@class="a-link-normal a-text-normal"]').get_attribute("href")
        product_link.append(link)

    driver.quit()

    # to check data scraped
    print(product_name)
    print(product_asin)
    print(product_price)
    print(product_ratings)
    print(product_ratings_num)
    print(product_link)
product_list = ["rice_cooker"]
for item in product_list:
    scrape_item_on_amazon(item)