# import web driver
import csv
from parsel import Selector
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os.path
#from selenium.webdriver.common.action_chains import ActionChains

file_path = 'C:/Users/aneogy/Desktop/Master_Thesis/TextClassification_Practise/output.csv'
resp = os.path.isfile(file_path)

print('Response', resp)

# store the information into a csv file
writer = csv.writer(open(file_path, 'w+', encoding='utf-8-sig', newline=''))
writer.writerow(['Name', 'Position', 'Company', 'Education', 'Location', 'URL'])


# specifies the path to the chromedriver.exe
driver = webdriver.Chrome('C:/Users/aneogy/chromedriver')
#profile_link="https://www.linkedin.com/in/ananya-neogi-33678653/"

# driver.get method() will navigate to a page given by the URL address
driver.get('https://www.linkedin.com/')
sleep(10)

# locate email form by_class_name
username = driver.find_element_by_name("session_key")
print(username)

# send_keys() to simulate key strokes
username.send_keys('youremail@gmail.com')
sleep(10)

# locate password form by_class_name
password = driver.find_element_by_name('session_password')

# send_keys() to simulate key strokes
password.send_keys('your account password')
sleep(2)

# locate submit button by_class_name
log_in_button = driver.find_element_by_class_name('sign-in-form__submit-btn')

# .click() to mimic button click
log_in_button.click()
sleep(2)

# driver.implicitly_wait(10)
# ActionChains(driver).move_to_element(log_in_button).click(log_in_button).perform()

driver.get('https://www.google.com/')
search_query = driver.find_element_by_name('q')
search_query.send_keys('site:linkedin.com/in AND "data scientist" AND "berlin"')
search_query.send_keys(Keys.RETURN)
sleep(0.5)

urls = driver.find_elements_by_xpath('//*[@class = "r"]/a[@href]')
urls = [url.get_attribute('href') for url in urls]
sleep(0.5)


for url in urls:
    driver.get(url)
    sleep(2)

    sel = Selector(text = driver.page_source)

    name = sel.xpath('//*[@class = "inline t-24 t-black t-normal break-words"]/text()').extract_first().split()
    name = ' '.join(name)

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
          
driver.quit()
# locate submit button by_xpath
#log_in_button = driver.find_element_by_xpath('//*[@type="submit"]')

