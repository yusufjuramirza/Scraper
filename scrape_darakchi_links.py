from text_scraper_util import set_firefox_driver, find_elements_by_css_selector
import time
import os

# URL
# 1
# DARAKCHI_URL = "https://darakchi.uz/oz/feeds"
# 2
DARAKCHI_URL = "https://darakchi.uz/oz/feeds?page=912"

# SET FIREFOX DRIVER
driver = set_firefox_driver(is_headless=False, image_disabled=True, js_disabled=False)
driver.get(DARAKCHI_URL)


# FILE NAME
page_title_obj_list = find_elements_by_css_selector(selector=".container h1", driver=driver)
page_title_parts = page_title_obj_list[0].text.strip().split()
page_title = ""  # use this one -->
for part in page_title_parts:
    page_title += ''.join(char for char in part if char.isalpha())
    page_title = page_title.lower()
    page_title += "_" if part != page_title_parts[-1] else ""
# CREATE PAGE TITLE FOLDER
folder_path = os.path.join("darakchi_links", f"{page_title}_links")
os.makedirs(folder_path, exist_ok=True)

# check
scraped_links = []
with open(f"darakchi_links/{page_title}_links/{page_title}_links.txt", "r") as see_f:
    lines = see_f.readlines()
    for line in lines:
        line = line.strip()
        scraped_links.append(line)

counter = 1
page_num = 912
while True:
    # CHECK IF NEXT PAGE EXISTS
    news_links = []
    # FETCH PAGE NEWS
    if page_news := find_elements_by_css_selector(selector=".container .card a", driver=driver):
        for news in page_news:
            try:
                valid_link = news.get_attribute("href")
            except Exception as e:
                print("Exception in getting href attribute", e)
            else:
                if valid_link not in scraped_links:
                    news_links.append(valid_link)

        # WRITE INTO FILE
        if news_links:
            with open(f"darakchi_links/{page_title}_links/{page_title}_links.txt", "a") as file:
                news_links = set(news_links)
                file.writelines(f"{link}\n" for link in news_links)

        # LOG
        print(f"\rIteration: {counter} & Finished: {driver.current_url}", end="", flush=True)
        counter += 1

    if find_elements_by_css_selector(selector=".d-flex .pagination li", driver=driver):
        driver.get(f"https://darakchi.uz/oz/feeds?page={page_num}")
        page_num += 1
    else:
        break

    # NEXT PAGE
    # if next_page_btn := find_elements_by_css_selector(selector=".d-flex .pagination li", driver=driver):
    #    next_page_btn[-1].click()
    #    time.sleep(1)
    # else:
    #    break

driver.quit()

