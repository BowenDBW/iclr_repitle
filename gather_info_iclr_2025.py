import os
import time

from reptile import OpenreviewReptile
from storage import ICLRStorage
from tqdm import tqdm

def clear_console():
    # Clear console output for both Windows and Ubuntu
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":

    page_count = 372
    db = ICLRStorage('root', 'admin', 'iclr2025')
    submission_link = 'https://openreview.net/group?id=ICLR.cc/2025/Conference#tab-active-submissions'

    print("=> 1. Starting webdriver...")
    openreview = OpenreviewReptile(show_browser=False, chrome_driver=True)

    print("=> 2(1). Check if links are already crawled...")
    if db.is_link_empty():
        print("=> 2(2). Fetching article links...")
        all_links = openreview.get_article_links(submission_link, page_count)
        print(f"[INFO] Found {len(all_links)} articles.")
        for link in all_links:
            db.insert_article_link(link)
    else:
        print("=> 2(2). Links already crawled. Skipping...")

    print("=> 3. Fetching article links from database...")
    all_links = db.get_article_links()
    # turn tuples into list
    all_links = [link[0] for link in all_links]
    print(f"[INFO] Found {len(all_links)} articles.")

    print("=> 4. Fetching article information and saving to database...")
    link_prefix = 'https://openreview.net'
    time.sleep(1)

    # Fetch already recorded article count
    recorded_count = db.get_article_count()

    # Skip the first recorded_count links
    unrecorded_links = all_links[recorded_count:]

    print(f"[INFO] Found {len(unrecorded_links)} unrecorded articles.")

    for link in tqdm(unrecorded_links, desc="Processing articles"):
        article = openreview.get_article_info(link_prefix + link, 2025)
        if article is None:
            continue
        db.save_article(article)

    print("=> 4. Process completed.")
