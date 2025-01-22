# README

## Overview
This project is a Scrapy-based web crawler that collects URLs from the Georgia Tech College of Computing domain (cc.gatech.edu) and saves data to JSON. A separate Python analysis script processes the JSON data to compute statistics and generate charts.  

## Repository Structure
```
├── analysis.py # Analyzes crawled_data.json and generates statistics/charts 
├── crawl_output.log # Captures crawler stdout and stderr
├── crawl_stats.json # JSON file with summarized crawl stats 
├── crawled_data.json # JSON file with main crawler output (URLs and keywords) 
├── main.py # Entry point to run the crawler ├── satkp_crawler/ # Scrapy project folder 
│ ├── spiders/ 
│ │ ├── __init__.py 
│ │ └── satkp_spider.py # Main spider class with parsing logic 
│ ├── __init__.py 
│ ├── items.py # Defines Scrapy item structure (unused) 
│ ├── middlewares.py # Defines Scrapy middlewares (unused) 
│ ├── pipelines.py # Defines Scrapy pipelines (unused) 
│ ├── settings.py # Project-wide Scrapy settings 
├── scrapy.cfg # Settings for deploying the Scrapy project 
└── ...
```
## How It Works
1. **Spiders**  
   - The `SatkpSpider` in `satkp_crawler/spiders/satkp_spider.py` starts at `https://www.cc.gatech.edu/` and follows internal links.  
   - Pages are parsed, keywords are extracted, stats are updated, and items (URL + keywords) are yielded back to Scrapy.
2. **Crawl Process**  
   - Run by executing `main.py`.  
   - Scrapy logs and output are redirected to `crawl_output.log`.  
   - Crawler results are saved to `crawled_data.json`.
   - Crawl plots are saved in `crawl_statistics.png`.
3. **Analysis**  
   - `analysis.py` reads `crawled_data.json`, counts various patterns in URLs, and generates a pie chart to show distribution.  
   - Results are printed to the console, and a pie chart is saved as `subdomains_pie_chart.png`.

## Usage
1. Install dependencies (Scrapy, matplotlib)  
```bash
pip install scrapy matplotlib
```

2. Run the crawler
```bash
python main.py
```
This overwrites crawled_data.json and produces crawl_output.log.

3. Analyze results
```bash
python analysis.py
```
Prints summary statistics and generates subdomains_pie_chart.png.

## Customization

- Spider Settings: Adjust in satkp_spider.py (e.g., start_urls, allowed_domains) or in settings.py.
- Timeouts and Limits: Controlled by DOWNLOAD_TIMEOUT, CLOSESPIDER_PAGECOUNT, etc. in settings or spider class.
- Output Formats: Current setup writes to JSON. Modify FEED_FORMAT or FEED_URI in settings.py to change the format.

## License
This project is licensed under the MIT License.
