# coding: utf-8
import csv
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

ROOT_URL = "http://books.toscrape.com/"
CATEGORY_URL = "http://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html"
URL = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/"
CSV_FILE = './output.csv'


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


def get_books_from_category(url):
    category_pages = [url]
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    is_next_page = soup.find("li", class_="next")
    while is_next_page is not None:
        category_pages.append(urljoin(url, is_next_page.find("a")["href"]))
        page = requests.get(urljoin(url, is_next_page.find("a")["href"]))
        soup = BeautifulSoup(page.content, 'html.parser')
        is_next_page = soup.find("li", class_="next")
    books_url = []
    for category_page in category_pages:
        page = requests.get(category_page)
        soup = BeautifulSoup(page.content, 'html.parser')
        books_tags = soup.find_all("h3")
        for tag in books_tags:
            book_relative_url = tag.find("a")["href"]
            book_url = urljoin(url, book_relative_url)
            books_url.append(book_url)

    return books_url


books_url = get_books_from_category(CATEGORY_URL)

with open(CSV_FILE, 'w', newline='', encoding="utf-8") as csv_file:
    csv_columns = ['product_page_url', 'universal_product_code (upc)', 'title', 'price_including_tax',
                   'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating',
                   'image_url']
    writer = csv.DictWriter(csv_file, delimiter=';', fieldnames=csv_columns)
    writer.writeheader()
    books_information = []
    for book_url in books_url:
        book = Book(book_url)
        books_information.append(book.get_informations())
    for data in books_information:
        writer.writerow(data)
