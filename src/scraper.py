from src.consolelog import console_logger
from bs4 import BeautifulSoup
import requests
import os
import time
import json
from config import Config as config

class Scraper:

    @staticmethod
    def read_files():
        dirpath = os.path.join(os.getcwd(), config.HTML_DIR)
        files = os.listdir(dirpath)
        for file in files:
            filepath = "{}/{}".format(dirpath, file)
            f = open(filepath, 'r').read()
            html_file = BeautifulSoup(f, "lxml")
            yield html_file, file.split(".")[0]

    @staticmethod
    def parse_html(file):
        parent_container = file.find('div', class_="hnsbs512Border")
        atags = parent_container.find_all('a', class_="hnsql212Question valign-wrapper")
        links = list()
        for atag in atags:
            links.append(atag["href"])
        return links

    @staticmethod  
    def get_question_page(url):
        try:
            response_page = requests.get(url).text
            response_page = BeautifulSoup(response_page, "lxml")
            return response_page
        except Exception as e:
            console_logger.debug(e)

    @staticmethod
    def parse_question_page(question_page):
        try:
            question = question_page.find('h1', class_="qap761Title").text
            answer = question_page.find('pre', class_="qap761AnswerDivImg").text
            if question and answer:
                return {"question": question, "answer": answer}
            else:
                return None
        except Exception as e:
            return None

    def scrape(self, filename):
        # file generator
        generator = self.read_files()

        # question urls
        url_to_tag = {}
        question_url = list()
        for file, tag in generator:
            file_urls = self.parse_html(file)
            for url in file_urls:
                url_to_tag[url] = tag
            question_url = question_url + file_urls

        # getting all entries for the csv file 
        allentries = list()
        for url in question_url:
            question_page = self.get_question_page(url)
            entry = self.parse_question_page(question_page)
            if entry:
                entry["tag"] = [url_to_tag[url]]
                allentries.append(entry)
        
        json_object = json.dumps(allentries, indent = 4)
        # Writing to sample.json
        with open(filename, "w") as outfile:
            outfile.write(json_object)

        return True

    def run(self):
        console_logger.debug("Scraper is running")

        console_logger.debug("Reading html files")

        status = self.scrape("FAQ.json")

        if status:
            console_logger.debug("Scraping Successfull")
        else:
            console_logger.debug("Scraping Failed")

        
        

