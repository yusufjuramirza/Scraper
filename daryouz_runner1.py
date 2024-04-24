from daryouz_engine import scrape

# 1
# start, end, file_path = 0, 44495, "daryouz_links/crawled_urls.txt"
# 2
# start, end, file_path = 44496, 60000, "daryouz_links/crawled_urls.txt"
# 3
# start, end, file_path = 160000, 200000, "daryouz_links/crawled_urls.txt"
# 4
# start, end, file_path = 280000, 320000, "daryouz_links/crawled_urls.txt"
# 5
# start, end, file_path = 400000, 420303, "daryouz_links/crawled_urls.txt"
# 5
start, end, file_path = 420304, 440000, "daryouz_links/crawled_urls.txt"

# call
scrape(start, end, file_path)

