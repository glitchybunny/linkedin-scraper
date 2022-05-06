'''
&copy; Glitch Taylor 2022

Attempts to scrape information from linkedin using selenium.
Last working May 6th, 2022. Probably outdated soon.

Data that is downloaded:
- Name
- Title
- About
- Everything listed under:
    - Experience
    - Volunteering
    - Education
'''

# Imports
import json
from parsel import Selector
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import os.path
from os import getenv


def extract_section(section_id):
    section = []
    try:
        section_items = driver.find_element(By.ID, section_id) \
            .find_elements(By.XPATH,
                           '..//ul//li[@class="artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column"]')
        if VERBOSE: print(len(section_items), section_id)

        for item in section_items:
            actions.move_to_element(item).perform()

            # Get item title
            title = item.find_element(By.CLASS_NAME, 'mr1') \
                .find_element(By.CLASS_NAME, "visually-hidden").text.strip()

            # Get item subtitle
            try:
                subtitle = item.find_element(By.CLASS_NAME, 't-14') \
                    .find_element(By.CLASS_NAME, 'visually-hidden').text.strip()
            except:
                subtitle = None

            # Get item dates, location
            try:
                dates = item.find_element(By.CLASS_NAME, 't-black--light') \
                    .find_element(By.CLASS_NAME, 'visually-hidden').text.strip()
            except:
                dates = None

            # Get item description
            try:
                desc = item.find_element(By.CLASS_NAME, 'pvs-list') \
                    .find_element(By.CLASS_NAME, 'visually-hidden').text.strip()
            except:
                desc = None

            section.append({"Title": title, "Subtitle": subtitle, "Dates": dates, "Description": desc})

    except NoSuchElementException:
        # Section doesn't exist on page, skip
        if VERBOSE: print("0", section_id)

    return section


if __name__ == '__main__':
    # Constants
    USERNAME = getenv('USERNAME')
    PASSWORD = getenv('PASSWORD')
    VERBOSE = True
    SCRAPED_DATA = {}

    # Load previously scraped data (if any)
    if os.path.exists("output.json"):
        with open("output.json", "r") as file:
            SCRAPED_DATA = json.load(file)

    # Load URLs to download
    with open("urls.txt") as file:  # file with each URL on a new line
        urls = file.read().split('\n')

    # Setup webdriver
    driver = webdriver.Chrome()
    actions = ActionChains(driver)
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    # Login to linkedin
    driver.get('https://www.linkedin.com/')
    sleep(3)
    driver.find_element(By.NAME, "session_key").send_keys(USERNAME)
    sleep(0.2)
    driver.find_element(By.NAME, "session_password").send_keys(PASSWORD)
    sleep(0.2)
    driver.find_element(By.CLASS_NAME, "sign-in-form__submit-button").click()
    sleep(3)

    # Go to each page and download publicly available user information
    for url in urls:
        if len(url) > 0 and url not in SCRAPED_DATA:
            # Load page
            driver.get(url)
            sleep(3)

            # Progressively scroll down page to load everything on it
            driver.execute_script(
                "const sleep = ms => new Promise(r => setTimeout(r, ms)); let height = document.body.scrollHeight; for (let i=0; i<height/200; i++) {window.scrollTo(0, i*200); await sleep(50)}")
            sleep(3)

            # Expand all "...see more" buttons
            buttons = driver.find_elements(By.TAG_NAME, "button")
            for button in buttons:
                if "see" in button.text and "more" in button.text:
                    actions.move_to_element(button).click(button).perform()
                    sleep(0.2)

            # Scrape basic info from page
            sel = Selector(text=driver.page_source)
            name = sel.xpath(
                '//*[@class = "text-heading-xlarge inline t-24 v-align-middle break-words"]/text()').extract_first().strip()
            print(name)
            title = sel.xpath('//*[@class = "text-body-medium break-words"]/text()').extract_first().strip()
            about = sel.xpath(
                '//*[@class="pv-shared-text-with-see-more t-14 t-normal t-black display-flex align-items-center"]/div/span[@class="visually-hidden"]/text()').extract_first().strip()

            # Scrape sections
            experience = extract_section("experience")
            volunteering = extract_section("volunteering_experience")
            education = extract_section("education")

            # Record data
            SCRAPED_DATA[url] = {
                "Name": name,
                "Title": title,
                "About": about,
                "Experience": experience,
                "Volunteering": volunteering,
                "Education": education
            }

            # Save after every single scrape, since linkedin likes logging out the scraper
            with open('output.json', 'w') as file:
                json.dump(SCRAPED_DATA, file)

            sleep(1)

    driver.quit()
