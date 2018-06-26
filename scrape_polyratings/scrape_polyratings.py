from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from datetime import datetime

chromedriver_url = "./chromedriver"
driver = webdriver.Chrome(chromedriver_url)
prof_list_url = 'http://polyratings.com/list.php'

bad_urls = ['http://polyratings.com/eval.php?profid=728', 'http://polyratings.com/eval.php?profid=717', 'http://polyratings.com/eval.php?profid=715', 'http://polyratings.com/eval.php?profid=694','http://polyratings.com/eval.php?profid=693', 'http://polyratings.com/eval.php?profid=509', 'http://polyratings.com/eval.php?profid=542', 'http://polyratings.com/eval.php?profid=583']

def get_prof_urls(url, driver):
    driver.get(url)
    xpath = '/html/body/div/a[*]'
    urls = []
    for link in driver.find_elements(By.XPATH, xpath):
        urls.append(link.get_attribute('href'))
    return [url for url in urls if url not in bad_urls]

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

class Professor:

    def __init__(self, pid, f_name, l_name, reviews, department):
        self.pid = pid
        self.f_name = f_name
        self.l_name = l_name
        self.reviews = reviews
        self.department = department

    def insert_statement(self):
        return (
            "INSERT INTO Professor (pid, f_name, l_name, department)"
            "VALUES (%s, %s, %s, %s)"
        )

    def insert_values(self):
        return (self.pid, self.f_name, self.l_name, self.department)

    @staticmethod
    def create_statement():
        return (
            "CREATE TABLE `professor` ("
            "   `pid` INTEGER, "
            "   `f_name` VARCHAR(20), "
            "   `l_name` VARCHAR(20), "
            "   `department` VARCHAR(50), "
            "   PRIMARY KEY (`pid`) "
            ") ENGINE=InnoDB")

class Review:

    def __init__(self, rid, pid, content, class_name, rating_overall,
        rating_difficulty, reason_taking, date_posted, grade_received,
        class_standing):

        self.rid = rid
        self.pid = pid
        self.content = content
        self.class_name = class_name
        self.rating_overall = rating_overall
        self.rating_difficulty = rating_difficulty
        self.reason_taking = reason_taking
        self.date_posted = date_posted
        self.grade_received = grade_received
        self.class_standing = class_standing

    def insert_statement(self):
        return (
            "INSERT INTO review (rid, pid, content, class_name, "
            "rating_overall, rating_difficulty, reason_taking, date_posted, "
            "grade_received, class_standing) VALUES (%s, %s, %s, %s, %s, %s, "
            "%s, %s, %s, %s)"
        )

    def insert_values(self):
        return (self.rid, self.pid, self.content, self.class_name,
            self.rating_overall, self.rating_difficulty, self.reason_taking,
            self.date_posted, self.grade_received, self.class_standing
        )

    @staticmethod
    def create_statement():
        return (
            "CREATE TABLE `review` ("
            "  `rid` INTEGER,"
            "  `pid` INTEGER,"
            "  `content` VARCHAR(5000),"
            "  `class_name` VARCHAR(20),"
            "  `rating_overall` DOUBLE(4,2),"
            "  `rating_difficulty` DOUBLE(4,2),"
            "  `reason_taking` enum('R', 'S', 'E'),"
            "  `date_posted` DATETIME,"
            "  `grade_received` VARCHAR(10),"
            "  `class_standing` VARCHAR(20),"
            "  PRIMARY KEY (`rid`),"
            "  FOREIGN KEY (`pid`) REFERENCES `professor` (`pid`)"
            "    ON DELETE CASCADE"
            ") ENGINE=InnoDB")

professors = []

pid_count = 0
rid_count = 0

prof_urls = get_prof_urls(prof_list_url, driver)

print('Begin scraping data...')

for prof_url in prof_urls[2430:]:
    print('\t> scraping data from page ' + str(pid_count + 1) + '/' + str(len(prof_urls)) + ': ' + prof_url)
    driver.get(prof_url)
    prof_name = parse_prof_name(driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/h1/strong').text)
    prof_department = clean_whitespace(driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/h4[2]').text)
    rating_overall = parse_rating_overall(driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/span/h2').text)
    rating_difficulty = parse_rating_difficulty(driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/span/b[2]').text)
    reviews = []
    class_sections = driver.find_elements(By.CLASS_NAME, 'group')
    for class_section in class_sections:
        class_name = clean_whitespace(class_section.find_element(By.TAG_NAME, 'h2').text)
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
            reviews.append(Review(rid_count, pid_count, comment.text, class_name, rating_overall, rating_difficulty, reason_taking, date_posted, grade_received, class_standing))
            rid_count += 1
    prof = Professor(pid_count, prof_name[0], prof_name[1], reviews, prof_department)
    professors.append(prof)
    pid_count += 1

driver.close()

print('End scraping data...')


import mysql.connector
from mysql.connector import errorcode

print("Connecting to database...")

try:
    cnx = mysql.connector.connect(option_files='db_config.cnf', raise_on_warnings=True)
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    print("Connected successfully...")
    cursor = cnx.cursor()

    TABLES = {}
    TABLES['professor'] = Professor.create_statement()
    TABLES['review'] = Review.create_statement()

    try:
        cursor.execute("DROP TABLE IF EXISTS `review`")
        cursor.execute("DROP TABLE IF EXISTS `professor`")
    except:
        pass

    for name, ddl in TABLES.items():
        try:
            print("Creating table {}: ".format(name), end='')
            cursor.execute(ddl)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

    print("Inserting values into tables...")
    for prof in professors:
        cursor.execute(prof.insert_statement(), prof.insert_values())
        for review in prof.reviews:
            cursor.execute(review.insert_statement(), review.insert_values())

    cnx.commit()
    cursor.close()
    cnx.close()
