import os.path

from text_scraper_util import set_firefox_driver, find_elements_by_css_selector, split_by_paragraph, remove_newlines
import time
import re

# set driver
driver = set_firefox_driver(is_headless=True, image_disabled=True, js_disabled=True)


def scrape(start, end, file_path):
    print("Scraping started...")

    counter = start
    with open(file_path, "r") as file:
        links = file.readlines()

        for link in links[start:end]:
            time.sleep(1)
            link = link.replace("\n", "")

            is_success = True
            # go to news_page
            for i in range(3):
                try:
                    driver.get(link)
                    break
                except Exception as exc:
                    print(f"  {i + 1} Exception in reaching the webpage: {link} -> ", exc)
                    time.sleep(1)
                    is_success = False

            if is_success:
                # file name
                year, month, day = "", "", ""
                match = re.search(r'\d{4}/\d{2}/\d{2}', link)
                if match:
                    year, month, day = match.group().split("/")
                else:
                    year, month, day = "2025", "01", "01"
                folder_path = os.path.join("gazetauz_content", year, month)
                os.makedirs(folder_path, exist_ok=True)

                # subtitle
                subtitle = ""
                if headline := find_elements_by_css_selector(".articleTopBG h4", driver, file_path, link):
                    subtitle = headline[0].text.strip()
                else:
                    with open("garbage_links.txt", "a") as g_file:
                        g_file.write(f"{link}\n")

                # article
                paragraph = ""
                if p_list := find_elements_by_css_selector(".articleContent .article-text p", driver, file_path, link):
                    for p in p_list:
                        text = p.text.strip()
                        text = text.replace("&nbsp;", "")
                        text = remove_newlines(text)
                        paragraph += text + "\n"

                    if paragraph:
                        # print(paragraph)
                        articles = split_by_paragraph(paragraph)

                        # write content
                        with open(f"gazetauz_content/{year}/{month}/{month}-{day}.txt", "a") as w_file:
                            if subtitle:
                                w_file.write(f"{subtitle}\n")
                            for i in range(len(articles)):
                                paragraph_text = articles[i].strip()
                                w_file.write(f"{paragraph_text.strip()}\n")
            # log
            print(f"\rIteration: {counter} & Finished: {link}", end="", flush=True)
            counter += 1

    driver.quit()


# 1
# s, e, f_path = 0, 9999, "gazetauz_links/yangiliklar/yangiliklar.txt"
# 2
# s, e, f_path = 9999, 19999, "gazetauz_links/yangiliklar/yangiliklar.txt"
# 3
# s, e, f_path = 19999, 20102, "gazetauz_links/yangiliklar/yangiliklar.txt"
# 4
# s, e, f_path = 20102, 38114, "gazetauz_links/yangiliklar/yangiliklar.txt"
# 5
# s, e, f_path = 0, 489, "gazetauz_links/maqolalar/maqolalar.txt"
# 6
# s, e, f_path = 0, 159, "gazetauz_links/media/media.txt"
# 7
s, e, f_path = 0, 59, "gazetauz_links/reportajlar/reportajlar.txt"


# call scraper
scrape(s, e, f_path)
