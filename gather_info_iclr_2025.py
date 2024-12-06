import os
import time

from reptile import OpenreviewReptile
from storage import ICLRStorage
from tqdm import tqdm

def clear_console():
    # Clear console output for both Windows and Ubuntu
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":

    page_count = 373

    print("=> 1. Starting webdriver...")
    openreview = OpenreviewReptile(show_browser=False)

    print("=> 2. Fetching article links...")
    submission_link = 'https://openreview.net/group?id=ICLR.cc/2025/Conference#tab-active-submissions'
    all_links = openreview.get_article_links(submission_link, page_count)
    print(f"[INFO] Found {len(all_links)} articles.")

    # 2. get all articles' information and save them to database
    print("=> 3. Fetching article information and saving to database...")
    link_prefix = 'https://openreview.net'
    db = ICLRStorage('root', 'admin', 'iclr2025')

    time.sleep(1)
    for link in tqdm(all_links, desc="Processing articles"):
        article = openreview.get_article_info(link_prefix + link, 2025)
        if article is None:
            continue
        db.save_article(article)

    print("=> 4. Process completed.")
