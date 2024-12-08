import time

import storage
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import re

# draw word cloud of keywords in articles with rating higher than 8
if __name__ == "__main__":
    db = storage.ICLRStorage('root', 'admin', 'iclr2025')
    articles = db.get_by_avg_rating(8)
    keywords = []
    for article in articles:
        keywords.extend(article[5].split(','))
    keywords = [phrase.strip().title() for phrase in keywords]
    keywords = [re.sub(r'\b(\w+)s\b$', r'\1', phrase) for phrase in keywords]
    counter = Counter(keywords)
    most_common_phrases = counter.most_common(20)
    phrases, frequencies = zip(*most_common_phrases)

    # 绘制条形图
    plt.figure(figsize=(10, 6))
    plt.barh(phrases, frequencies, color='skyblue')
    plt.xlabel('Frequency')
    plt.ylabel('Phrases')
    plt.title('Top 20 Most Frequent Phrases')
    plt.gca().invert_yaxis()  # 反转Y轴，使频率最高的短语在顶部
    plt.yticks(fontsize=6)  # 调整Y轴刻度字体大小
    plt.savefig('bar_chart.png')
    plt.show()
    # save bar chart to file
    time.sleep(1)

    # 绘制词云
    wc = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(counter)
    plt.figure(figsize=(10, 6))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.show()
    # save word cloud to file
    wc.to_file('word_cloud.png')