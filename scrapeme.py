#!/usr/bin/env python3

import click
import sys

from scripts.pet_scraper import PetScraper, get_appropriate_pets, save_data, load_json

# @click.command()
# @click.option('-s', '--sex', type=str, help='Gender of a dog')
# @click.option('-a', '--age', type=int, help='Age of the dog. Type --help ')
# @click.option('-h', '--height', type=int)
# @click.option('-col1', '--color1', type=str)
# @click.option('-col2', '--color2', type=str)
# @click.option('-c', '--condition', type=str)
# @click.option('f', '--fci', type=str)
def main():
	ps = PetScraper()

	### Make requests to pesweb.cz server and fetch all of theirs pets
	pets_list = ps.iterate_through_pages()

	### Load pets info and scrape URL which satisfied conditions
	data = load_json('pets_list.json')
	url_list = get_appropriate_pets(data)
	save_data('pets_url.json', url_list, False)
	print(url_list)

if __name__ == '__main__':
	main()
