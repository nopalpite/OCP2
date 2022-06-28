import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


class Book:

    def __init__(self, url):
        self.url = url
        self.page = requests.get(url)
        self.soup = BeautifulSoup(self.page.content, 'html.parser')

    @property
    def upc(self):
        upc_tag = self.soup.find("th", string="UPC")
        return upc_tag.find_next().string

    @property
    def title(self):
        title_tag = self.soup.find("h1")
        return title_tag.string

    @property
    def price(self):
        price_tag = self.soup.find("th", string="Price (incl. tax)")
        return price_tag.find_next().string

    @property
    def price_without_tax(self):
        price_tax_free_tag = self.soup.find("th", string="Price (excl. tax)")
        return price_tax_free_tag.find_next().string

    @property
    def availability(self):
        availability_tag = self.soup.find("th", string="Availability")
        return availability_tag.find_next().string

    @property
    def description(self):
        description_tag = self.soup.find(id="product_description")
        if description_tag is not None:
            return description_tag.find_next("p").string
        return ""

    @property
    def category(self):
        category_parent_tag = self.soup.find("ul")
        category_tag = category_parent_tag.find_all_next("a")[-1]
        return category_tag.string

    @property
    def review_rating(self):
        review_tag = self.soup.find("p", class_=re.compile('star-rating'))
        review_string = review_tag['class'][-1]
        review_dict = {"One": 1,
                       "Two": 2,
                       "Three": 3,
                       "Four": 4,
                       "Five": 5}
        return review_dict[review_string]

    @property
    def image_url(self):
        image_url_tag = self.soup.find("img")
        image_relative_url = image_url_tag['src']
        return urljoin(self.url, image_relative_url)

    def get_informations(self):
        return {
            'product_page_url': self.url,
            'universal_product_code (upc)': self.upc,
            'title': self.title,
            'price_including_tax': self.price,
            'price_excluding_tax': self.price_without_tax,
            'number_available': self.availability,
            'product_description': self.description,
            'category': self.category,
            'review_rating': self.review_rating,
            'image_url': self.image_url
        }
