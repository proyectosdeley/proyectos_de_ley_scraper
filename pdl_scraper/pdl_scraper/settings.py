# -*- coding: utf-8 -*-

# Scrapy settings for pdl_scraper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
import json
import os
from unipath import Path
import sys


BASE_DIR = Path(__file__).absolute().ancestor(3)
SECRETS_FILE = os.path.join(BASE_DIR, 'config.json')

with open(SECRETS_FILE) as f:
    secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {0} environment variable".format(setting)
        print(error_msg)
        sys.exit(1)

DATABASE = {
    'drivername': get_secret('drivername'),
    'username': get_secret('username'),
    'password': get_secret('password'),
    'host': get_secret('host'),
    'port': get_secret('port'),
    'database': get_secret('database'),
}

BOT_NAME = 'pdl_scraper'

SPIDER_MODULES = ['pdl_scraper.spiders']
NEWSPIDER_MODULE = 'pdl_scraper.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'pdl_scraper (+http://www.yourdomain.com)'
# be nice
CONCURRENT_REQUESTS = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 1
DOWNLOAD_DELAY = 5


CRAWLERA_USER = get_secret("crawlera_user")
CRAWLERA_PASS = get_secret("crawlera_pass")
DOWNLOADER_MIDDLEWARES = {
    'scrapylib.crawlera.CrawleraMiddleware': 600,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36",
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': "http://" + CRAWLERA_USER + ":" + CRAWLERA_PASS + "@proxy.crawlera.com:8010/",
}

CRAWLERA_ENABLED = True


LOG_LEVEL = 'DEBUG'
LOG_ENABLED = True