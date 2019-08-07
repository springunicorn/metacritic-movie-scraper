# -*- coding: utf-8 -*-

# Scrapy settings for metacriticbot project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
import os
from datetime import datetime

BOT_NAME = 'metacriticbot'

SPIDER_MODULES = ['metacriticbot.spiders']
NEWSPIDER_MODULE = 'metacriticbot.spiders'

COOKIES_ENABLED = True
DOWNLOAD_DELAY = 2
DOWNLOAD_TIMEOUT = 360
#CONCURRENT_REQUESTS = 1

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'metacriticbot (+http://www.yourdomain.com)'

# Spoofing to resolve 301 redirections problem (Not really...)
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'

#Pipelines. Some data cleaning. Export to xls.
ITEM_PIPELINES = {
    'metacriticbot.pipelines.MetacriticbotPipeline': 100,
    'metacriticbot.pipelines.XlsExportPipeline': 200,
}

# Feed Exports
TIMESTR = datetime.now().strftime("%Y%m%d-%H%M%S")
cur_dir = os.path.dirname(os.path.realpath(__file__))
components = cur_dir.split(os.sep)
RELPATH = str.join(os.sep, components[:components.index("metacritic-analysis")+1])

FEED_URI = os.path.join(RELPATH, 'data', '%(name)s-' + TIMESTR + '.csv')
       #os.path.join(relpath, 'data', '%(name)s-%(time)s.json')
       # ]
FEED_FORMAT = 'csv'

#Logging
logname = "log-" + TIMESTR + ".log"
LOG_FILE = os.path.join(RELPATH, 'data', logname)
