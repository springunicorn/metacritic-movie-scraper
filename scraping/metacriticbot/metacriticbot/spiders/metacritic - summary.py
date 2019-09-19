
# To use the summary bot, do the following:
# 1. Uncomment metacritic - summary.py (except this block comment)
# 2. Comment out metacritic - original.py
# 3. In pipelines.py, comment out line 52 (item = Movie())
#    and uncomment line 53 (item = Summery())
# 4. Comment out every line in MetacriticbotPipeline.process_item from
#    pipelines.py except the return statement.
# 5. Now run bot using the same command to run the orignial bot.


# import scrapy
# from scrapy.selector import Selector
# from scrapy.http import Request
# import json
# from metacriticbot.items import Summary
#
#
# # Helper functions
# def safe_extract(selector, xpath_query):
#     """
#     Helper function that extracts info from selector object
#     using the xpath query constrains.
#     If nothing can be extracted, NA is returned.
#     """
#     val = selector.xpath(xpath_query).extract()
#     return val[0].strip() if val else 'NA'
#
#
# def safe_list_extract(selector, xpath_query):
#     """
#     Helper function that extracts LIST info from selector object
#     using the xpath query constrains.
#     If nothing can be extracted, NA is returned.
#     """
#     val = selector.xpath(xpath_query).extract()
#     result_string = ''
#     for el in val:
#         result_string += el.strip() + ', '
#     return result_string[:-2] if len(result_string) > 0 else 'NA'
#
#
# class MetacriticSummarySpider(scrapy.Spider):
#     """
#     Goal: Scrape all PC games
#     1. Start with "action" genre: start_url =
#        "http://www.metacritic.com/browse/games/genre/date/action/pc"
#     2. Get links for every genre page
#     3. Get links for page 1..n for genre
#     4. Take "genre" field from sidebar in game list,
#        other fields from game page itself.
#     5. Go to next genre.
#     6. Repeat.
#     """
#     name = "metacritic"
#     allowed_domains = ["metacritic.com"]
#     start_urls = [
#             "https://www.metacritic.com/browse/movies/genre/date/action?view=detailed"
#             ]
#
#     # Get genre list from start_url, generate requests to parse genre pages later
#     def parse(self, response):
#         genres = [s.split()[1].split('_', 1)[1].replace("_", "-")
#                   for s in response.xpath('//ul[@class="genre_nav"]'
#                                           + '/li/@class').extract()]
#         genre_links = ["https://www.metacritic.com/browse/movies/genre/date/"
#                        + genre for genre in genres]
#
#         requests = [Request(url=URL,
#                             callback=self.parse_genre) for URL in genre_links]
#         self.log("###INITIAL PARSING ### " + str(len(genre_links)) + " Genres IN THIS TOTAL LIST")
#         return requests
#
#     # Get all pages for a genre, send them to page parser
#     def parse_genre(self, response):
#         try:
#             page_links = [response.url + "?page="
#                           + str(i) for i in range(
#                               int(response.xpath('//li[@class="page'
#                                   + 'last_page"]/a/text()').extract()[0])
#                           )]
#         except IndexError:
#             page_links = [response.url]
#
#         requests = [Request(url=URL,
#                             callback=self.parse_page) for URL in page_links]
#         self.log("###PARSING GENRE### "
#                  + str(len(page_links))
#                  + " PAGES IN THIS GENRE")
#         return requests
#
#     # Get all movies for a page
#     def parse_page(self, response):
#         movie_links = ["https://www.metacritic.com"
#                        + postfix for postfix in
#                        response.xpath('//ol[@class="list_products '
#                                       + 'list_product_condensed"]'
#                                       + '/li/div/div/a/@href').extract()]
#         meta_genre = response.xpath('//div[@class="module products_module'
#                                     + 'list_product_condensed_module "]/div/'
#                                     + 'div/h2[@class="module_title"]/text()'
#                                     ).extract()[0].strip()
#         header = {}
#         header['Accept'] = 'text/html,application/xhtml+xml,'\
#             + 'application/xml;q=0.9,*/*;q=0.8'
#         header['Accept-Language'] = 'en'
#         header['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '\
#             + 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 '\
#             + 'Safari/537.36'
#         header['Accept-Encoding'] = 'gzip,deflate'
#         header['Connection'] = 'Keep-Alive'
#         requests = [Request(url=URL + "/details",
#                             callback=self.parse_movie,
#                             meta={'genre': meta_genre},
#                             headers=header) for URL in movie_links]
#         self.log("###PARSING PAGE### " + str(len(movie_links))
#                  + " MOVIES IN THIS PAGE")
#         return requests
#
#     def parse_movie(self, response):
#         sel = Selector(response, type='html')
#         summary = Summary()
#         # General info
#         summary['name'] =\
#             safe_extract(sel, '//*[@id="mantle_skin"]/div[4]/div/div[1]/div[2]'
#                          + '/div[2]/div[1]/a/h1/text()')
#         summary['link'] = response.url[:-8]
#         summary['description'] =\
#             safe_extract(sel, '//*[@id="mantle_skin"]/div[4]/div/div[1]/div[2]'
#                          + '/div[2]/div[3]/span[2]/text()')
#
#         yield summary
