#!/usr/bin/python3
import sys
from config import Config
import logging
from scrape import Scraper
import os
from os import listdir
from os.path import isfile, join

def main():

	# First we'll check to see if we already have data locally 
	if not has_local_data():
		scraper = Scraper(config)
		scraper.start()

	# TODO the rest of the thing

def has_local_data():
	path = config.HAIKU_JSON_LOCATION
	if os.path.exists(path):
		files = [f for f in listdir(path) if isfile(join(path, f))]
		if files != []:
			return True
	return False

if __name__ == '__main__':
	config = Config()
	main()