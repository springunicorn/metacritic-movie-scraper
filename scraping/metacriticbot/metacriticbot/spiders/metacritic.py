# import scrapy
# from scrapy.selector import Selector
# from scrapy.http import Request
# import json
# from metacriticbot.items import Movie
#
# #Helper functions
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
# class MetacriticSpider(scrapy.Spider):
#     """
#     Goal: Scrape all PC games
#     1. Start with "action" genre: start_url = "http://www.metacritic.com/browse/games/genre/date/action/pc"
#     2. Get links for every genre page
#     3. Get links for page 1..n for genre
#     4. Take "genre" field from sidebar in game list, other fields from game page itself.
#     5. Go to next genre.
#     6. Repeat.
#     """
#     name = "metacritic"
#     allowed_domains = ["metacritic.com"]
#     start_urls = [
#             "https://www.metacritic.com/browse/movies/genre/date/action?view=detailed"
#             ]
#
#
#     #Get genre list from start_url, generate requests to parse genre pages later
#     def parse(self, response):
#         # genres = [s.split()[1].split('_', 1)[1].replace("_", "-") for s in response.xpath('//ul[@class="genre_nav"]/li/@class').extract()]
#         # genre_links = ["https://www.metacritic.com/browse/movies/genre/date/" + genre for genre in genres]
#         #
#         # requests = [Request(url = URL, callback = self.parse_genre) for URL in genre_links]
#         # self.log("###INITIAL PARSING ### " + str(len(genre_links)) + " Genres IN THIS TOTAL LIST")
#         # return requests
#         requests = [Request(url = URL, callback = self.parse_movie) for URL in toRedo]
#         return requests
#
#     #Get all pages for a genre, send them to page parser
#     def parse_genre(self, response):
#         try:
#             page_links = [response.url + "?page=" + str(i) for i in range(int(response.xpath('//li[@class="page last_page"]/a/text()').extract()[0]))]
#         except IndexError:
#             page_links = [response.url]
#
#         requests = [Request(url = URL, callback = self.parse_page) for URL in page_links]
#         self.log("###PARSING GENRE### " + str(len(page_links)) + " PAGES IN THIS GENRE")
#         return requests
#
#     #Get all movies for a page
#     def parse_page(self, response):
#         movie_links = ["https://www.metacritic.com" + postfix for postfix in response.xpath('//ol[@class="list_products list_product_condensed"]/li/div/div/a/@href').extract()]
#         meta_genre = response.xpath('//div[@class="module products_module list_product_condensed_module "]/div/div/h2[@class="module_title"]/text()').extract()[0].strip()
#         header = {}
#         header['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
#         header['Accept-Language'] = 'en'
#         header['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
#         header['Accept-Encoding'] = 'gzip,deflate'
#         header['Connection'] = 'Keep-Alive'
#         requests = [Request(url = URL+"/critic-reviews", callback = self.parse_movie, meta = {'genre': meta_genre}, headers=header) for URL in movie_links]
#         self.log("###PARSING PAGE### " + str(len(movie_links)) + " MOVIES IN THIS PAGE")
#         return requests
#
#     def parse_movie(self, response):
#         sel = Selector(response, type='html')
#         movie = Movie()
#         # General info
#         movie['name'] = safe_extract(sel, '//*[@id="mantle_skin"]/div[4]/div/div[1]/div[2]/a/h1/text()')
#         movie['link'] = response.url
#         #infojson = json.loads(safe_extract(sel,'//script[@type="application/ld+json"]/text()'))
#         #print(infojson)
#         movie['datePublished'] = safe_extract(sel, '//span[@class="release_date"]/span[2]/text()')
#         movie['sources'] = ', '.join(sel.xpath('//span[@class="source"]/a/text()').extract())
#         movie['authors'] = ', '.join(sel.xpath('//span[@class="author"]/a/text()').extract())
#         summaryList = sel.xpath('//div[@class="summary"]/a[@class="no_hover"]/text()').extract()
#         movie['summary'] = ""
#         for s in summaryList:
#             trimmed = s.strip()
#             movie['summary'] = "||".join([movie['summary'],trimmed])
#         movie['scores'] = []
#         movie['scores'] += sel.xpath('//div[@class="metascore_w large movie positive indiv perfect"]/text()').extract()
#         movie['scores'] += sel.xpath('//div[@class="metascore_w large movie positive indiv"]/text()').extract()
#         movie['scores'] += sel.xpath('//div[@class="metascore_w large movie mixed indiv"]/text()').extract()
#         movie['scores'] += sel.xpath('//div[@class="metascore_w large movie negative indiv"]/text()').extract()
#         movie['scores'] = ', '.join(movie['scores'])
#
#         yield movie
#
# toRedo = ['https://www.metacritic.com/movie/the-kill-team-2019/critic-reviews',
#     'https://www.metacritic.com/movie/the-command/critic-reviews',
#     'https://www.metacritic.com/movie/citizen-kane-1941/critic-reviews',
#     'https://www.metacritic.com/movie/pokemon-the-movie-2000/critic-reviews',
#     'https://www.metacritic.com/movie/dr-dolittle/critic-reviews',
#     'https://www.metacritic.com/movie/the-wizard-of-oz-re-release/critic-reviews',
#     'https://www.metacritic.com/movie/pokmon-the-first-movie---mewtwo-strikes-back%21/critic-reviews',
#     'https://www.metacritic.com/movie/the-grinch/critic-reviews',
#     'https://www.metacritic.com/movie/beetlejuice/critic-reviews',
#     'https://www.metacritic.com/movie/hotel-transylvania-3-summer-vacation/critic-reviews',
#     'https://www.metacritic.com/movie/the-night-is-short-walk-on-girl/critic-reviews',
#     'https://www.metacritic.com/movie/the-big-bad-fox-other-tales/critic-reviews',
#     'https://www.metacritic.com/movie/the-boss-baby/critic-reviews',
#     'https://www.metacritic.com/movie/spark-a-space-tail/critic-reviews',
#     'https://www.metacritic.com/movie/fantastic-beasts-the-crimes-of-grindelwald/critic-reviews',
#     'https://www.metacritic.com/movie/mowgli-legend-of-the-jungle/critic-reviews',
#     'https://www.metacritic.com/movie/the-lego-movie-2-the-second-part/critic-reviews',
#     'https://www.metacritic.com/movie/wonder-park/critic-reviews',
#     'https://www.metacritic.com/movie/pokemon-detective-pikachu/critic-reviews',
#     'https://www.metacritic.com/movie/captain-underpants-the-first-epic-movie/critic-reviews',
#     'https://www.metacritic.com/movie/goodbye-christopher-robin/critic-reviews',
#     'https://www.metacritic.com/movie/shaun-the-sheep-movie/critic-reviews',
#     'https://www.metacritic.com/movie/the-peanuts-movie/critic-reviews',
#     'https://www.metacritic.com/movie/alvin-and-the-chipmunks-the-road-chip/critic-reviews',
#     'https://www.metacritic.com/movie/the-angry-birds-movie/critic-reviews',
#     'https://www.metacritic.com/movie/alice-through-the-looking-glass/critic-reviews',
#     'https://www.metacritic.com/movie/ice-age-collision-course/critic-reviews',
#     'https://www.metacritic.com/movie/through-a-lens-darkly-black-photographers-and-the-emergence-of-a-people/critic-reviews',
#     'https://www.metacritic.com/movie/the-book-of-life/critic-reviews',
#     'https://www.metacritic.com/movie/the-secret-world-of-arrietty/critic-reviews',
#     'https://www.metacritic.com/movie/madagascar-3-europes-most-wanted/critic-reviews',
#     'https://www.metacritic.com/movie/step-up-to-the-plate/critic-reviews',
#     'https://www.metacritic.com/movie/wreck-it-ralph/critic-reviews',
#     'https://www.metacritic.com/movie/the-penguin-king-3d/critic-reviews',
#     'https://www.metacritic.com/movie/one-candle-two-candles/critic-reviews',
#     'https://www.metacritic.com/movie/monsters-university/critic-reviews',
#     'https://www.metacritic.com/movie/mia-and-the-migoo/critic-reviews',
#     'https://www.metacritic.com/movie/spy-kids-all-the-time-in-the-world/critic-reviews',
#     'https://www.metacritic.com/movie/happy-feet-two/critic-reviews',
#     'https://www.metacritic.com/movie/alvin-and-the-chipmunks-chipwrecked/critic-reviews',
#     'https://www.metacritic.com/movie/wes-cravens-new-nightmare/critic-reviews',
#     'https://www.metacritic.com/movie/fantastic-four-rise-of-the-silver-surfer/critic-reviews',
#     'https://www.metacritic.com/movie/pusher-iii-im-the-angel-of-death/critic-reviews',
#     'https://www.metacritic.com/movie/fanny-and-alexander-re-release/critic-reviews',
#     'https://www.metacritic.com/movie/metropolis-re-release/critic-reviews',
#     'https://www.metacritic.com/movie/beauty-and-the-beast-re-release/critic-reviews',
#     'https://www.metacritic.com/movie/the-discreet-charm-of-the-bourgeoisie-re-release/critic-reviews',
#     'https://www.metacritic.com/movie/vampires/critic-reviews',
#     'https://www.metacritic.com/movie/the-tale-of-the-princess-kaguya/critic-reviews',
#     'https://www.metacritic.com/movie/legend-of-the-mountain-1979/critic-reviews',
#     'https://www.metacritic.com/movie/the-leopard-re-release/critic-reviews',
#     'https://www.metacritic.com/movie/the-battle-of-algiers-re-release/critic-reviews',
#     'https://www.metacritic.com/movie/welcome-to-marwen/critic-reviews',
#     'https://www.metacritic.com/movie/shazam%21/critic-reviews',
#     'https://www.metacritic.com/movie/the-battleship-island/critic-reviews',
#     'https://www.metacritic.com/movie/star-wars-episode-viii---the-last-jedi/critic-reviews',
#     'https://www.metacritic.com/movie/rogue-one-a-star-wars-story/critic-reviews',
#     'https://www.metacritic.com/movie/sabans-power-rangers/critic-reviews',
#     'https://www.metacritic.com/movie/belladonna-of-sadness-1973/critic-reviews',
#     'https://www.metacritic.com/movie/lost-river/critic-reviews',
#     'https://www.metacritic.com/movie/one-two/critic-reviews',
#     'https://www.metacritic.com/movie/this-is-the-end/critic-reviews',
#     'https://www.metacritic.com/movie/ruby-sparks/critic-reviews',
#     'https://www.metacritic.com/movie/jack-the-giant-slayer/critic-reviews',
#     'https://www.metacritic.com/movie/underworld-awakening/critic-reviews',
#     'https://www.metacritic.com/movie/the-post/critic-reviews',
#     'https://www.metacritic.com/movie/the-12th-man/critic-reviews',
#     'https://www.metacritic.com/movie/smiling-through-the-apocalypse-esquire-in-the-60s/critic-reviews',
#     'https://www.metacritic.com/movie/the-liberator/critic-reviews',
#     'https://www.metacritic.com/movie/tokyo-waka-a-city-poem/critic-reviews',
#     'https://www.metacritic.com/movie/uprising-2013/critic-reviews',
#     'https://www.metacritic.com/movie/granito-how-to-nail-a-dictator/critic-reviews',
#     'https://www.metacritic.com/movie/resident-evil-retribution/critic-reviews',
#     'https://www.metacritic.com/movie/in-cold-blood-re-release/critic-reviews',
#     'https://www.metacritic.com/movie/overlord-re-release/critic-reviews',
#     'https://www.metacritic.com/movie/even-the-rain-tambien-la-lluvia/critic-reviews',
#     'https://www.metacritic.com/movie/the-desert-of-forbidden-art/critic-reviews',
#     'https://www.metacritic.com/movie/becket-re-release/critic-reviews',
#     'https://www.metacritic.com/movie/repulsion-re-release/critic-reviews',
#     'https://www.metacritic.com/movie/eyes-without-a-face-re-release/critic-reviews',
#     'https://www.metacritic.com/movie/thirteen-ghosts/critic-reviews',
#     'https://www.metacritic.com/movie/halloween-5-the-revenge-of-michael-myers/critic-reviews',
#     'https://www.metacritic.com/movie/alien-1979/critic-reviews',
#     'https://www.metacritic.com/movie/the-exorcist-1973/critic-reviews',
#     'https://www.metacritic.com/movie/the-possession/critic-reviews',
#     'https://www.metacritic.com/movie/the-offering/critic-reviews',
#     'https://www.metacritic.com/movie/patrick-evil-awakens/critic-reviews',
#     'https://www.metacritic.com/movie/bad-milo%21/critic-reviews',
#     'https://www.metacritic.com/movie/evil-dead-2013/critic-reviews',
#     'https://www.metacritic.com/movie/trollhunter/critic-reviews',
#     'https://www.metacritic.com/movie/the-devil-inside/critic-reviews',
#     'https://www.metacritic.com/movie/halloween-2007/critic-reviews',
#     'https://www.metacritic.com/movie/the-last-waltz-re-release/critic-reviews',
#     'https://www.metacritic.com/movie/a-hard-days-night-re-release/critic-reviews',
#     'https://www.metacritic.com/movie/incident-in-a-ghostland/critic-reviews',
#     'https://www.metacritic.com/movie/unfriended-dark-web/critic-reviews',
#     'https://www.metacritic.com/movie/the-meg/critic-reviews',
#     'https://www.metacritic.com/movie/the-possession-of-hannah-grace/critic-reviews',
#     'https://www.metacritic.com/movie/the-housemaid-2018/critic-reviews',
#     'https://www.metacritic.com/movie/tyler-perrys-boo-2%21-a-madea-halloween/critic-reviews',
#     'https://www.metacritic.com/movie/shin-godzilla-godzilla-resurgence/critic-reviews',
#     'https://www.metacritic.com/movie/here-and-now/critic-reviews',
#     'https://www.metacritic.com/movie/the-music-of-strangers-yo-yo-ma-and-the-silk-road-ensemble/critic-reviews',
#     'https://www.metacritic.com/movie/justin-timberlake-%2B-the-tennessee-kids/critic-reviews',
#     'https://www.metacritic.com/movie/pulp-a-film-about-life-death-supermarkets/critic-reviews',
#     'https://www.metacritic.com/movie/we-are-mari-pepa/critic-reviews',
#     'https://www.metacritic.com/movie/pussy-riot-a-punk-prayer/critic-reviews',
#     'https://www.metacritic.com/movie/step-up-revolution/critic-reviews',
#     'https://www.metacritic.com/movie/ornette-made-in-america-1985/critic-reviews',
#     'https://www.metacritic.com/movie/glee-the-3d-concert-movie/critic-reviews',
#     'https://www.metacritic.com/movie/gainsbourg-a-heroic-life/critic-reviews',
#     'https://www.metacritic.com/movie/dave-chappelles-block-party/critic-reviews',
#     'https://www.metacritic.com/movie/bride-prejudice/critic-reviews',
#     'https://www.metacritic.com/movie/love-beats-rhymes/critic-reviews',
#     'https://www.metacritic.com/movie/the-night-of-the-hunter-re-release/critic-reviews',
#     'https://www.metacritic.com/movie/mysterious-object-at-noon/critic-reviews',
#     'https://www.metacritic.com/movie/seven/critic-reviews',
#     'https://www.metacritic.com/movie/first-night/critic-reviews',
#     'https://www.metacritic.com/movie/the-last-five-years/critic-reviews',
#     'https://www.metacritic.com/movie/funny-girl-re-release/critic-reviews',
#     'https://www.metacritic.com/movie/donnie-darko-the-directors-cut/critic-reviews',
#     'https://www.metacritic.com/movie/the-monk/critic-reviews',
#     'https://www.metacritic.com/movie/nymphomaniac-volume-ii/critic-reviews',
#     'https://www.metacritic.com/movie/about-elly-2009/critic-reviews',
#     'https://www.metacritic.com/movie/atlas-shrugged-part-i/critic-reviews',
#     'https://www.metacritic.com/movie/sherlock-holmes-a-game-of-shadows/critic-reviews',
#     'https://www.metacritic.com/movie/a-man-vanishes-1967/critic-reviews',
#     'https://www.metacritic.com/movie/red-riding-trilogy/critic-reviews',
#     'https://www.metacritic.com/movie/the-passenger-re-release/critic-reviews',
#     'https://www.metacritic.com/movie/solaris-re-release/critic-reviews',
#     'https://www.metacritic.com/movie/annie-hall-1977/critic-reviews',
#     'https://www.metacritic.com/movie/days-of-heaven-re-release/critic-reviews',
#     'https://www.metacritic.com/movie/alive-inside-2014/critic-reviews',
#     'https://www.metacritic.com/movie/holmes-watson/critic-reviews',
#     'https://www.metacritic.com/movie/searching/critic-reviews',
#     'https://www.metacritic.com/movie/the-vanishing-of-sidney-hall/critic-reviews',
#     'https://www.metacritic.com/movie/exposed-2015/critic-reviews',
#     'https://www.metacritic.com/movie/fireworks-wednesday-2006/critic-reviews',
#     'https://www.metacritic.com/movie/the-divergent-series-allegiant/critic-reviews',
#     'https://www.metacritic.com/movie/romeo-and-juliet/critic-reviews',
#     'https://www.metacritic.com/movie/days-of-being-wild-re-release/critic-reviews',
#     'https://www.metacritic.com/movie/modern-times-re-release/critic-reviews',
#     'https://www.metacritic.com/movie/the-adventures-of-robin-hood-re-release/critic-reviews',
#     'https://www.metacritic.com/movie/the-crime-of-padre-amaro/critic-reviews',
#     'https://www.metacritic.com/movie/pepe-le-moko-re-release/critic-reviews',
#     'https://www.metacritic.com/movie/tristan-and-isolde/critic-reviews',
#     'https://www.metacritic.com/movie/russian-dolls/critic-reviews',
#     'https://www.metacritic.com/movie/lenfant-the-child/critic-reviews',
#     'https://www.metacritic.com/movie/apres-vous-after-you/critic-reviews',
#     'https://www.metacritic.com/movie/the-soft-skin-1969/critic-reviews',
#     'https://www.metacritic.com/movie/love-friendship/critic-reviews',
#     'https://www.metacritic.com/movie/only-yesterday-1991/critic-reviews',
#     'https://www.metacritic.com/movie/some-kind-of-beautiful/critic-reviews',
#     'https://www.metacritic.com/movie/think-like-a-man-too/critic-reviews',
#     'https://www.metacritic.com/movie/what-if-2014/critic-reviews',
#     'https://www.metacritic.com/movie/hope-springs/critic-reviews',
#     'https://www.metacritic.com/movie/nothing-but-a-man-1964/critic-reviews',
#     'https://www.metacritic.com/movie/tiny-times-20/critic-reviews',
#     'https://www.metacritic.com/movie/romeo-juliet/critic-reviews',
#     'https://www.metacritic.com/movie/the-five-year-engagement/critic-reviews',
#     'https://www.metacritic.com/movie/to-rome-with-love/critic-reviews',
#     'https://www.metacritic.com/movie/a-brighter-summer-day-1991/critic-reviews',
#     'https://www.metacritic.com/movie/the-art-of-getting-by/critic-reviews',
#     'https://www.metacritic.com/movie/hot-summer-days-chuen-sing-yit-luen---yit-lat-lat/critic-reviews',
#     'https://www.metacritic.com/movie/the-road-warrior/critic-reviews',
#     'https://www.metacritic.com/movie/long-shot-2019/critic-reviews',
#     'https://www.metacritic.com/movie/non-fiction/critic-reviews',
#     'https://www.metacritic.com/movie/double-lover/critic-reviews',
#     'https://www.metacritic.com/movie/marie-curie-the-courage-of-knowledge/critic-reviews',
#     'https://www.metacritic.com/movie/ocean-waves-1993/critic-reviews',
#     'https://www.metacritic.com/movie/the-legend-of-tarzan/critic-reviews',
#     'https://www.metacritic.com/movie/my-king/critic-reviews',
#     'https://www.metacritic.com/movie/plus-one/critic-reviews',
#     'https://www.metacritic.com/movie/big-ass-spider%21/critic-reviews',
#     'https://www.metacritic.com/movie/edge-of-tomorrow/critic-reviews',
#     'https://www.metacritic.com/movie/transformers-age-of-extinction/critic-reviews',
#     'https://www.metacritic.com/movie/gi-joe-retaliation/critic-reviews',
#     'https://www.metacritic.com/movie/star-trek-into-darkness/critic-reviews',
#     'https://www.metacritic.com/movie/battle-royale-2000/critic-reviews',
#     'https://www.metacritic.com/movie/the-watch/critic-reviews',
#     'https://www.metacritic.com/movie/world-on-a-wire-1973/critic-reviews',
#     'https://www.metacritic.com/movie/rise-of-the-planet-of-the-apes/critic-reviews',
#     'https://www.metacritic.com/movie/x2-x-men-united/critic-reviews',
#     'https://www.metacritic.com/movie/independence-day-resurgence/critic-reviews',
#     'https://www.metacritic.com/movie/hardcore-henry/critic-reviews',
#     'https://www.metacritic.com/movie/high-rise-2015/critic-reviews',
#     'https://www.metacritic.com/movie/taxi-driver-1976/critic-reviews',
#     'https://www.metacritic.com/movie/the-french-connection-1971/critic-reviews',
#     'https://www.metacritic.com/movie/high-noon-re-release/critic-reviews',
#     'https://www.metacritic.com/movie/point-break-2015/critic-reviews',
#     'https://www.metacritic.com/movie/john-mcenroe-in-the-realm-of-perfection/critic-reviews',
#     'https://www.metacritic.com/movie/rififi-re-release/critic-reviews',
#     'https://www.metacritic.com/movie/september-tapes/critic-reviews',
#     'https://www.metacritic.com/movie/le-cercle-rouge-re-release/critic-reviews',
#     'https://www.metacritic.com/movie/the-raid-redemption/critic-reviews',
#     'https://www.metacritic.com/movie/pain-gain/critic-reviews',
#     'https://www.metacritic.com/movie/taken-3/critic-reviews',
#     'https://www.metacritic.com/movie/sin-city-a-dame-to-kill-for/critic-reviews',
#     'https://www.metacritic.com/movie/stephen-kings-a-good-marriage/critic-reviews',
#     'https://www.metacritic.com/movie/redemption/critic-reviews',
#     'https://www.metacritic.com/movie/the-family/critic-reviews',
#     'https://www.metacritic.com/movie/captain-phillips/critic-reviews',
#     'https://www.metacritic.com/movie/sweetwater/critic-reviews',
#     'https://www.metacritic.com/movie/un-flic-re-release/critic-reviews',
#     'https://www.metacritic.com/movie/wake-in-fright-1971/critic-reviews',
#     'https://www.metacritic.com/movie/skyfall/critic-reviews',
#     'https://www.metacritic.com/movie/killing-them-softly/critic-reviews',
#     'https://www.metacritic.com/movie/the-snowtown-murders/critic-reviews',
#     'https://www.metacritic.com/movie/the-hunters-prayer/critic-reviews',
#     'https://www.metacritic.com/movie/the-confessions/critic-reviews',
#     'https://www.metacritic.com/movie/the-assignment/critic-reviews',
#     'https://www.metacritic.com/movie/the-fate-of-the-furious/critic-reviews',
#     'https://www.metacritic.com/movie/the-take-2016/critic-reviews',
#     'https://www.metacritic.com/movie/war-dogs/critic-reviews',
#     'https://www.metacritic.com/movie/13-hours-the-secret-soldiers-of-benghazi/critic-reviews',
#     'https://www.metacritic.com/movie/the-connection/critic-reviews',
#     'https://www.metacritic.com/movie/lawrence-of-arabia-re-release/critic-reviews',
#     'https://www.metacritic.com/movie/john-wick-chapter-3---parabellum/critic-reviews',
#     'https://www.metacritic.com/movie/police-story-2-1988/critic-reviews',
#     'https://www.metacritic.com/movie/sicario-day-of-the-soldado/critic-reviews',
#     'https://www.metacritic.com/movie/tyler-perrys-acrimony/critic-reviews',
#     'https://www.metacritic.com/movie/6-below-miracle-on-the-mountain/critic-reviews',
#     'https://www.metacritic.com/movie/police-story-1985/critic-reviews',
#     'https://www.metacritic.com/movie/le-petit-soldat-re-release/critic-reviews',
#     'https://www.metacritic.com/movie/seven-samurai-re-release/critic-reviews',
#     'https://www.metacritic.com/movie/white-sun-seto-surya/critic-reviews',
#     'https://www.metacritic.com/movie/dragon-inn-1967/critic-reviews',
#     'https://www.metacritic.com/movie/cz12/critic-reviews',
#     'https://www.metacritic.com/movie/the-legend-of-hercules/critic-reviews',
#     'https://www.metacritic.com/movie/crystal-fairy-the-magical-cactus/critic-reviews',
#     'https://www.metacritic.com/movie/miami-connection-1987/critic-reviews',
#     'https://www.metacritic.com/movie/true-memoirs-of-an-international-assassin/critic-reviews',
#     'https://www.metacritic.com/movie/masterminds/critic-reviews',
#     'https://www.metacritic.com/movie/the-brothers-grimsby/critic-reviews',
#     'https://www.metacritic.com/movie/yarn/critic-reviews',
#     'https://www.metacritic.com/movie/the-painting-le-tableau/critic-reviews',
#     'https://www.metacritic.com/movie/fruitvale-station/critic-reviews',
#     'https://www.metacritic.com/movie/next-year-jerusalem/critic-reviews',
#     'https://www.metacritic.com/movie/philip-roth-unmasked/critic-reviews',
#     'https://www.metacritic.com/movie/cezanne-et-moi/critic-reviews',
#     'https://www.metacritic.com/movie/jt-leroy/critic-reviews',
#     'https://www.metacritic.com/movie/the-serengeti-rules/critic-reviews',
#     'https://www.metacritic.com/movie/blackkklansman/critic-reviews',
#     'https://www.metacritic.com/movie/the-pirates-of-somalia/critic-reviews',
#     'https://www.metacritic.com/movie/monty-pythons-life-of-brian/critic-reviews',
#     'https://www.metacritic.com/movie/the-producers-re-release/critic-reviews',
#     'https://www.metacritic.com/movie/lisa-picard-is-famous/critic-reviews',
#     'https://www.metacritic.com/movie/la-dolce-vita-re-release/critic-reviews',
#     'https://www.metacritic.com/movie/i-vitelloni-re-release/critic-reviews',
#     'https://www.metacritic.com/movie/mafioso-re-release/critic-reviews',
#     'https://www.metacritic.com/movie/the-campaign-2012/critic-reviews',
#     'https://www.metacritic.com/movie/sexual-chronicles-of-a-french-family/critic-reviews',
#     'https://www.metacritic.com/movie/thats-my-boy/critic-reviews',
#     'https://www.metacritic.com/movie/life-happens/critic-reviews',
#     'https://www.metacritic.com/movie/okis-movie/critic-reviews',
#     'https://www.metacritic.com/movie/bucky-larson-born-to-be-a-star/critic-reviews',
#     'https://www.metacritic.com/movie/the-woman-on-the-6th-floor/critic-reviews',
#     'https://www.metacritic.com/movie/birdman-or-the-unexpected-virtue-of-ignorance/critic-reviews',
#     'https://www.metacritic.com/movie/tyler-perrys-the-single-moms-club/critic-reviews',
#     'https://www.metacritic.com/movie/the-incredible-burt-wonderstone/critic-reviews',
#     'https://www.metacritic.com/movie/the-guilt-trip/critic-reviews',
#     'https://www.metacritic.com/movie/identity-thief/critic-reviews',
#     'https://www.metacritic.com/movie/everybody-wants-some%21%21/critic-reviews',
#     'https://www.metacritic.com/movie/barbershop-the-next-cut/critic-reviews',
#     'https://www.metacritic.com/movie/neighbors-2-sorority-rising/critic-reviews',
#     'https://www.metacritic.com/movie/the-meyerowitz-stories-new-and-selected/critic-reviews',
#     'https://www.metacritic.com/movie/the-old-man-the-gun/critic-reviews',
#     'https://www.metacritic.com/movie/a-bread-factory-part-two-walk-with-me-a-while/critic-reviews',
#     'https://www.metacritic.com/movie/a-bread-factory-part-one-for-the-sake-of-gold/critic-reviews',
#     'https://www.metacritic.com/movie/father-figures/critic-reviews',
#     'https://www.metacritic.com/movie/bennys-video-1992/critic-reviews',
#     'https://www.metacritic.com/movie/band-of-outsiders-re-release/critic-reviews',
#     'https://www.metacritic.com/movie/fever-heat-re-release/critic-reviews',
#     'https://www.metacritic.com/movie/investigation-of-a-citizen-above-suspicion-re-release/critic-reviews',
#     'https://www.metacritic.com/movie/balthazar-re-release/critic-reviews',
#     'https://www.metacritic.com/movie/piccadilly-re-release/critic-reviews',
#     'https://www.metacritic.com/movie/the-drop/critic-reviews',
#     'https://www.metacritic.com/movie/roman-j-israel-esq/critic-reviews',
#     'https://www.metacritic.com/movie/the-sky-turns/critic-reviews',
#     'https://www.metacritic.com/movie/shoah-re-release/critic-reviews',
#     'https://www.metacritic.com/movie/primo-levis-journey/critic-reviews',
#     'https://www.metacritic.com/movie/vocateur-the-morton-downey-jr-movie/critic-reviews',
#     'https://www.metacritic.com/movie/winter-nomads/critic-reviews',
#     'https://www.metacritic.com/movie/mumia-long-distance-revolutionary/critic-reviews',
#     'https://www.metacritic.com/movie/108-cuchillo-de-palo/critic-reviews',
#     'https://www.metacritic.com/movie/portrait-of-jason-re-release/critic-reviews',
#     'https://www.metacritic.com/movie/bestiary/critic-reviews',
#     'https://www.metacritic.com/movie/comic-con-episode-iv-a-fans-hope/critic-reviews',
#     'https://www.metacritic.com/movie/the-inheritors/critic-reviews',
#     'https://www.metacritic.com/movie/reindeerspotting-escape-from-santaland/critic-reviews',
#     'https://www.metacritic.com/movie/sunday-ball/critic-reviews',
#     'https://www.metacritic.com/movie/winter-on-fire-ukraines-fight-for-freedom/critic-reviews',
#     'https://www.metacritic.com/movie/what-our-fathers-did-a-nazi-legacy/critic-reviews',
#     'https://www.metacritic.com/movie/horse-money/critic-reviews',
#     'https://www.metacritic.com/movie/the-great-museum/critic-reviews',
#     'https://www.metacritic.com/movie/the-new-rijksmuseum/critic-reviews',
#     'https://www.metacritic.com/movie/the-great-buster-a-celebration/critic-reviews',
#     'https://www.metacritic.com/movie/the-king-2018/critic-reviews',
#     'https://www.metacritic.com/movie/an-inconvenient-sequel-truth-to-power/critic-reviews',
#     'https://www.metacritic.com/movie/school-life/critic-reviews',
#     'https://www.metacritic.com/movie/ex-libris-the-new-york-public-library/critic-reviews',
#     'https://www.metacritic.com/movie/jim-andy-the-great-beyond-featuring-a-very-special-contractually-obligated-mention-of-tony-clifton/critic-reviews',
#     'https://www.metacritic.com/movie/the-human-surge/critic-reviews',
#     'https://www.metacritic.com/movie/the-conformist-re-release/critic-reviews',
#     'https://www.metacritic.com/movie/august-winds-ventos-de-agosto/critic-reviews',
#     'https://www.metacritic.com/movie/our-time-nuestro-tiempo/critic-reviews',
#     'https://www.metacritic.com/movie/run-2019/critic-reviews',
#     'https://www.metacritic.com/movie/the-seventh-continent-1989/critic-reviews',
#     'https://www.metacritic.com/movie/first-love-2019/critic-reviews',
#     'https://www.metacritic.com/movie/montparnasse-bienvenue-jeune-femme/critic-reviews',
#     'https://www.metacritic.com/movie/tigerland-2019/critic-reviews',
#     'https://www.metacritic.com/movie/the-price-of-free/critic-reviews',
#     'https://www.metacritic.com/movie/la-promesse-the-promise/critic-reviews',
#     'https://www.metacritic.com/movie/dekalog-1988/critic-reviews',
#     'https://www.metacritic.com/movie/sweet-smell-of-success-re-release/critic-reviews',
#     'https://www.metacritic.com/movie/umberto-d-re-release/critic-reviews',
#     'https://www.metacritic.com/movie/anatomy-of-hell/critic-reviews',
#     'https://www.metacritic.com/movie/the-inheritance/critic-reviews',
#     'https://www.metacritic.com/movie/service-serbis/critic-reviews',
#     'https://www.metacritic.com/movie/little-girl-la-pivellina/critic-reviews',
#     'https://www.metacritic.com/movie/sidewalls/critic-reviews',
#     'https://www.metacritic.com/movie/cirkus-columbia/critic-reviews',
#     'https://www.metacritic.com/movie/jess-and-moss/critic-reviews',
#     'https://www.metacritic.com/movie/elza-le-bonheur-delza/critic-reviews',
#     'https://www.metacritic.com/movie/redemption-road/critic-reviews',
#     'https://www.metacritic.com/movie/octubre/critic-reviews',
#     'https://www.metacritic.com/movie/the-four-times-le-quattro-volte/critic-reviews',
#     'https://www.metacritic.com/movie/queen-to-play/critic-reviews',
#     'https://www.metacritic.com/movie/dhobi-ghat-mumbai-diaries/critic-reviews',
#     'https://www.metacritic.com/movie/the-sessions/critic-reviews',
#     'https://www.metacritic.com/movie/the-shine-of-day/critic-reviews',
#     'https://www.metacritic.com/movie/voyage-to-italy-re-release/critic-reviews',
#     'https://www.metacritic.com/movie/memories-look-at-me/critic-reviews',
#     'https://www.metacritic.com/movie/eden-2013/critic-reviews',
#     'https://www.metacritic.com/movie/tyler-perrys-temptation/critic-reviews',
#     'https://www.metacritic.com/movie/a-bottle-in-the-gaza-sea-une-bouteille-s-la-mer/critic-reviews',
#     'https://www.metacritic.com/movie/the-pirogue/critic-reviews',
#     'https://www.metacritic.com/movie/tristana-re-release/critic-reviews',
#     'https://www.metacritic.com/movie/wont-back-down/critic-reviews',
#     'https://www.metacritic.com/movie/sister/critic-reviews',
#     'https://www.metacritic.com/movie/quill-the-life-of-a-guide-dog/critic-reviews',
#     'https://www.metacritic.com/movie/we-are-the-best%21/critic-reviews',
#     'https://www.metacritic.com/movie/nymphomaniac-volume-i/critic-reviews',
#     'https://www.metacritic.com/movie/olvidados-forgotten/critic-reviews',
#     'https://www.metacritic.com/movie/hippocrates-diary-of-a-french-doctor/critic-reviews',
#     'https://www.metacritic.com/movie/my-name-is-hmmm/critic-reviews',
#     'https://www.metacritic.com/movie/land-and-shade/critic-reviews',
#     'https://www.metacritic.com/movie/mekong-hotel-2012/critic-reviews',
#     'https://www.metacritic.com/movie/the-benefactor/critic-reviews',
#     'https://www.metacritic.com/movie/out-1-noli-me-tangere-1971/critic-reviews',
#     'https://www.metacritic.com/movie/bpm-beats-per-minute/critic-reviews',
#     'https://www.metacritic.com/movie/lover-for-a-day/critic-reviews',
#     'https://www.metacritic.com/movie/whos-crazy-1966/critic-reviews',
#     'https://www.metacritic.com/movie/the-son-of-joseph/critic-reviews',
#     'https://www.metacritic.com/movie/the-last-suit/critic-reviews',
#     'https://www.metacritic.com/movie/the-mustang/critic-reviews',
#     'https://www.metacritic.com/movie/the-citizen-az-allampolgar/critic-reviews',
#     'https://www.metacritic.com/movie/the-swan/critic-reviews',
#     'https://www.metacritic.com/movie/mrs-hyde/critic-reviews',
#     'https://www.metacritic.com/movie/cold-water-1994/critic-reviews',
#     'https://www.metacritic.com/movie/personal-problems-1980/critic-reviews',
#     'https://www.metacritic.com/movie/sauvage-wild/critic-reviews']
