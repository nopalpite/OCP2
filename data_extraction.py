import csv
import os
from book_scraper import Book
from category_scraper import *


def data_extraction(url):
    print("Beginning data extraction")
    for category in get_book_categories(url):
        category_name = get_category_name(category)
        csv_file = "./data/" + category_name + "/" + category_name + ".csv"
        os.makedirs(os.path.dirname(csv_file), exist_ok=True)
        img_path = "./data/" + category_name + "/img/"
        os.makedirs(os.path.dirname(img_path), exist_ok=True)
        with open(csv_file, 'w', newline='', encoding="utf-8") as csv_file:
            csv_columns = ['product_page_url', 'universal_product_code (upc)', 'title', 'price_including_tax',
                           'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating',
                           'image_url']
            writer = csv.DictWriter(csv_file, delimiter=';', fieldnames=csv_columns)
            writer.writeheader()
            books_url = []

            for book_url in get_books_from_category(category):
                book = Book(book_url)
                books_url.append(book.get_informations())
                page = requests.get(book.get_image_url()["image_url"])
                with open(img_path + book.get_upc()["universal_product_code (upc)"] + ".jpg", 'wb') as img:
                    img.write(page.content)

            writer.writerows(books_url)
            print('"' + category_name + '"' + " data successfully extracted")
    print("All data successfully extracted")
