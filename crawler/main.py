from crawler.crawlers import PariMatchCrawler, PariMatchScrapperCrawler

crawler = PariMatchScrapperCrawler()

for event in crawler.get_top_football_events():
    print(event)
