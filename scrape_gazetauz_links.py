from text_scraper_util import set_firefox_driver, find_elements_by_css_selector
import time
import os

# Yangiliklar
# GAZETAUZ_URL = "https://www.gazeta.uz/oz/list/news/"
# Maqolalar
# GAZETAUZ_URL = "https://www.gazeta.uz/oz/list/articles?page=1"
# Reportajlar
# GAZETAUZ_URL = "https://www.gazeta.uz/oz/list/reporting?page=1"
# Media
GAZETAUZ_URL = "https://www.gazeta.uz/oz/list/media/?page=1"

driver = set_firefox_driver(is_headless=True, image_disabled=True, js_disabled=True)
driver.get(GAZETAUZ_URL)


folder_path = os.path.join("gazetauz_links", "media")
os.makedirs(folder_path, exist_ok=True)

counter = 1
while True:
    time.sleep(1)
    news_list = []
    if page_news := find_elements_by_css_selector(".leftContainer .nblock .nt a", driver):
        for news in page_news:
            try:
                valid_link = news.get_attribute("href")
            except Exception as e:
                print("Exception in getting href attribute", e)
            else:
                news_list.append(valid_link)

        with open("gazetauz_links/media/media.txt", "a") as file:
            file.writelines(f"{link}\n" for link in news_list)

        # LOG
        print(f"\rIteration: {counter} & Finished: {driver.current_url}", end="", flush=True)
        counter += 1

    counter += 1
    if counter < 17:
        driver.get(f"https://www.gazeta.uz/oz/list/media/?page={counter}")
    else:
        break

driver.quit()

