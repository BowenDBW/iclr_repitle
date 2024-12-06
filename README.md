# An OpenReview Crawler
crawl, select and visualize submissions from a conference on OpenReview
The code in gather_info_iclr_2025.py is based on the ICLR 2025 conference

### Usage
##### 1. Read submissions from OpenReview
1. create a database and a table in MySQL, you can run the script in your mysql if your target is ICLR 2025
```sql
source create_db.sql
```
2. run the reptile script to gather information from OpenReview
```bash
python gather_info_iclr_2025.py
```     
##### 2. Select submissions based on ratings and/or your interests

##### 3. download targeting articles in pdg form

##### 4. Yet you can analyze the ratings, hot topics and visualize the results