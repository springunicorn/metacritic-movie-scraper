metacritic-movie-sraping
===================

Movie scraper for metacritic.com. This movie scraper is modified from this [game scraper written by codenotfound](https://github.com/codenotfound/metacritic-analysis).

The dataset includes the following fields:
name, link, datePublished, director, publisher, actor, maturity_rating, genre, metascore, critics_reviews_count, user_score, user_reviews_count, description.


# How to use this scraper:
run `scrapy crawl metacritic` from within /scraping/metacriticbot

### Requirements to run code:
Python
* Scrapy
* xlwt

# Note
The original bot cannot scrape some of the descriptions correctly without accessing the detail page of movie. Read metacritic - summary.py for more information.
