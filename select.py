import storage
import re

if __name__ == "__main__":
    db = storage.ICLRStorage('root', 'admin', 'iclr2025')
    # get articles with high ratings and relevant keywords to reinforcement learning
    articles = db.get_by_avg_rating(7)
    # find articles with reinforcement learning keyword
    rl_articles = []
    for article in articles:
        if re.search(r'reinforcement', article[5]):
            rl_articles.append(article)
    print(f"find {len(rl_articles)} articles with reinforcement learning")
    # find articles with reinforcement learning keyword and diffusion model, diffusion use pattern matching
    dm_rl_articles = []
    for article in rl_articles:
        if re.search(r'diffusion', article[5]):
            dm_rl_articles.append(article)
    print(f"find {len(dm_rl_articles)} articles with reinforcement learning and diffusion model")
