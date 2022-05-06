# linkedin-scraper

Attempts to scrape information from linkedin using selenium and python.

---

Data that's downloaded:

- Name
- Title
- About
- Everything listed under:
    - Experience
    - Volunteering
    - Education

---

How to use:

1. Make sure you have a valid Python3 installation with the selenium and parsel packages.
2. Also ensure chrome/chromium is installed on your system for selenium to use.
3. In scraper.py, Replace "YOUR_LINKEDIN_USERNAME" with your username and "YOUR_LINKEDIN_PASSWORD" with your password,
   so that selenium
   can login to LinkedIn and view profiles.
4. Add the urls you would like to download data from to urls.txt, with each web address on a new line.
5. Run scraper.py, this will open a new chromium window, login to linkedin, and then scrape data from the profiles. It
   will generate output.json and fill it with profile information as the code runs. It may take a while to fully
   download all the profiles, since each profile takes about 10-20 seconds.
6. (optional) Run json_to_csv.py, which will convert output.json to output.csv. The CSV file can then be imported into
   Excel/Google Sheets.