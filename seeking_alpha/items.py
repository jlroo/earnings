# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import re
import scrapy
from datetime import datetime
from scrapy.loader.processors import MapCompose, TakeFirst

src_url = "https://seekingalpha.com"


def to_utc(value):
    date = [datetime.utcfromtimestamp(int(i)) if i is not None else "" for i in [value]][0]
    return date


def source_url(value):
    global src_url
    if value:
        return src_url + value


def article_year(value):
    year_match = re.match(r".*[\s](\d{4})\s", value)
    year = [int(i.group(1).strip()) if i is not None else "" for i in [year_match]][0]
    return year


def article_id(value):
    arc_id = [int(i) if i is not None else "" for i in [value]][0]
    return arc_id


def article_quarter(value):
    quarter_match = re.match(r".*[\s](Q\d)\s", value)
    quarter = [i.group(1) if i is not None else "" for i in [quarter_match]][0]
    return quarter


def article_ceo(value):
    #match = r'(?:\)\s|\)\sCEO|\sCEO\s|\sCEO,\s)(.*?\s)(?:on|On|present|Presents|Hosts|Q\d)'
    match = r'(?:-ceo-)(.*?)(-[A-Za-z]\d|-on)'
    ceo_match = re.search(match , value)
    if ceo_match is not None:
        ceo = ceo_match.group(1)
    elif "presents" in value:
        ceo = "presentation"
    elif "management" in value:
        ceo = "management"
    else:
        ceo = ""
    return ceo


class SeekingAlphaItem(scrapy.Item):
    filing = scrapy.Field(output_processor=TakeFirst())
    press = scrapy.Field(output_processor=TakeFirst())
    audio = scrapy.Field(output_processor=TakeFirst())
    date_posted = scrapy.Field(input_processor=MapCompose(to_utc),
                               output_processor=TakeFirst())
    date_published = scrapy.Field(output_processor=TakeFirst())
    date_modified = scrapy.Field(output_processor=TakeFirst())
    data_id = scrapy.Field(input_processor=MapCompose(article_id),
                           output_processor=TakeFirst())
    pag_index = scrapy.Field(output_processor=TakeFirst())
    symbol = scrapy.Field(output_processor=TakeFirst())
    company = scrapy.Field(output_processor=TakeFirst())
    description = scrapy.Field(output_processor=TakeFirst())
    response_url = scrapy.Field(output_processor=TakeFirst())
    article_url = scrapy.Field(input_processor=MapCompose(source_url),
                               output_processor=TakeFirst())
    year = scrapy.Field(input_processor=MapCompose(article_year),
                        output_processor=TakeFirst())
    quarter = scrapy.Field(input_processor=MapCompose(article_quarter),
                           output_processor=TakeFirst())
    company_ceo = scrapy.Field(input_processor=MapCompose(article_ceo),
                               output_processor=TakeFirst())


