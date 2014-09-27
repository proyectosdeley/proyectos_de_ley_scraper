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