from daryouz_engine import scrape

# 1
# start, end, file_path = 50000, 94695, "daryouz_links/crawled_urls.txt"
# 2
# start, end, file_path = 94696, 110000, "daryouz_links/crawled_urls.txt"
# 3
# start, end, file_path = 200000, 240000, "daryouz_links/crawled_urls.txt"
# 4
# start, end, file_path = 320000, 360000, "daryouz_links/crawled_urls.txt"
# 5
# start, end, file_path = 440000, 460300, "daryouz_links/crawled_urls.txt"
# 6
start, end, file_path = 460301, 480000, "daryouz_links/crawled_urls.txt"

# call
scrape(start, end, file_path)
