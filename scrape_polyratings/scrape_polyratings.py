from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import pickle
import sys
from review import Review
from professor import Professor


chrome_options = Options()
chrome_options.add_argument("--headless")
chromedriver_url = "/Users/jtorres/polyratings/scrape_polyratings/chromedriver"
driver = webdriver.Chrome(executable_path=chromedriver_url,
                          chrome_options=chrome_options)


def parse_prof_name(s):
    return s.replace(',', "").split()


def clean_whitespace(s):
    return ' '.join(s.split())


def parse_rating_overall(s):
    return float(s[:4])


def parse_rating_difficulty(s):
    return float(s[33:])


def parse_date_posted(s):
    return datetime.strptime(s, '%b %Y').strftime('%Y-%m-%d')


def parse_is_req_major(s):
    return 'TRUE' if s == 'Required (Major)' else 'FALSE'


def parse_is_req_support(s):
    return 'TRUE' if s == 'Required (Support)' else 'FALSE'


def parse_is_elective(s):
    return 'TRUE' if s == 'Elective' else 'FALSE'


def get_reason_taking_value(is_req, is_sup, is_elect):
    if is_req:
        return 'R'
    elif is_sup:
        return 'S'
    else:
        return 'E'


professors = []

pid_count = 0
rid_count = 0


print("Unpickling urls...")
prof_urls = []
with open("./urls.pkl", 'rb') as pickle_file:
    prof_urls = pickle.load(pickle_file)

if not prof_urls:
    sys.exit("No urls in pickle file...")


print('Begin scraping data...')

# for prof_url in prof_urls[2430:]:
for prof_url in prof_urls:
    print('\t> scraping data from page ' + str(pid_count + 1) + '/'
          + str(len(prof_urls)) + ': ' + prof_url)
    driver.get(prof_url)
    prof_name = parse_prof_name(driver.find_element(
        By.XPATH, '/html/body/div[1]/div[2]/div/div/h1/strong').text)
    prof_department = clean_whitespace(driver.find_element(
        By.XPATH, '/html/body/div[1]/div[2]/div/div/h4[2]').text)
    rating_overall = parse_rating_overall(driver.find_element(
        By.XPATH, '/html/body/div[1]/div[3]/span/h2').text)
    rating_difficulty = parse_rating_difficulty(driver.find_element(
        By.XPATH, '/html/body/div[1]/div[3]/span/b[2]').text)
    reviews = []
    class_sections = driver.find_elements(By.CLASS_NAME, 'group')
    for class_section in class_sections:
        class_name = clean_whitespace(
            class_section.find_element(By.TAG_NAME, 'h2').text)
        comments = class_section.find_elements(By.CLASS_NAME, 'eval-comment')
        eval_infos = class_section.find_elements(By.CLASS_NAME, 'eval-info')
        for index, comment in enumerate(comments):
            eval_info = eval_infos[index].text.split('\n')
            class_standing = clean_whitespace(eval_info[0])
            grade_received = clean_whitespace(eval_info[1])
            req_string = clean_whitespace(eval_info[2])
            reason_taking = get_reason_taking_value(
                parse_is_req_major(req_string),
                parse_is_req_support(req_string),
                parse_is_elective(req_string)
            )
            date_posted = parse_date_posted(clean_whitespace(eval_info[3]))
            reviews.append(
                Review(rid_count, pid_count, comment.text, class_name,
                       rating_overall, rating_difficulty, reason_taking,
                       date_posted, grade_received, class_standing))
            rid_count += 1
    prof = Professor(pid_count, prof_name[0], prof_name[1], reviews,
                     prof_department)
    professors.append(prof)
    pid_count += 1

driver.close()

print('End scraping data...')

pickle_file_name = "./polyratings_scrape_" \
    + str(datetime.datetime.now().strftime("%b-%d-%Y_%H:%M:%S"))

print("Pickling data to file: " + pickle_file_name)

with open(pickle_file_name, 'wb') as pickle_file:
    pickle.dump(professors, pickle_file)

print("Done pickling data.")
