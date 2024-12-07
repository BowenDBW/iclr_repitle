import os

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
            print(f"\nArticle {article.title} already exists.")
            return
        # check if folder /abstracts/{database_name} exists
        if not os.path.exists(f"abstracts/{self.__database_name}"):
            os.makedirs(f"abstracts/{self.__database_name}")
        # save abstract to file
        with open(f"abstracts/{self.__database_name}/{article.title}.txt", 'w') as f:
            f.write(article.abstract)
        query = (
            "INSERT INTO article (serial, title, author, keywords, tl_dr, primary_area, "
            "abstract_file_link, download_link, year) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
        abstract_file_link = f"abstracts/{self.__database_name}/{article.title}.txt"
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