from bs4 import BeautifulSoup
import requests
import random as rand

# Function to extract Product Title
def get_title(soup):
	
	try:
		# Outer Tag Object
		title = soup.find("span", attrs={"id":'productTitle'})

		# Inner NavigatableString Object
		title_value = title.string 

		# Title as a string value
		title_string = title_value.strip()

		# # Printing types of values for efficient understanding
		# print(type(title))
		# print(type(title_value))
		# print(type(title_string))
		# print()

	except AttributeError:
		title_string = ""	

	return title_string

# Function to extract Product Price
def get_price(soup):

	try:
		price = soup.find("span", attrs={'id':'priceblock_ourprice'}).string.strip()

	except AttributeError:

		try:
			# If there is some deal price
			price = soup.find("span", attrs={'id':'priceblock_dealprice'}).string.strip()

		except:		
			price = ""	

	return price

# Function to extract Product Rating
def get_rating(soup):

	try:
		rating = soup.find("i", attrs={'class':'a-icon a-icon-star a-star-4-5'}).string.strip()
		
	except AttributeError:
		
		try:
			rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
		except:
			rating = ""	

	return rating

# Function to extract Number of User Reviews
def get_review_count(soup):
	try:
		review_count = soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.strip()
		
	except AttributeError:
		review_count = ""	

	return review_count

# Function to extract Availability Status
def get_availability(soup):
	try:
		available = soup.find("div", attrs={'id':'availability'})
		available = available.find("span").string.strip()

	except AttributeError:
		available = "Not Available"	

	return available	


if __name__ == '__main__':

	# Headers for request
    rotated_headers = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15']
    HEADERS = ({'User-Agent':
                rotated_headers[rand.randrange(0, len(rotated_headers))],
	            'Accept-Language': 'en-US'})

	# The webpage URL
    URL = "https://www.amazon.com/Cancelling-Headphones-Lightweight-Srhythm-Bluetooth/dp/B083S6Q8VK/ref=sr_1_2_sspa?c=ts&keywords=Over-Ear+Headphones&qid=1688949354&s=aht&sr=1-2-spons&ts_id=12097479011&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1"
	
	# HTTP Request
    webpage = requests.get(URL, headers=HEADERS)
    print(webpage)

	# Soup Object containing all data
    soup = BeautifulSoup(webpage.content, "lxml")
    print(soup)
    
    """
	# Fetch links as List of Tag Objects
    links = soup.find_all("a", attrs={'class':'a-link-normal s-no-outline'})

	# Store the links
    links_list = []

	# Loop for extracting links from Tag Objects
    for link in links:
        links_list.append(link.get('href'))

	# Loop for extracting product details from each link 
    for link in links_list:

        new_webpage = requests.get("https://www.amazon.com" + link, headers=HEADERS)

        new_soup = BeautifulSoup(new_webpage.content, "lxml")
		
		# Function calls to display all necessary product information
        print("Product Title =", get_title(new_soup))
        print("Product Price =", get_price(new_soup))
        print("Product Rating =", get_rating(new_soup))
        print("Number of Product Reviews =", get_review_count(new_soup))
        print("Availability =", get_availability(new_soup))
        print()
        print()
	    """