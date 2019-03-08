# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

# Scrapy settings for seeking_alpha project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'seeking_alpha'

SPIDER_MODULES = ['seeking_alpha.spiders']
NEWSPIDER_MODULE = 'seeking_alpha.spiders'
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'seeking_alpha (+http://www.yourdomain.com)'

FEED_FORMAT = 'jsonlines'
FEED_URI = "data/earnings.json"


def get_proxies():
    proxy_url = "https://www.us-proxy.org/"
    response = requests.get(proxy_url, timeout=5)
    html = BeautifulSoup(response.content, 'html.parser')
    table = html.find('table', {'class': 'table'})
    table = table.findAll("tr")
    addr = [i.findAll("td")[0].text + ":" + i.findAll("td")[1].text for i in table[1:-2]]
    with open('proxies/proxy_file.txt', 'a') as outfile:
        outfile.writelines("\n" + "\n".join(addr))
    return addr

ROTATED_PROXY_ENABLED = True
#ROTATING_PROXY_LIST = get_proxies()
ROTATING_PROXY_LIST_PATH = 'proxies/proxy_file.txt'
USER_AGENT_CHOICES = [
    # New user agents from http://whatsmyuseragent.com/commonuseragents
    'Mozilla/5.0 ;Windows NT 6.3; WOW64; Trident/7.0; rv:11.0; like Gecko',
    'Mozilla/5.0 ;iPhone; CPU iPhone OS 7_1_2 like Mac OS X; AppleWebKit/537.51.2 ;KHTML, like Gecko; Version/7.0 Mobile/11D257 Safari/9537.53',
    'Mozilla/5.0 ;Windows NT 6.1; rv:35.0; Gecko/20100101 Firefox/35.0',
    'Mozilla/5.0 ;iPhone; CPU iPhone OS 8_0_2 like Mac OS X; AppleWebKit/600.1.4 ;KHTML, like Gecko; Version/8.0 Mobile/12A405 Safari/600.1.4' ,
    'Mozilla/5.0 ;iPad; CPU OS 8_1_2 like Mac OS X; AppleWebKit/600.1.4 ;KHTML, like Gecko; Version/8.0 Mobile/12B440 Safari/600.1.4' ,
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:23.0) Gecko/20100101 Firefox/23.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    'Mozilla/5.0 ;Windows NT 6.1; WOW64; Trident/7.0; rv:11.0; like Gecko',
    'Mozilla/5.0 ;iPhone; CPU iPhone OS 8_1_2 like Mac OS X; AppleWebKit/600.1.4 ;KHTML, like Gecko; Version/8.0 Mobile/12B440 Safari/600.1.4',
    'Mozilla/5.0 ;Windows NT 6.1; WOW64; AppleWebKit/537.36 ;KHTML, like Gecko; Chrome/36.0.1985.143 Safari/537.36',
    'Mozilla/5.0 ;Windows NT 6.3; WOW64; AppleWebKit/537.36 ;KHTML, like Gecko; Chrome/39.0.2171.95 Safari/537.36',
    'Mozilla/5.0 ;Windows NT 6.1; rv:34.0; Gecko/20100101 Firefox/34.0',
    'Mozilla/5.0 ;Windows NT 6.1; WOW64; rv:34.0; Gecko/20100101 Firefox/34.0',
    'Mozilla/5.0 ;compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/7.0;',
    'Mozilla/5.0 ;Windows NT 6.2; WOW64; rv:27.0; Gecko/20100101 Firefox/27.0',
    'Mozilla/5.0 ;compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html;',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0)',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.146 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.146 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64; rv:24.0) Gecko/20140205 Firefox/24.0 Iceweasel/24.3.0',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:28.0) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
    'Mozilla/5.0 ;Windows NT 6.1; WOW64; rv:35.0; Gecko/20100101 Firefox/35.0',
    'Mozilla/5.0 ;Windows NT 6.3; WOW64; rv:34.0; Gecko/20100101 Firefox/34.0',
    'Mozilla/5.0 ;Windows NT 6.1; AppleWebKit/537.36 ;KHTML, like Gecko; Chrome/39.0.2171.95 Safari/537.36',
    'Mozilla/5.0 ;Macintosh; Intel Mac OS X 10_10_1; AppleWebKit/600.2.5 ;KHTML, like Gecko; Version/8.0.2 Safari/600.2.5',
    'Mozilla/5.0 ;Windows NT 6.3; WOW64; rv:35.0; Gecko/20100101 Firefox/35.0',
    'Mozilla/5.0 ;Windows NT 6.1; WOW64; AppleWebKit/537.36 ;KHTML, like Gecko; Chrome/39.0.2171.99 Safari/537.36',
    'Mozilla/5.0 ;Macintosh; Intel Mac OS X 10_10_1; AppleWebKit/537.36 ;KHTML, like Gecko; Chrome/39.0.2171.95 Safari/537.36',
    'Mozilla/5.0 ;Windows NT 6.1; WOW64; AppleWebKit/537.36 ;KHTML, like Gecko; Chrome/40.0.2214.93 Safari/537.36',
    'Mozilla/5.0 ;Windows NT 5.1; rv:35.0; Gecko/20100101 Firefox/35.0'
]

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 6

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.5
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

#HTTPERROR_ALLOWED_CODES  =[404]

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

RETRY_ENABLED = True
RETRY_TIMES = 5  # initial response + 2 retries = 3 requests
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408]

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'seeking_alpha.middlewares.SeekingAlphaSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
# scrapy-rotating-proxies
# https://github.com/TeamHG-Memex/scrapy-rotating-proxies
DOWNLOADER_MIDDLEWARES = {
#    'seeking_alpha.middlewares.SeekingAlphaDownloaderMiddleware': 543,
    'seeking_alpha.middlewares.RotateUserAgentMiddleware': 610,
    'rotating_proxies.middlewares.RotatingProxyMiddleware': 610 ,
    'rotating_proxies.middlewares.BanDetectionMiddleware': 620 ,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'seeking_alpha.pipelines.SeekingAlphaPipeline': 300,
#}

FEED_EXPORTERS = {
 'jsonlines': 'scrapy.exporters.JsonLinesItemExporter',
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 10
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'