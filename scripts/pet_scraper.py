import requests

from bs4 import BeautifulSoup

class PetScraper:

	def __init__(self):
		self.api_url = 'https://www.pesweb.cz/cz/psi-k-adopci?list_type=desc&vek=2m-6m&vek=6m-2r&vek=2r-8r&barva1=&barva2=&plemeno=&fci=&link-utulek=&start='
		self.pet_results = {}

	def get_response(self, start):
		url = self.api_url + str(start)
		try:
			response = requests.Session().get(url)
			response.raise_for_status()
		except Exception as e:
			print(f'Couldn\'t get response from server. Error: {e}.')

		return response.text

	def get_page_of_pets(self, response):
		soup = BeautifulSoup(response, 'html.parser')
		pets_div = soup.find_all('div', {'class': 'block_items'})[0]

		pets_page = pets_div.find_all('div', {'class': 'object-item-in'})  

		return pets_page

	def iterate_through_pages(self):
		pets_list = []
		start = 0

		while True:
			response = self.get_response(start)
			pets_page = self.get_page_of_pets(response)

			pets_list.extend(pets_page)
			if len(pets_page) != 52:
				return pets_list
			else:
				start += 52

def get_appropriate_pets(pets_data):
	### Store URL of pets which are other dogs, cats friendly and appropriate to live in a flat

	acceptable_icon = ['plemeno-icon-kocka', 'plemeno-icon-psi', 'plemeno-icon-byt']
	url_list = []
	soup = BeautifulSoup(pets_data, features="lxml")
	pets_list = soup.find_all('div', {'class': 'object-item-in'})  
	for pet in pets_list:
		pet_icons = pet.find_all('div', {'class': 'icons'})
		icon_cat, icon_dog, icon_flat = 0, 0, 0
		if pet_icons:
			icon_list = pet_icons[0].find_all('span', {'class': 'icon'})
			for icon in icon_list:
				icon_id = icon.get('id')

				if icon_id == acceptable_icon[0]:
					icon_cat = 1
				elif icon_id == acceptable_icon[1]:
					icon_dog = 1
				elif icon_id == acceptable_icon[2]:
					icon_flat = 1
				
			if icon_cat and icon_dog and icon_flat:
				url = pet.find_all('a')
				url_list.append(url[0]['href'])
			else:
				continue
	return url_list

def save_data(path, data, raw=False):
	if raw:
		with open(path, 'w') as f:
			f.write(str(data))
	else:
		if type(data) == list:
			with open(path, 'w') as f:
				for d in data:
					f.write('https://pesweb.cz' + d + '\n')
		else:
			with open(path, 'w') as f:
				f.write(d)

			


def load_json(path):
	with open(path, 'r') as f:
		data = f.read()

	return data
