# coding: utf-8
import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from book_scraper import Book

ROOT_URL = "http://books.toscrape.com/"
CATEGORY_URL = "http://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html"
URL = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/"
CSV_FILE = './output.csv'



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
