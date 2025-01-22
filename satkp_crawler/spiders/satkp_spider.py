import time
import scrapy
import matplotlib.pyplot as plt
import json
from urllib.parse import urljoin

# Reference: https://docs.scrapy.org/en/latest/intro/tutorial.html
# Reference: https://www.geeksforgeeks.org/implementing-web-scraping-python-scrapy/


# https://docs.scrapy.org/en/latest/topics/extensions.html#std-setting-CLOSESPIDER_TIMEOUT
# https://www.scrapingbee.com/blog/crawling-python/
# https://doc.scrapy.org/en/latest/topics/spiders.html#scrapy.Spider.start_requests
# https://docs.scrapy.org/en/latest/topics/spiders.html#scrapy.Spider.closed


class SatkpSpider(scrapy.Spider):

    name = 'satkp_spider'
    start_urls = ['https://www.cc.gatech.edu/']
    allowed_domains = ['cc.gatech.edu']

    # https://docs.scrapy.org/en/latest/topics/extensions.html#std-setting-CLOSESPIDER_TIMEOUT
    custom_settings = {
        'CLOSESPIDER_PAGECOUNT': 25001,  # Stop after crawling 1000 pages
        #'CLOSESPIDER_TIMEOUT': 20,  # Stop after 10 minutes
    }


    # https://doc.scrapy.org/en/latest/topics/spiders.html#scrapy.Spider.start_requests
    def start_requests(self):
        # https://stackoverflow.com/questions/22951418/how-to-collect-stats-from-within-scrapy-spider-callback
        self.crawler.stats.set_value('start_time', time.time())
        self.crawler.stats.set_value('pages_crawled', 0)
        self.crawler.stats.set_value('urls_found', 0)
        self.crawler.stats.set_value('keywords_extracted', 0)
        self.crawler.stats.set_value('crawl_timestamps', [])
        self.crawler.stats.set_value('pages_crawled_history', [])
        self.crawler.stats.set_value('urls_found_history', [])
        self.crawler.stats.set_value('keywords_extracted_history', [])
        self.crawler.stats.set_value('mailto_errors', 0)
        self.crawler.stats.set_value('non_text_errors', 0)
        self.crawler.stats.set_value('other_errors', 0)
        return super().start_requests()

    def parse(self, response):

        #self.crawler.stats.inc_value('pages_crawled') 

        try:

            # Extract keywords - I will simply use the title and meta description as keywords
            keywords = response.css('title::text').get() + ' ' + response.css('meta[name="description"]::attr(content)').get('')
            keywords_strip = keywords.strip()
        
            yield {
                'url': response.url,
                'keywords': keywords_strip,
            }

            keyword_count = len(keywords_strip.split()) if keywords_strip else 0
            self.crawler.stats.inc_value('keywords_extracted', count = keyword_count)
            self.crawler.stats.inc_value('pages_crawled') 

            # Follow links within the allowed domain (here: cc.gatech.edu or whatever I set above)
            for href in response.css('a::attr(href)').getall():
                # url = href
                # sometimes, href can be broken, for example https://www.cc.gatech.edu/page1 and the href is /page2, urljoin will change to https://www.cc.gatech.edu/page2
                url = urljoin(response.url, href)

                if self.allowed_domains[0] in url:
                    self.crawler.stats.inc_value('urls_found')
                    yield scrapy.Request(url, callback=self.parse)
        
        except Exception as e:
            print(f"Error occurred for URL: {response.url}")
            error_message = str(e)
            if "Missing scheme in request url: mailto" in error_message:
                self.crawler.stats.inc_value('mailto_errors')
            elif "Response content isn't text" in error_message:
                self.crawler.stats.inc_value('non_text_errors')
            else:
                self.crawler.stats.inc_value('other_errors')
                print("other_error : "+error_message)
            pass

        finally:
            # Very IMP: We need finally block otherwise the stats will not be updated properly in case of exceptions and out of domain urls (Also due to BFS nature, we need to update stats after each page is completely crawled)
            current_time = time.time() - self.crawler.stats.get_value('start_time').timestamp()
            self.crawler.stats.get_value('crawl_timestamps').append(current_time)
            self.crawler.stats.get_value('pages_crawled_history').append(self.crawler.stats.get_value('pages_crawled'))
            self.crawler.stats.get_value('keywords_extracted_history').append(self.crawler.stats.get_value('keywords_extracted'))
            self.crawler.stats.get_value('urls_found_history').append(self.crawler.stats.get_value('urls_found'))


    # https://docs.scrapy.org/en/latest/topics/spiders.html#scrapy.Spider.closed
    def closed(self, reason):
        end_time = time.time()
        crawl_duration = end_time - self.crawler.stats.get_value('start_time').timestamp()
        crawl_speed = self.crawler.stats.get_value('pages_crawled') / (crawl_duration / 60)  # pages per minute

        # Convert history lists to local variables for readability
        timestamps = self.crawler.stats.get_value('crawl_timestamps')
        pages_crawled_hist = self.crawler.stats.get_value('pages_crawled_history')
        urls_found_hist = self.crawler.stats.get_value('urls_found_history')
        keywords_hist = self.crawler.stats.get_value('keywords_extracted_history')

        # Calculate the ratio: (#pages_crawled) / (#urls_found)
        # If urls_found is zero at any index, ratio defaults to 0 to avoid division by zero
        ratio_list = []
        for pc, uf in zip(pages_crawled_hist, urls_found_hist):
            ratio_list.append(pc / uf if uf else 0)

        plt.figure(figsize=(12, 10))

        # 1) Pages Crawled Over Time
        plt.subplot(3, 2, 1)
        plt.plot(timestamps, pages_crawled_hist)
        plt.title('Pages Crawled Over Time')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Pages Crawled')

        # 2) URLs Found Over Time
        plt.subplot(3, 2, 2)
        plt.plot(timestamps, urls_found_hist)
        plt.title('URLs Found Over Time')
        plt.xlabel('Time (seconds)')
        plt.ylabel('URLs Found')

        # 3) Keywords Extracted Over Time
        plt.subplot(3, 2, 3)
        plt.plot(timestamps, keywords_hist)
        plt.title('Keywords Extracted Over Time')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Keywords Extracted')

        # 4) Crawl Speed (Pages per Minute) Over Time
        plt.subplot(3, 2, 4)
        crawl_speeds = [(p / (t / 60)) if t != 0 else 0 for p, t in zip(pages_crawled_hist, timestamps)]
        plt.plot(timestamps, crawl_speeds)
        plt.title('Crawl Speed Over Time')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Pages per Minute')

        # 5) Ratio of #URL Crawled / #URL Found Over Time
        plt.subplot(3, 2, 5)
        plt.plot(timestamps, ratio_list)
        plt.title('Ratio (Crawled / Found) Over Time')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Ratio')

        plt.tight_layout()
        plt.savefig('crawl_statistics.png')

        print(f"Crawl completed in {crawl_duration:.2f} seconds")
        print(f"Pages crawled: {self.crawler.stats.get_value('pages_crawled')}")
        print(f"URLs found: {self.crawler.stats.get_value('urls_found')}")
        print(f"Keywords extracted: {self.crawler.stats.get_value('keywords_extracted')}")
        print(f"Crawl speed: {crawl_speed:.2f} pages/minute")
        print(f"Mailto errors: {self.crawler.stats.get_value('mailto_errors')}")
        print(f"Non-text errors: {self.crawler.stats.get_value('non_text_errors')}")
        print(f"Other errors: {self.crawler.stats.get_value('other_errors')}")

        # Save stats to JSON file, excluding large history lists
        stats = dict(self.crawler.stats.get_stats())
        exclude_keys = ['start_time', 'crawl_timestamps', 'pages_crawled_history', 'urls_found_history', 'keywords_extracted_history']
        json_stats = {}
        for key, value in stats.items():
            if key in exclude_keys:
                if isinstance(value, list):
                    json_stats[key] = f"List with {len(value)} items"
                else:
                    json_stats[key] = f"Excluded: {type(value).__name__}"
            else:
                if not isinstance(value, list):
                    json_stats[key] = str(value)
                else:
                    json_stats[key] = value

        with open('crawl_stats.json', 'w') as f:
            json.dump(json_stats, f, indent=2)

        print("Graphs saved to crawl_statistics.png")
        print("Full statistics saved to crawl_stats.json")