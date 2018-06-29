from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pickle

chrome_options = Options()
chrome_options.add_argument("--headless")
chromedriver_url = "/Users/jtorres/polyratings/scrape_polyratings/chromedriver"
driver = webdriver.Chrome(executable_path=chromedriver_url,
                          chrome_options=chrome_options)

prof_list_url = 'http://polyratings.com/list.php'


bad_urls = ['http://polyratings.com/eval.php?profid=728',
            'http://polyratings.com/eval.php?profid=717',
            'http://polyratings.com/eval.php?profid=715',
            'http://polyratings.com/eval.php?profid=694',
            'http://polyratings.com/eval.php?profid=693',
            'http://polyratings.com/eval.php?profid=509',
            'http://polyratings.com/eval.php?profid=542',
            'http://polyratings.com/eval.php?profid=583']


def get_prof_urls(url, driver):
    driver.get(url)
    xpath = '/html/body/div/a[*]'
    urls = []
    for link in driver.find_elements(By.XPATH, xpath):
        urls.append(link.get_attribute('href'))
    return [url for url in urls if url not in bad_urls]


with open("./urls.pkl", "wb") as pickle_file:
    urls = get_prof_urls(prof_list_url, driver)
    pickle.dump(urls, pickle_file)
