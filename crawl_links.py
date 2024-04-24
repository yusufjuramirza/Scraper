import requests
from bs4 import BeautifulSoup
from collections import deque
from urllib.parse import urlparse


def get_all_hyperlinks(url_link):
    hyperlinks = []
    try:
        response = requests.get(url_link)
        # Ensure the response content is HTML before proceeding
        if "text/html" in response.headers["Content-Type"]:
            soup = BeautifulSoup(response.text, 'html.parser')
            for link in soup.find_all('a', href=True):
                href = link['href']
                if href.startswith('/'):
                    href = urlparse(url_link).scheme + "://" + urlparse(url_link).netloc + href
                elif not urlparse(href).scheme:
                    href = urlparse(url_link).scheme + "://" + urlparse(url_link).netloc + '/' + href
                hyperlinks.append(href)
    except Exception as e:
        print(f"Error getting hyperlinks from {url_link}: {e}")
    return hyperlinks


def should_visit(url):
    # Check if the URL contains language-specific paths we want to exclude
    excluded_paths = ['/ru', '/en', '/#', '/k']
    for path in excluded_paths:
        if path in url:
            return False
    return True


def crawl(start_url, local_domain):
    visited = set()  # Track visited URLs to avoid loops
    to_visit = [start_url]  # Queue of URLs to be visited

    index = 1
    while to_visit:
        current_url = to_visit.pop(0)  # Get and remove the first URL from the queue
        if current_url not in visited:
            print(f"Crawling-{index}: {current_url}")
            index += 1
            visited.add(current_url)

            # Attempt to get all hyperlinks from the current URL and queue them
            for link in get_all_hyperlinks(current_url):
                if link not in visited:
                    if urlparse(link).netloc == local_domain:
                        if should_visit(link):
                            to_visit.append(link)

    return visited  # Optionally return the set of visited URLs


domain = "daryo.uz"
full_url = "https://daryo.uz"

crawled_urls = crawl(full_url, domain)
with open("daryouz_links/crawled_urls.txt", "a") as file:
    for c_url in crawled_urls:
        c_url = c_url.strip()
        file.write(f"{c_url}\n")
