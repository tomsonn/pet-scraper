#!/usr/bin/env python3

from scripts.pet_scraper import PetScraper, get_appropriate_pets, save_data, load_json

def main():
	ps = PetScraper()

	### Make requests to pesweb.cz server and fetch all of theirs pets
	pets_list = ps.iterate_through_pages()

	### Load pets info and scrape URL which satisfied conditions
	data = load_json('pets_list.json')
	url_list = get_appropriate_pets(data)
	save_data('pets_url.json', url_list, False)


if __name__ == '__main__':
	main()
