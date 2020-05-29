import psycopg2
import db.queries as queries
import logging

logging.basicConfig(level=logging.INFO)
user="gtvdrkjgsvphfm"
password="14eb59e2296723ea6865c1cd6abf1c8acad0f3f92fe99674d42cc62961116f85"
host="ec2-54-246-90-10.eu-west-1.compute.amazonaws.com"
port="5432"
database="dbhribebhu9rel"

class DbClient:
    def connect(self):
        self.connection = psycopg2.connect(user="gtvdrkjgsvphfm",
                                           password="14eb59e2296723ea6865c1cd6abf1c8acad0f3f92fe99674d42cc62961116f85",
                                           host="ec2-54-246-90-10.eu-west-1.compute.amazonaws.com",
                                           port="5432",
                                           database="dbhribebhu9rel")
        logging.info("Initialized the connection to db")
        return self.connection

    def execute_query(self, query):
        cursor = self.connection.cursor()
        logging.info("Executing query: \n" + query)
        try:
            cursor.execute(query)
            self.connection.commit()
        except Exception as e:
            logging.error("Execution was failed")
            logging.error(e)
        else:
            logging.info("Execution completed successfully")
        finally:
            cursor.close()

        return self

    def finalize(self):
        if self.connection:
            self.connection.close()
            logging.info("Connection to DB is closed")
