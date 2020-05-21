from crawler.crawlers import PariMatchCrawler

crawler = PariMatchCrawler()

for event in crawler.get_top_football_events():
    print(event)
