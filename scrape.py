#!/usr/bin/python3
import urllib.request
import json
import time
import logging
import os
from bs4 import BeautifulSoup
from os import listdir
from os.path import isfile, join

class Scraper(object):
    """docstring for Scraper"""
    

    def __init__(self, config):
        super(Scraper, self).__init__()
        self.config = config
        self.logger = logging.getLogger('Scraper')
        
        self.prepare_for_local_resources()


    def prepare_for_local_resources(self):
        cfg = self.config
        log = self.logger
        # When we start scraping we need a folder to store all of the downloaded files
        paths_to_check = [
            cfg.RESOURCE_PATH,
            cfg.HAIKU_PATH,
            cfg.RAW_HAIKU_PATH,
            cfg.PROCESSED_HAIKU_PATH
        ]

        log.debug('Checking for {} paths.'.format(len(paths_to_check)))

        for path in paths_to_check:
            log.debug('Checking for "{}".'.format(path))
            if not os.path.exists(path):
                log.debug('Path dose not exist, creating it.')
                os.makedirs(path)
            else:
                log.debug('Path exists.')

    def generate_urls_to_scrape(self):
        cfg = self.config
        log = self.logger
        log.info('Starting url generation.')

        log.info('Fetching haiku urls.')
        response = urllib.request.urlopen(cfg.HAIKU_URL)

        log.info('Decoding fetched html page.')
        # Use utf-8 decoder to ensure cross platform usability
        soup = BeautifulSoup(response.read(), cfg.SOUP_PARSER)

        log.info('Locating valid hrefs.')
        # Grabbing all elements that are links and have a parent element
        # matching our locator
        partial_urls = soup.find_all(href=cfg.HAIKU_PARTIAL_HREF_REGEX)

        log.info('Extracting hrefs and building full urls.')
        urls = [ cfg.HAIKU_BASE_URL + partial.get('href') for partial in partial_urls]

        log.info('Found {} urls.'.format(len(urls)))
        
        return urls

    def fetch_raw_html_pages(self, urls):
        cfg = self.config
        log = self.logger

        log.info('Starting fetch on {} pages.'.format(len(urls)))
        for index, link in enumerate(urls):
            log.debug('{}/{} Fetching {}.'.format(index + 1, len(urls), link))
            urllib.request.urlretrieve(link, '{}/{}.html'.format(cfg.RAW_HAIKU_PATH, index))
            time.sleep(cfg.FETCH_DELAY_IN_SEC)

        log.info('Finished fetching pages.')

    def parseHTML(self):
        cfg = self.config
        log = self.logger

        log.info('Starting html parsing for haikus.')
        # We will start by grabbling a list of all files in the raw folder
        raw_path = cfg.RAW_HAIKU_PATH
        log.info('Looking for raw html files.')
        raw_files = [join(raw_path, f) for f in listdir(raw_path) if isfile(join(raw_path, f))]
        log.info('Found {} html files to extract from.'.format(len(raw_files)))
        all_lines = []

        for index, file in enumerate(raw_files):
            with open( file, encoding='utf-8') as fp:
                log.debug('{}/{} Opening {}.'.format(index + 1, len(raw_files), file))
                soup = BeautifulSoup(fp, cfg.SOUP_PARSER)
            log.debug('Locating all haikus.')
            haikus = soup.find_all("p", class_="haiku")
            log.debug('Found {} haikus.'.format(len(haikus)))
            for haiku in haikus:
                lines = [text for text in haiku.stripped_strings]
                all_lines.append(lines)

        # We filter out empty lists if they exits (they do)
        result = [x for x in all_lines if x]
        
        log.info('Creating haikus.json from a toal of {}.'.format(len(result)))
        with open( cfg.HAIKU_JSON_LOCATION, 'w', encoding='utf-8') as output:
            json.dump(result, output, ensure_ascii=False, indent=4)
    
        log.info('Created {}.'.format(cfg.PROCESSED_HAIKU_PATH + "haikus.json"))

    def start(self):
        log = self.logger

        log.info('Starting scraping')
        urls = self.generate_urls_to_scrape()
        self.fetch_raw_html_pages(urls)
        self.parseHTML()
        log.info('Scraping complete')