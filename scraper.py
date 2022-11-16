"""
&copy; Glitch Taylor 2022

Attempts to scrape information from linkedin using selenium.
Last working May 6th, 2022. Probably outdated soon.

Data that's downloaded:
- Name
- Title
- About
- Everything listed under:
    - Experience
    - Volunteering
    - Education
"""

# Imports
import json
import random
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
                .find_element(By.CLASS_NAME, "visually-hidden").text.strip().replace('\n', ' ')

            # Get item subtitle
            try:
                subtitle = item.find_element(By.CLASS_NAME, 't-14') \
                    .find_element(By.CLASS_NAME, 'visually-hidden').text.strip().replace('\n', ' ')
            except:
                subtitle = None

            # Get item date
            try:
                dates = item.find_element(By.CLASS_NAME, 't-black--light') \
                    .find_element(By.CLASS_NAME, 'visually-hidden').text.strip().replace('\n', ' ')
            except:
                dates = None

            # Item may have multiple description/date entries, loop over each
            try:
                descriptions = item.find_element(By.CLASS_NAME, 'pvs-list')
                if descriptions:
                    # Loop over descriptions
                    desc_items = descriptions.find_elements("li")
                    if len(desc_items) == 1:
                        # Just a single item description
                        desc = desc_items[0].find_element(By.CLASS_NAME, 'visually-hidden').text.strip().replace('\n',
                                                                                                                 ' ')
                        section.append({"Title": title, "Subtitle": subtitle, "Dates": dates, "Description": desc})
                    else:
                        # Multiple entries
                        for desc in descriptions.find_elements("li"):
                            try:
                                title2 = " - " + desc.find_element(By.CLASS_NAME, 'mr1') \
                                    .find_element(By.CLASS_NAME, 'visually-hidden') \
                                    .text.strip().replace('\n', ' ')
                                title += title2
                            except:
                                pass

                            try:
                                dates2 = desc.find_element(By.CLASS_NAME, 't-black--light') \
                                    .find_element(By.CLASS_NAME, 'visually-hidden') \
                                    .text.strip().replace('\n', ' ')
                                dates = dates2
                            except:
                                pass

                            try:
                                subtitle2 = desc.find_element(By.CLASS_NAME, 't-14') \
                                    .find_element(By.CLASS_NAME, 'visually-hidden') \
                                    .text.strip().replace('\n', ' ')
                                subtitle = subtitle2
                            except:
                                pass

                            try:
                                desc2 = desc.find_element(By.CLASS_NAME, 'pvs-list') \
                                    .find_element(By.CLASS_NAME, 'visually-hidden') \
                                    .text.strip().replace('\n', ' ')
                                descriptions = desc2
                            except:
                                pass

                            section.append(
                                {"Title": title, "Subtitle": subtitle, "Dates": dates, "Description": descriptions})
            except:
                pass

    except NoSuchElementException:
        # Section doesn't exist on page, skip
        if VERBOSE: print("0", section_id)

    return section


if __name__ == '__main__':
    # Constants
    USERNAME = getenv("LINKEDIN_USERNAME")
    PASSWORD = getenv("LINKEDIN_PASSWORD")
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
    sleep(random.uniform(3, 4))
    driver.find_element(By.NAME, "session_key").send_keys(USERNAME)
    sleep(random.uniform(0.2, 0.4))
    driver.find_element(By.NAME, "session_password").send_keys(PASSWORD)
    sleep(random.uniform(0.2, 0.4))
    driver.find_element(By.CLASS_NAME, "sign-in-form__submit-button").click()
    sleep(random.uniform(3, 4))

    # Go to each page and download publicly available user information
    for url in urls:
        if len(url) > 0 and url not in SCRAPED_DATA:
            # Load page
            driver.get(url)
            sleep(random.uniform(3, 5))

            # Progressively scroll down page to load everything on it
            driver.execute_script(
                "const sleep = ms => new Promise(r => setTimeout(r, ms)); let height = document.body.scrollHeight; for (let i=0; i<height/200; i++) {window.scrollTo(0, i*200); await sleep(50)}")
            sleep(random.uniform(3, 5))

            # Expand all "...see more" buttons
            buttons = driver.find_elements(By.TAG_NAME, "button")
            for button in buttons:
                if "see" in button.text and "more" in button.text:
                    actions.move_to_element(button).click(button).perform()
                    sleep(random.uniform(0.2, 0.4))

            sel = Selector(text=driver.page_source)

            # Scrape name
            name = sel.xpath(
                '//*[@class = "text-heading-xlarge inline t-24 v-align-middle break-words"]/text()').extract_first().strip().replace(
                '\n', ' ')
            print(name)

            # Scape title
            try:
                title = sel.xpath(
                    '//*[@class = "text-body-medium break-words"]/text()').extract_first().strip().replace('\n', ' ')
            except AttributeError:
                title = None

            # Scape about
            try:
                about = sel.xpath(
                    '//*[@class="pv-shared-text-with-see-more t-14 t-normal t-black display-flex align-items-center"]/div/span[@class="visually-hidden"]/text()').extract_first().strip().replace(
                    '\n', ' ')
            except AttributeError:
                about = None

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

            # Save after every single scrape just to be sure, since linkedin sometimes logs out
            with open('output.json', 'w') as file:
                json.dump(SCRAPED_DATA, file)

            sleep(random.uniform(10, 15))

    driver.quit()
