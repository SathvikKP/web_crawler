import sys
import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from satkp_crawler.spiders.satkp_spider import SatkpSpider

def run_spider():

    if os.path.exists('crawled_data.json'):
        os.remove('crawled_data.json')

    if os.path.exists('crawl_statistics.png'):
        os.rename('crawl_statistics.png', 'crawl_statistics_old.png')

    # Redirect terminal output to a file
    original_stdout = sys.stdout
    original_stderr = sys.stderr
    with open('crawl_output.log', 'w') as f:
        sys.stdout = f
        sys.stderr = f
        
        process = CrawlerProcess(get_project_settings())
        process.crawl(SatkpSpider)
        process.start()
        
        # Restore original stdout (not needed really)
        sys.stdout = original_stdout
        sys.stderr = original_stderr

if __name__ == '__main__':
    run_spider()