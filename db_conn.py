import MySQLdb

sql_table_create = "CREATE TABLE  IF NOT EXISTS `epic_data_1` ( `s_no` INT NOT NULL AUTO_INCREMENT , `epic_no` VARCHAR(16) NOT NULL , `district` VARCHAR(3) NULL DEFAULT NULL , `queried` BOOLEAN NOT NULL DEFAULT FALSE , `ac_no` VARCHAR(4) NULL DEFAULT NULL, `part_no` VARCHAR(5) NULL DEFAULT NULL, `section_no` VARCHAR(7) NULL DEFAULT NULL , `serial_no` VARCHAR(10) NULL DEFAULT NULL , `house_no` VARCHAR(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL, `electors_name` VARCHAR(30) NULL DEFAULT NULL , `electors_name_hindi` VARCHAR(40) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL , `relatives_name` VARCHAR(30) NULL DEFAULT NULL , `relatives_name_hindi` VARCHAR(40) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL , `dob` VARCHAR(10) NULL DEFAULT NULL , `age` VARCHAR(3) NULL DEFAULT NULL , `gender` VARCHAR(1) NULL DEFAULT NULL , PRIMARY KEY (`epic_no`), UNIQUE (`s_no`)) ENGINE = InnoDB;"

def getConnection():
    return MySQLdb.connect(host="localhost",
                     user="root",
                     passwd="myIsy269",
                     db="test"
                     )

def getCursor(db):
    db.set_character_set('utf8')
    cur = db.cursor()
    cur.execute('SET NAMES utf8;')
    cur.execute('SET CHARACTER SET utf8;')
    cur.execute('SET character_set_connection=utf8;')

    return cur