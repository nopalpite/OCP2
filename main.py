# coding: utf-8
import csv
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

URL = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/"

BOOK_INFORMATION = ["product_page_url", "universal_ product_code (upc)", "title", "price_including_tax",
                    "price_excluding_tax", "number_available", "product_description", "category", "review_rating",
                    "image_url"]

book_information_result = {"product_page_url": "get_url",
                           "universal_ product_code (upc)": "get_upc",
                           "title": "get_title",
                           "price_including_tax": "get_price",
                           "price_excluding_tax": "get_price_tax_free",
                           "number_available": "get_availability",
                           "product_description": "get_description",
                           "category": "get_category",
                           "review_rating": "get_review_rating",
                           "image_url": "get_image_url"
                           }

CSV_FILE = './output.csv'


class Book:

    def __init__(self, url):
        self.url = url
        self.page = requests.get(url)
        self.soup = BeautifulSoup(self.page.content, 'html.parser')

    def get_url(self):
        return self.url

    def get_upc(self):
        upc_tag = self.soup.find("th", string="UPC")  # find tag by string
        upc = upc_tag.find_next().string
        return upc

    def get_title(self):
        title_tag = self.soup.find("h1")
        title = title_tag.string
        return title

    def get_price(self):
        price_tag = self.soup.find("th", string="Price (incl. tax)")  # find tag by string
        price = price_tag.find_next().string
        return price

    def get_price_tax_free(self):
        price_tax_free_tag = self.soup.find("th", string="Price (excl. tax)")  # find tag by string
        price_tax_free = price_tax_free_tag.find_next().string
        return price_tax_free

    def get_availability(self):
        availability_tag = self.soup.find("th", string="Availability")
        availability = availability_tag.find_next().string
        return availability

    def get_description(self):
        description_tag = self.soup.find(id="product_description")
        description = description_tag.find_next("p").string
        return description

    def get_category(self):
        category_parent_tag = self.soup.find("ul")
        category_tag = category_parent_tag.find_all_next("a")[-1]
        category = category_tag.string
        return category

    def get_review_rating(self):
        review_tag = self.soup.find("p", class_=re.compile('star-rating'))
        review = review_tag['class'][-1]
        return review

    def get_image_url(self):
        image_url_tag = self.soup.find("img")
        image_relative_url = image_url_tag['src']
        image_url = urljoin(self.url, image_relative_url)
        return image_url


book = Book(URL)

with open(CSV_FILE, 'w') as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    writer.writerow(BOOK_INFORMATION)
    rows = []
    for i in book_information_result:
        toto = getattr(Book, book_information_result[i])
        rows.append(toto(book))
    writer.writerow(rows)
