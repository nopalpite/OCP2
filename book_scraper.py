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
        return {"product_page_url": self.url}

    def get_upc(self):
        upc_tag = self.soup.find("th", string="UPC")  # find tag by string
        upc = upc_tag.find_next().string
        return {"universal_product_code (upc)": upc}

    def get_title(self):
        title_tag = self.soup.find("h1")
        title = title_tag.string
        return {"title": title}

    def get_price(self):
        price_tag = self.soup.find("th", string="Price (incl. tax)")  # find tag by string
        price = price_tag.find_next().string
        return {"price_including_tax": price}

    def get_price_tax_free(self):
        price_tax_free_tag = self.soup.find("th", string="Price (excl. tax)")  # find tag by string
        price_tax_free = price_tax_free_tag.find_next().string
        return {"price_excluding_tax": price_tax_free}

    def get_availability(self):
        availability_tag = self.soup.find("th", string="Availability")
        availability = availability_tag.find_next().string
        return {"number_available": availability}

    def get_description(self):
        description_tag = self.soup.find(id="product_description")
        description = description_tag.find_next("p").string
        return {"product_description": description}

    def get_category(self):
        category_parent_tag = self.soup.find("ul")
        category_tag = category_parent_tag.find_all_next("a")[-1]
        category = category_tag.string
        return {"category": category}

    def get_review_rating(self):
        review_tag = self.soup.find("p", class_=re.compile('star-rating'))
        review = review_tag['class'][-1]
        return {"review_rating": review}

    def get_image_url(self):
        image_url_tag = self.soup.find("img")
        image_relative_url = image_url_tag['src']
        image_url = urljoin(self.url, image_relative_url)
        return {"image_url": image_url}

    def get_informations(self):
        informations = {}
        informations.update(self.get_url())
        informations.update(self.get_upc())
        informations.update(self.get_title())
        informations.update(self.get_price())
        informations.update(self.get_price_tax_free())
        informations.update(self.get_availability())
        informations.update(self.get_description())
        informations.update(self.get_category())
        informations.update(self.get_review_rating())
        informations.update(self.get_image_url())
        return informations
