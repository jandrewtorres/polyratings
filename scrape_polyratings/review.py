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
        return ("INSERT INTO review (rid, pid, content, class_name, "
                "rating_overall, rating_difficulty, reason_taking, date_posted"
                ", grade_received, class_standing) VALUES (%s, %s, %s, %s, %s,"
                " %s, %s, %s, %s, %s)")

    def insert_values(self):
        return (self.rid, self.pid, self.content, self.class_name,
                self.rating_overall, self.rating_difficulty,
                self.reason_taking, self.date_posted, self.grade_received,
                self.class_standing)

    @staticmethod
    def create_statement():
        return ("CREATE TABLE `review` ("
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
