import os
import re
import time

from text_scraper_util import set_firefox_driver, find_elements_by_css_selector
from text_scraper_util import remove_newlines, split_by_paragraph, find_element_by_xpath


# set driver
driver = set_firefox_driver(is_headless=True, image_disabled=True, js_disabled=True)


def scrape(start, end, file_path):
    print("Scraping started...")
    print(f"From {start} to {end}")
    with open(file_path, "r") as file:
        links = file.readlines()

        counter = start
        for link in links[start:end]:
            link = link.strip()
            time.sleep(2)

            is_success = True
            # go to news page
            for i in range(2):
                try:
                    driver.get(link)
                    break
                except Exception:
                    print(f"{i + 1} Exception in reaching the webpage: {link}")
                    time.sleep(1)
                    is_success = False

            if is_success:
                if elem := find_element_by_xpath("/html/body/div[2]/div[8]/div/div/div[1]/div/div[1]/span/a", driver):
                    title = elem.get_attribute("title")
                    if title != "Futbol":
                        # get paragraph
                        paragraph = ""
                        if p_list := find_elements_by_css_selector(".the-post .post-content p", driver, file_path, link):
                            for p in p_list:
                                text = p.text.strip()
                                text = text.replace("&nbsp;", "")
                                text = remove_newlines(text)
                                paragraph += text + "\n"

                            if paragraph:
                                articles = split_by_paragraph(paragraph)

                                # folder name
                                year, month, day = "2025", "01", "01"
                                match = re.search(r'\d{4}/\d{2}/\d{2}', link)
                                if match:
                                    year, month, day = match.group().split("/")

                                folder_path = os.path.join("daryouz_content", year, month)
                                os.makedirs(folder_path, exist_ok=True)

                                with open(f"daryouz_content/{year}/{month}/{month}-{day}.txt", "a") as w_file:
                                    for i in range(len(articles)):
                                        w_file.write(f"{articles[i].strip()}\n")
                else:
                    # if not found
                    with open("daryouz_garbage_links.txt", "a") as g_file:
                        g_file.write(f"{link}\n")

            # log
            print(f"Iteration: {counter} & Finished: {link}")
            counter += 1
            print()

    driver.quit()


