class Professor:

    def __init__(self, pid, f_name, l_name, reviews, department):
        self.pid = pid
        self.f_name = f_name
        self.l_name = l_name
        self.reviews = reviews
        self.department = department

    def insert_statement(self):
        return ("INSERT INTO Professor (pid, f_name, l_name, department)"
                "VALUES (%s, %s, %s, %s)")

    def insert_values(self):
        return (self.pid, self.f_name, self.l_name, self.department)

    @staticmethod
    def create_statement():
        return ("CREATE TABLE `professor` ("
                "   `pid` INTEGER, "
                "   `f_name` VARCHAR(20), "
                "   `l_name` VARCHAR(20), "
                "   `department` VARCHAR(50), "
                "   PRIMARY KEY (`pid`) "
                ") ENGINE=InnoDB")
