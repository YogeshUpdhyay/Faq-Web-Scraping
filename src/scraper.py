from src.consolelog import console_logger
from bs4 import BeautifulSoup
import requests
import os
from config import Config as config

class Scraper:
    def __init__(self):
        self.url_file = config.SCRAPE_URL_FILE

    def read_urls(self):
        # read urls from the files
        if os.path.isfile(self.url_file):
            with open(self.url_file) as f:
                urls = f.read().splitlines() 
                # console_logger.debug(urls)
            return urls
        else:
            return None

    def fetch_file(self, url):
        try:
            source = requests.get(url).text
            html_file = BeautifulSoup(source, 'lxml')
            return html_file
        except Exception as e:
            console_logger.debug(e)

    def get_questions(self, html_file):
        # fetch questions from html file
        block = html_file.find('div', class_="hnsql212QuestionGroup")
        console_logger.debug(block)


    def scrape(self, filename):
        # scarpe files
        # for url in self.urls:
        #     html_file = self.fetch_file(url)
        html_file = self.fetch_file("https://groww.in/help/stocks/sx-dashboard")
        console_logger.debug(html_file)
        questions = self.get_questions(html_file)

    def run(self):
        console_logger.debug("Scraper is running")

        console_logger.debug("Reading urls from the file")

        self.urls = self.read_urls()
        if not self.urls:
            console_logger.debug("File was not found")
            return

        status = self.scrape("FAQ.csv")

        if status:
            console_logger.debug("Scraping Successfull")
        else:
            console_logger.debug("Scraping Failed")

        
        

