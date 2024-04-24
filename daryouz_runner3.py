from daryouz_engine import scrape

# 1
# start, end, file_path = 100000, 144273, "daryouz_links/crawled_urls.txt"
# 2
# start, end, file_path = 144274, 160000, "daryouz_links/crawled_urls.txt"
# 3
# start, end, file_path = 240000, 280000, "daryouz_links/crawled_urls.txt"
# 4
# start, end, file_path = 360000, 400000, "daryouz_links/crawled_urls.txt"
# 5
# start, end, file_path = 480000, 500525, "daryouz_links/crawled_urls.txt"
# 6
start, end, file_path = 500526, 520000, "daryouz_links/crawled_urls.txt"

# call
scrape(start, end, file_path)
