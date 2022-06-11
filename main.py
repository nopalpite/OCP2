# coding: utf-8
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

URL = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/"


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

    def get_review(self):
        review_tag = self.soup.find("p", class_=re.compile('star-rating'))
        review = review_tag['class'][-1]
        return review

    def get_image_url(self):
        image_url_tag = self.soup.find("img")
        image_relative_url = image_url_tag['src']
        image_url = urljoin(self.url, image_relative_url)
        return image_url


book = Book(URL)


