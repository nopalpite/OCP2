import re
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup


class Book:

    def __init__(self, url):
        self.url = url
        self.page = requests.get(url)
        self.soup = BeautifulSoup(self.page.content, 'html.parser')

    def get_url(self):
        return self.url

    def get_upc(self):
        upc_tag = self.soup.find("th", string="UPC")
        upc = upc_tag.find_next().string
        return upc
    def get_title(self):
        title_tag = self.soup.find("h1")
        title = title_tag.string
        return title

    def get_price(self):
        price_tag = self.soup.find("th", string="Price (incl. tax)")
        price = price_tag.find_next().string
        return price

    def get_price_tax_free(self):
        price_tax_free_tag = self.soup.find("th", string="Price (excl. tax)")
        price_tax_free = price_tax_free_tag.find_next().string
        return price_tax_free

    def get_availability(self):
        availability_tag = self.soup.find("th", string="Availability")
        availability = availability_tag.find_next().string
        return availability

    def get_description(self):
        description_tag = self.soup.find(id="product_description")
        if description_tag is not None:
            description = description_tag.find_next("p").string
        else:
            description = ""
        return description

    def get_category(self):
        category_parent_tag = self.soup.find("ul")
        category_tag = category_parent_tag.find_all_next("a")[-1]
        category = category_tag.string
        return category

    def get_review_rating(self):
        review_tag = self.soup.find("p", class_=re.compile('star-rating'))
        review_string = review_tag['class'][-1]
        review_dict = {"One": 1,
                       "Two": 2,
                       "Three": 3,
                       "Four": 4,
                       "Five": 5}
        review = review_dict[review_string]
        return review

    def get_image_url(self):
        image_url_tag = self.soup.find("img")
        image_relative_url = image_url_tag['src']
        image_url = urljoin(self.url, image_relative_url)
        return image_url

    def get_informations(self):
        return {
            'product_page_url': self.url,
            'universal_product_code (upc)': self.get_upc,
            'title': self.get_title,
            'price_including_tax': self.get_price,
            'price_excluding_tax': self.get_price_tax_free,
            'number_available': self.get_availability,
            'product_description': self.get_description,
            'category': self.get_category,
            'review_rating': self.get_review_rating,
            'image_url': self.get_image_url
        }
