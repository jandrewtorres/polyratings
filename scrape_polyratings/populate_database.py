import mysql.connector
from mysql.connector import errorcode
from scrape_polyratings import Professor, Review
import pickle
import sys

if len(sys.argv) == 0:
    sys.exit("You must enter a file name")

with open(sys.argv[0], 'rb') as pickle_file:
    professors = pickle.load(pickle_file)
    reviews = pickle.load(pickle_file)

    print("Connecting to database...")

    try:
        cnx = mysql.connector.connect(
            option_files='db_config.cnf', raise_on_warnings=True)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cursor = cnx.cursor()

        TABLES = {}
        TABLES['professor'] = Professor.create_statement()
        TABLES['review'] = Review.create_statement()

        print("\t> dropping tables...")
        try:
            cursor.execute("DROP TABLE IF EXISTS `review`")
            cursor.execute("DROP TABLE IF EXISTS `professor`")
        except Exception:
            pass

        for name, ddl in TABLES.items():
            try:
                print("\t> creating table {}: ".format(name), end='')
                cursor.execute(ddl)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else:
                    print(err.msg)
            else:
                print("OK")

        print("\t> inserting values into tables...")
        for index, prof in enumerate(professors):
            print("\t\t> inserting professor " + str(index) + "/" +
                  str(len(professors)) + ": " + prof.f_name + " " +
                  prof.l_name)
            cursor.execute(prof.insert_statement(), prof.insert_values())
            for review in prof.reviews:
                cursor.execute(review.insert_statement(),
                               review.insert_values())

        cnx.commit()
        cursor.close()
        cnx.close()
