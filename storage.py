import os
import hashlib
import pymysql

class Article:
    def __init__(self, year, serial, title, author, keywords, tl_dr,
                 primary_area, abstract, ratings, download_link):
        self.year = year
        self.serial = serial
        self.title = title
        self.author = author
        self.keywords = keywords
        self.abstract = abstract
        self.ratings = ratings
        self.tl_dr = tl_dr
        self.primary_area = primary_area
        self.download_link = download_link

class ICLRStorage:
    def __init__(self, username, password, database):
        self.__database_name = database
        self.__connection = pymysql.connect(
            host='localhost', user=username, password=password, database=database)
        self.__cursor = self.__connection.cursor()

    def save_article(self, article):
        # check duplicate
        query = "SELECT * FROM article WHERE title = %s"
        self.__cursor.execute(query, (article.title,))
        if self.__cursor.fetchone() is not None:
            return
        # check if folder /abstracts/{database_name} exists
        if not os.path.exists(f"abstracts/{self.__database_name}"):
            os.makedirs(f"abstracts/{self.__database_name}")
        # md5 to avoid too long file name
        filename = hashlib.md5(article.title.encode()).hexdigest()
        # save abstract to file
        with open(f"abstracts/{self.__database_name}/{filename}.txt", 'w') as f:
            f.write(article.abstract)
        query = (
            "INSERT INTO article (serial, title, author, keywords, tl_dr, primary_area, "
            "abstract_file_link, download_link, year) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
        abstract_file_link = f"abstracts/{self.__database_name}/{filename}.txt"
        values = (article.serial, article.title, article.author, article.keywords,
                  article.tl_dr, article.primary_area, abstract_file_link,
                  article.download_link, article.year)
        self.__cursor.execute(query, values)
        self.__connection.commit()
        # get id of this article
        query = "SELECT id FROM article WHERE title = %s"
        self.__cursor.execute(query, (article.title,))
        article_id = self.__cursor.fetchone()[0]
        # add ratings
        for rating in article.ratings:
            query = "INSERT INTO rating (article_id, rating) VALUES (%s, %s)"
            self.__cursor.execute(query, (article_id, rating))
            self.__connection.commit()

    def insert_article_link(self, link):
        query = "INSERT INTO article_link (link) VALUES (%s)"
        self.__cursor.execute(query, (link,))
        self.__connection.commit()

    def is_link_empty(self):
        query = "SELECT * FROM article_link"
        self.__cursor.execute(query)
        return self.__cursor.fetchone() is None

    def get_article_links(self):
        query = "SELECT link FROM article_link"
        self.__cursor.execute(query)
        return self.__cursor.fetchall()

    def get_abstract_links(self):
        query = "SELECT (id, title, abstract_file_link) FROM article"
        self.__cursor.execute(query)
        return self.__cursor.fetchall()

    def get_keywords(self):
        query = "SELECT (id, title, keywords) FROM article"
        self.__cursor.execute(query)
        return self.__cursor.fetchall()

    def get_articles_by_page(self, page_num):
        page_size = 500
        offset = (page_num - 1) * page_size
        query = "SELECT * FROM article LIMIT %s OFFSET %s"
        self.__cursor.execute(query, (page_size, offset))
        return self.__cursor.fetchall()
