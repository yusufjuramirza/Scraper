from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Set Up Firefox Driver
def set_firefox_driver(is_headless, image_disabled, js_disabled):
    firefox_options = webdriver.FirefoxOptions()
    if is_headless:
        firefox_options.add_argument("--headless")
    if image_disabled:
        firefox_options.set_preference("permissions.default.image", 2)
        firefox_options.add_argument("--blink-settings=imagesEnabled=false")
    if js_disabled:
        firefox_options.add_argument("--disable-javascript")

    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)
    driver.implicitly_wait(2)

    return driver


# Find Elements By CSS Selectors
def find_elements_by_css_selector(selector, driver, link="default_link", file_p="default path"):
    wait = WebDriverWait(driver=driver, timeout=2)
    try:
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))
        return driver.find_elements(By.CSS_SELECTOR, selector)
    except TimeoutException:
        print(f"TimeoutException for CSS selector: {selector}")
        return []


def find_element_by_xpath(xpath, driver, link="default_link", file_p="default path"):
    wait = WebDriverWait(driver=driver, timeout=2)
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        return driver.find_element(By.XPATH, xpath)
    except TimeoutException:
        print(f"TimeoutException for xpath: {xpath}")
        return None


def split_by_paragraph(article_text):
    valid_endings = ['!', '?', '."', '.', ".'"]
    sentences = []

    prev = []
    for line in article_text.splitlines():
        line = line.strip()
        if line.endswith(tuple(valid_endings)):
            sentences.append(''.join(prev) + line)
            prev = []
        else:
            prev.append(line + " ")

    if prev:
        sentences.append(''.join(prev))

    return sentences


def has_strong(p):
    try:
        ps = p.find_elements_by_tag_name("strong")
        return True, len(p)
    except NoSuchElementException:
        return False, 0


# Remove New Lines
def remove_newlines(string: str) -> str:
    string = string.replace("\n", " ")
    string = string.replace("\\n", "")
    string = string.replace("   ", "  ")
    string = string.replace("  ", " ")
    string = string.strip()
    return string

