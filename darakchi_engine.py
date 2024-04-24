import os.path
import re
import time

from text_scraper_util import set_firefox_driver, find_elements_by_css_selector, split_by_paragraph
from text_scraper_util import find_element_by_xpath, remove_newlines

# set driver
driver = set_firefox_driver(is_headless=True, image_disabled=True, js_disabled=True)


def scrape(start, end, file_path):
    print("Scraping started...")
    with open(file_path, "r") as file:
        links = file.readlines()

        counter = start
        for link in links[start:end]:
            link = link.strip()
            time.sleep(1)

            is_success = True
            # go to news page
            for i in range(2):
                try:
                    driver.get(link)
                    break
                except Exception as exc:
                    print(f"{i + 1} Exception in reaching the webpage: {link} -> ", exc)
                    time.sleep(1)
                    is_success = False

            if is_success:
                # get paragraph
                paragraph = ""
                if p_list := find_elements_by_css_selector(".container .pg-article__text p", driver, file_path, link):
                    for p in p_list:
                        text = p.text.strip()
                        text = text.replace("&nbsp;", "")
                        text = remove_newlines(text)
                        paragraph += text + "\n"

                    if paragraph:
                        # print(paragraph)
                        articles = split_by_paragraph(paragraph)

                        # folder name
                        day, month, year = "01", "01", "2025"
                        if date := find_element_by_xpath("/html/body/div[4]/div[1]/div/span", driver, link, file_path):
                            match = re.search(r'\d{2}\.\d{2}\.\d{4}', date.text.strip())
                            if match:
                                day, month, year = match.group().split(".")
                        folder_path = os.path.join("darakchi_content", year, month)
                        os.makedirs(folder_path, exist_ok=True)

                        # write content
                        with open(f"darakchi_content/{year}/{month}/{month}-{day}.txt", "a") as w_file:
                            for i in range(len(articles)):
                                paragraph_text = articles[i].strip()
                                w_file.write(f"{paragraph_text.strip()}\n")

                with open(f"darakchi_garbage_links.txt", "a") as g_file:
                    g_file.write(f"{link}\n")

            # log
            print(f"\rIteration: {counter} & Finished: {link}", end="", flush=True)
            counter += 1

    driver.quit()


# 1
# s, e, f_path = 0, 9892, "darakchi_links/yangiliklar_tasmasi_links/yangiliklar_tasmasi_links.txt"
# 2
# s, e, f_path = 9892, 50000, "darakchi_links/yangiliklar_tasmasi_links/yangiliklar_tasmasi_links.txt"
# 3
# s, e, f_path = 43362, 49000, "darakchi_links/yangiliklar_tasmasi_links/yangiliklar_tasmasi_links.txt"
# 4
# s, e, f_path = 50000, 99999, "darakchi_links/yangiliklar_tasmasi_links/yangiliklar_tasmasi_links.txt"
# 5
# s, e, f_path = 99999, 101776, "darakchi_links/yangiliklar_tasmasi_links/yangiliklar_tasmasi_links.txt"
# 6
s, e, f_path = 101776, 120007, "darakchi_links/yangiliklar_tasmasi_links/yangiliklar_tasmasi_links.txt"

# call scraper
scrape(s, e, f_path)
