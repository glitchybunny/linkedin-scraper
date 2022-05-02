# Imports
import csv
from parsel import Selector
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import os.path
from os import getenv

'''
Data to download:
- Name
- Title
- About
- Everything listed under:
    - Experience
    - Volunteering
    - Education
'''

USERNAME = getenv('USERNAME')
PASSWORD = getenv('PASSWORD')

# Load URLs to download
with open("urls.txt") as file:  # file with each URL on a new line
    urls = file.read().split('\n')

# Login to linkedin
driver = webdriver.Chrome()
actions = ActionChains(driver)
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
    if len(url) > 0:
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
                sleep(0.5)

        # Scrape info from page
        sel = Selector(text=driver.page_source)
        name = sel.xpath(
            '//*[@class = "text-heading-xlarge inline t-24 v-align-middle break-words"]/text()').extract_first().strip()
        title = sel.xpath('//*[@class = "text-body-medium break-words"]/text()').extract_first().strip()
        about = sel.xpath(
            '//*[@class="pv-shared-text-with-see-more t-14 t-normal t-black display-flex align-items-center"]/div/span[@class="visually-hidden"]/text()').extract_first().strip()

        experience = driver.find_element(By.ID, "experience") \
            .find_element(By.XPATH, "..") \
            .find_element(By.XPATH, ".//ul") \
            .find_elements(By.XPATH, ".//li")
        print(len(experience))
        for exp in experience:
            actions.move_to_element(exp).perform()
            print(exp)#, exp.text, '\n\n')
            sleep(0.5)
            # print(exp.text)
            # exp_title = exp.find_element(By.XPATH, './/span[@class="mr1 t-bold"]/span').text.strip()
            # print(exp_title)

        # print("Name:", name)
        # print("Title:", title)
        # print("About:", about)

        sleep(10)

driver.quit()

"""
    position = sel.xpath('//*[@class = "mt1 t-18 t-black t-normal"]/text()').extract_first().split()
    position = ' '.join(position)

    experience = sel.xpath('//*[@class = "pv-top-card--experience-list"]')
    company = experience.xpath('./li[@data-control-name = "position_see_more"]//span/text()').extract_first()
    company = ''.join(company.split()) if company else None
    education = experience.xpath('.//li[@data-control-name = "education_see_more"]//span/text()').extract_first()
    education = ' '.join(education.split()) if education else None

    location = ' '.join(sel.xpath('//*[@class = "t-16 t-black t-normal inline-block"]/text()').extract_first().split())

    url = driver.current_url

    print('\n')
    print('Name: ', name)
    print('Position: ', position)
    print('Company: ', company)
    print('Education: ', education)
    print('Location: ', location)
    print('URL: ', url)
    print('\n')

    writer.writerow([name,
                     position,
                     company,
                     education,
                     location,
                     url])
"""
