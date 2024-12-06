import time
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from storage import Article
from tqdm import tqdm


class OpenreviewReptile:
    def __init__(self, show_browser=False):
        self.__show_browser = show_browser
        self.__clear_cmd = 'cls' if os.name == 'nt' else 'clear'
        if show_browser:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu" if os.name == 'nt' else '--no-sandbox')
            self.__driver = webdriver.Chrome(options=chrome_options)
        else:
            self.__driver = webdriver.Chrome()

    def get_article_links(self, link, page_count):
        self.__driver.get(link)
        # Wait for the page to load
        wait = WebDriverWait(self.__driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="active-submissions"]/div/div/ul')))

        all_links = []
        # Iterate through all pages
        for page in tqdm(range(1, page_count), desc="Fetching pages", unit="page", ncols=100):
            # Wait for the current page's list to load
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="active-submissions"]/div/div/ul')))

            # Get the current page's HTML content
            page_source = self.__driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')

            # Extract matching links
            ul = soup.select_one('#active-submissions > div > div > ul')
            if ul:
                for li in ul.find_all('li'):
                    h4 = li.find('h4')
                    if h4:
                        a_tags = h4.find_all('a')
                        for a in a_tags:
                            if 'pdf-link' not in a.get('class', []):
                                all_links.append(a['href'])

            # Click next page
            next_page_li = self.__driver.find_element(By.XPATH,
                                               f'//*[@id="active-submissions"]/div/div/nav/ul/li/a[text()="{page + 1}"]')
            next_page_button = wait.until(EC.element_to_be_clickable(next_page_li))
            next_page_button.click()

        return all_links

    # 输入文章链接 获取标题，关键词，摘要，主要领域，投稿编号，3-5个评分
    def get_article_info(self, link, year):
        self.__driver.get(link)

        wait = WebDriverWait(self.__driver, 100)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div/div[1]/div[1]/h2')))

        # 提取信息
        keywords = None
        tl_dr = None
        abstract = None
        primary_area = None

        title = self.__driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/div[1]/h2').text

        a_index_no_sure = 1
        while True:
            try:
                label_xpath = f'//*[@id="content"]/div/div[1]/div[4]/div[{a_index_no_sure}]/strong'
                label = self.__driver.find_element(By.XPATH, label_xpath).text.strip().strip(':')

                if label == "Keywords":
                    value_xpath = f'//*[@id="content"]/div/div[1]/div[4]/div[{a_index_no_sure}]/span'
                    keywords = self.__driver.find_element(By.XPATH, value_xpath).text
                elif label == "TL;DR":
                    value_xpath = f'//*[@id="content"]/div/div[1]/div[4]/div[{a_index_no_sure}]/span'
                    tl_dr = self.__driver.find_element(By.XPATH, value_xpath).text
                elif label == "Abstract":
                    value_xpath = f'//*[@id="content"]/div/div[1]/div[4]/div[{a_index_no_sure}]/div/p'
                    abstract = self.__driver.find_element(By.XPATH, value_xpath).text
                elif label == "Primary Area":
                    value_xpath = f'//*[@id="content"]/div/div[1]/div[4]/div[{a_index_no_sure}]/span'
                    primary_area = self.__driver.find_element(By.XPATH, value_xpath).text
                elif label == "Submission Number":
                    value_xpath = f'//*[@id="content"]/div/div[1]/div[4]/div[{a_index_no_sure}]/span'
                    serial = self.__driver.find_element(By.XPATH, value_xpath).text
                a_index_no_sure += 1
            except:
                break

        download_link = self.__driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/div[1]/div/a').get_attribute(
            'href')
        # Extract ratings
        ratings = []
        comment_index = 1
        while True:
            loading_text = self.__driver.find_element(By.XPATH, '//*[@id="forum-replies"]').text
            if loading_text != "LOADING":
                break
            time.sleep(1)

        while comment_index < 20:
            try:
                rating1_xpath = f'//*[@id="forum-replies"]/div[{comment_index}]/div[4]/div/div[2]/span'
                rating2_xpath = f'//*[@id="forum-replies"]/div[{comment_index}]/div[4]/div/div[3]/span'
                rating3_xpath = f'//*[@id="forum-replies"]/div[{comment_index}]/div[4]/div/div[4]/span'
                rating1 = self.__driver.find_element(By.XPATH, rating1_xpath).text
                rating2 = self.__driver.find_element(By.XPATH, rating2_xpath).text
                rating3 = self.__driver.find_element(By.XPATH, rating3_xpath).text

                rating1 = int(rating1.split(":")[0].strip())
                rating2 = int(rating2.split(":")[0].strip())
                rating3 = int(rating3.split(":")[0].strip())

                ratings.append(rating1 + rating2 + rating3)
                comment_index += 1
            except:
                comment_index += 1
                continue

        return Article(year, serial, title, None, keywords, tl_dr,
                       primary_area, abstract, ratings, download_link)

