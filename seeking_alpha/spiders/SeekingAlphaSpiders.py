import scrapy
from scrapy.loader import ItemLoader
from twisted.internet.error import TimeoutError
from twisted.internet.error import DNSLookupError
from seeking_alpha.items import SeekingAlphaItem
from scrapy.spidermiddlewares.httperror import HttpError


class EarningsSpider(scrapy.Spider):

    name = "earnings"
    rotate_user_agent = True
    source_url = "https://seekingalpha.com"

    def start_requests(self):
        num_pages = getattr(self, 'num_pages', None)
        start = getattr(self, 'start', None)
        end = getattr(self, 'end', None)
        pag = getattr(self, 'pag', None)
        articles_url = "/earnings"
        section_url = "/earnings-call-transcripts"
        site_url = self.source_url + articles_url + section_url + "/"
        if num_pages:
            urls = [site_url + str(i) for i in range(1, int(num_pages)+1)]
        elif start and end:
            urls = [site_url + str(i) for i in range(int(start), int(end)+1)]
        elif pag:
            urls = [self.source_url + articles_url + section_url + "/" + pag]
        else:
            return print("Need an start request url")
        for url in urls:
            yield scrapy.Request(url=url,
                                 callback=self.parse,
                                 errback=self.error_response,
                                 dont_filter=True)

    def parse(self, response):
        for article in response.xpath("//*[@id='analysis-list-container']/ul/li"):
            item = ItemLoader(item=SeekingAlphaItem(), selector=article)
            item.add_css('data_id', '.article::attr(data-id)')
            item.add_value('pag_index', int(str(response.url).split("/")[-1]))
            item.add_value('response_url', response.url)
            item.add_css('symbol', 'span.article-symbols > a::text')
            item.add_css('company', 'span.article-symbols > a::attr(title)')
            item.add_css('description', 'h3.list-group-item-heading > a::text')
            item.add_css('date_posted', '.article::attr(data-published)')
            item.add_css('article_url', 'h3.list-group-item-heading > a::attr(href)')
            item.add_css('year', 'h3.list-group-item-heading > a::text')
            item.add_css('quarter', 'h3.list-group-item-heading > a::text')
            item.add_css('company_ceo', 'h3.list-group-item-heading > a::attr(href)')
            yield item.load_item()

    # TODO
    def parse_article(self, response):
        article_url = response.css('h3.list-group-item-heading > a::attr(href)')
        article_url = self.source_url + article_url.extract()[0]
        request = scrapy.Request(article_url ,
                                 callback=self.parse_article ,
                                 meta={'item': item})

        item = response.meta['item']
        date_modified = response.xpath('//*[@id="content-rail"]/article/header/time/@datetime').get()
        date_published = response.xpath('//*[@id="a-hd"]/div/time/@content').get()
        audio = response.xpath('//*[@id="content-rail"]/article/section/audio/source/@src').get()
        item.add_value('date_modified', date_modified)
        item.add_value('date_published', date_published)
        item.add_value('audio', audio)
        yield item.load_item()

    def error_response(self, failure):
        if failure.check(HttpError):
            # you can get the response
            response = failure.value.response
            with open("errors/http_error.txt","a") as f:
                f.write(response.url + "\n")
            yield self.logger.error('HttpError on %s', response.url)
        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            with open("errors/dnslookup_error.txt","a") as f:
                f.write(failure.url + "\n")
            yield self.logger.error('DNSLookupError on %s', request.url)
        elif failure.check(TimeoutError):
            request = failure.request
            with open("errors/timeout_error.txt","a") as f:
                f.write(failure.url + "\n")
            yield self.logger.error('TimeoutError on %s', request.url)


# scrapy crawl earnings -a start=5 -a end=10

    """
    def parse(self, response):
        for article in response.xpath("//*[@id='analysis-list-container']/ul/li"):
            item = ItemLoader(item=SeekingAlphaItem(), selector=article)
            item.add_css('data_id', 'ul.list-group > li::attr(data-id)')
            item.add_value('pag_index', int(str(response.url).split("/")[-1]))
            item.add_value('response_url', response.url)
            item.add_css('symbol', 'span.article-symbols > a::text')
            item.add_css('company', 'span.article-symbols > a::attr(title)')
            item.add_css('description', 'h3.list-group-item-heading > a::text')
            item.add_css('posted_date', 'ul.list-group > li::attr(data-published)')
            item.add_css('article_url', 'h3.list-group-item-heading > a::attr(href)')
            item.add_css('year', 'h3.list-group-item-heading > a::text')
            item.add_css('quarter', 'h3.list-group-item-heading > a::text')
            item.add_css('company_ceo', 'h3.list-group-item-heading > a::text')
            yield item.load_item()
    
    #transcript = response.css('h3.list-group-item-heading > a::attr(href)').extract()
    #filing = transcript.css('li#filing > a::attr(href)').get()
    #press = transcript.css('li#press_release > a::attr(href)').get()
    #audio = transcript.css('section.audio.audio > source::attr(src)').get()

    def get_call(self, response):

        url_split = response.url.split('-')

        if 'earnings' and 'call' and 'transcript' in url_split:

            if 'q1' in url_split:
                index_q1 = url_split.index('q1')
                if 'ceo' in url_split:
                    index_ceo = url_split.index('ceo')
                    filename = url_split[index_ceo - 1] + '-' + '-'.join(url_split[index_q1 : index_q1 + 2]) + '.html'
                else:
                    filename = '-'.join(url_split[index_q1 - 1 : index_q1 + 2]) + '.html'

            if 'q2' in url_split:
                index_q2 = url_split.index('q2')
                if 'ceo' in url_split:
                    index_ceo = url_split.index('ceo')
                    filename = url_split[index_ceo - 1] + '-' + '-'.join(url_split[index_q2 : index_q2 + 2]) + '.html'
                else:
                    filename = '-'.join(url_split[index_q2 - 1 : index_q2 + 2]) + '.html'

            if 'q3' in url_split:
                index_q3 = url_split.index('q3')
                if 'ceo' in url_split:
                    index_ceo = url_split.index('ceo')
                    filename = url_split[index_ceo - 1] + '-' + '-'.join(url_split[index_q3 : index_q3 + 2]) + '.html'
                else:
                    filename = '-'.join(url_split[index_q3 - 1 : index_q3 + 2]) + '.html'

            if 'q4' in url_split:
                index_q4 = url_split.index('q4')
                if 'ceo' in url_split:
                    index_ceo = url_split.index('ceo')
                    filename = url_split[index_ceo - 1] + '-' + '-'.join(url_split[index_q4 : index_q4 + 2]) + '.html'
                else:
                    filename = '-'.join(url_split[index_q4 - 1 : index_q4 + 2]) + '.html'

            #meta = {'name': filename}
            dirname = 'Data/'
            filename = os.path.join(dirname, filename)
            with open(filename, 'wb') as f:
                f.write(response.body)

"""
