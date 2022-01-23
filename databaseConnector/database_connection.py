import os
from loguru import logger
from from_root import from_root
from mysql.connector import connect

logger.add(sink=os.path.join(from_root(), 'logs.log'),
           format="[{time:YYYY-MM-DD HH:mm:ss.SSS} - {level} - {module} ] - {message}",
           level="INFO")


class MysqlHelper:
    """This Class is created to execute mysql query with less code"""

    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password

    def get_connection(self):
        try:
            cnx = connect(user=self.user,
                          host=self.host,
                          password=self.password)
            return cnx
        except Exception as e:
            logger.error("Error in mysql connection {0}".format(e.__str__()))
            return False

    def fetch_one(self, query=None):
        try:
            cnx = self.get_connection()
            cursor = cnx.cursor()
            cursor.execute(query)
            data = cursor.fetchone()
            cursor.close()
            cnx.close()
            return data

        except Exception as e:
            logger.error("Error in fetch one {0}".format(e.__str__()))
            return False

    def fetch_all(self, query):
        try:
            cnx = self.get_connection()
            cursor = cnx.cursor()
            cursor.execute(query)
            data = cursor.fetchall(query)
            cursor.close()
            cnx.close()
            return data

        except Exception as e:
            logger.error("Error in fetch all {0}".format(e.__str__()))
            return False

    def delete_record(self, query):
        try:
            cnx = self.get_connection()
            cursor = cnx.cursor()
            cursor.execute(query)
            cnx.commit()
            cnx.close()
            cursor.close()
            return True

        except Exception as e:
            logger.error("Error in delete record {0}".format(e.__str__()))
            return False

    def update_record(self, query):
        try:
            cnx = self.get_connection()
            cursor = cnx.cursor()
            cursor.execute(query)
            cnx.commit()
            cursor.close()
            cnx.close()
            return True

        except Exception as e:
            logger.error("Error in update record {0}".format(e.__str__()))
            return False

    def insert_record(self, query):
        try:
            cnx = self.get_connection()
            cursor = cnx.cursor()
            cursor.execute(query)
            cnx.commit()
            cursor.close()
            cnx.close()
            return True

        except Exception as e:
            logger.error("Error in insert record {0}".format(e.__str__()))
            return False
