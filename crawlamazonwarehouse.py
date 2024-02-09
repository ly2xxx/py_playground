from bs4 import BeautifulSoup
import requests

# Function to extract Product Title
def get_title(soup):
	
	try:
		# Outer Tag Object
		title = soup.find("span", attrs={"id":'productTitle'})

		# Inner NavigableString Object
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
def get_discount_ratio(soup):

	try:
		new_price = soup.find("span", attrs={'class':'a-offscreen'}).string.strip()
		print("New = ", new_price)
		prices = soup.select('div.a-box-inner span.a-offscreen')
		used_price = prices[0].get_text().strip()
		print("Used = ", used_price)
		price = float(used_price[1:]) / float(new_price[1:])
		if (price < 0.6):
			print("BARGAIN!!!")
	except AttributeError:
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
		available = ""	

	return available	

def print_product_info(url):
	print(url)
	# Headers for request
	HEADERS = ( {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"})

	# The webpage URL
	# URL = "https://www.amazon.co.uk/dp/B08688GFPD/"

	# HTTP Request
	webpage = requests.get(url, headers=HEADERS)

	# Soup Object containing all data
	# soup = BeautifulSoup(webpage.content, "lxml")
	soup = BeautifulSoup(webpage.content, "html.parser")

	# Function calls to display all necessary product information
	print("Product Title =", get_title(soup))
	print("Product Discount =", get_discount_ratio(soup))
	print("Product Rating =", get_rating(soup))
	print("Number of Product Reviews =", get_review_count(soup))
	print("Availability =", get_availability(soup))
	print()
	print()

if __name__ == '__main__':

	#https://www.octoparse.com/blog/how-to-scrape-amazon-data-using-python
	headers2 = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
	domain_url = "https://www.amazon.co.uk"
	base_url = "https://www.amazon.co.uk/s?k=ddr4+ram+32gb&i=warehouse-deals&page="
	for page_number in range(1, 101):
		# Create the new URL by replacing the page number
		page_url = base_url + str(page_number)
		print(page_url)
		response2 = requests.get(page_url, headers=headers2)

		soup2 = BeautifulSoup(response2.content, "html.parser")

		titles = soup2.find_all("h2", class_="a-size-mini a-spacing-none a-color-base s-line-clamp-2")
		if titles.count==0:
			print("===THE END===")
			break
		for title in titles:
			print (title.get_text())
			href = title.find('a', attrs={'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'}).get("href")
			print (href)
			# Split the string using '/'
			parts = href.split('/')
			print_product_info(domain_url+"/dp/"+parts[3])

 	# titles = [title.get_text() for title in titles]

	# print(titles)