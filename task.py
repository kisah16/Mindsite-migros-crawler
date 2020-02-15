import requests
import lxml
from bs4 import BeautifulSoup
import time



def Process_lists(Product, Product_category, Product_line):

	named_tuple = time.localtime()

	Product_name = Product.find('h5').text
	Product_url = 'https://www.migros.com.tr' + Product.find('a').get('href')
	Product_price = Product.find("div", attrs = {'class' : 'price-tag'}).text
#	Product_cargo_fee = Product
	if Product.find("div", attrs = {'class' : 'campaign-tag'}) == None:
		Product_promotion_text = "No promotion"
	else:
		Product_promotion_text = Product.find("div", attrs = {'class' : 'campaign-tag'}).text
	Product_category_name = Product_category
	Product_crawling_timestamp = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)

	Product_image_link = Product.find('img').get('src')

	print(Product_line)

	return {
		'product_id' : Product_name,
		'product_url' : Product_url,
		'product_price' : Product_price,
	#	'cargo_fee' : 
		'promotion_text' : Product_promotion_text,
		'category_name' : Product_category_name,
		'crawling_timestamp' :  Product_crawling_timestamp,
		'product_image_link' : Product_image_link,
	}



def List_products(soup, page_number):

	
	lists_of_all_product = soup.find_all("div", attrs = {'class' : 'list'})
	Product_category_name = soup.find('h1').text

	for Product_line,listsofall in enumerate(lists_of_all_product, start = 1):
		Process_lists(listsofall, Product_category_name, Product_line + (page_number - 1) * 24)


		
def Page_link():

	r = requests.get('https://www.migros.com.tr/gazli-icecek-c-80')

	soup = BeautifulSoup(r.content, 'html.parser')

	Num_of_page = int(soup.find("nav", attrs = {'class' : 'page-nav'}).find_all('li')[-2].a.get('data-page'))

	for Page_number in range (1, Num_of_page + 1):
		r = requests.get('https://www.migros.com.tr/gazli-icecek-c-80?sayfa=' + str(Page_number))
		soup = BeautifulSoup(r.content, 'html.parser')
		List_products(soup, Page_number)

	


Page_link()







# Sayfa sayfa dolaşma, Error handling, Arguman ile çalışma, Sort algoritması