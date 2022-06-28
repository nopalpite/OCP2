from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def get_book_categories(url):
    categories = []
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    category_tags = soup.find("ul", class_="nav nav-list").find_all("a")
    for tag in category_tags:
        if "books_1" not in tag.get("href"):
            categories.append(urljoin(url, tag.get("href")))
    return categories


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


def get_category_name(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup.find("h1").string
