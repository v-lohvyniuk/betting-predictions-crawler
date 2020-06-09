import psycopg2
import db.queries as queries
import logging

logging.basicConfig(level=logging.INFO)

class DbConsts:
    user="ndsqqccomgcjru"
    password="7731f0b85d92b20adabadde4bfdcf2f2527534119324422e631bd5ef4f5dabdf"
    host="ec2-46-137-84-140.eu-west-1.compute.amazonaws.com"
    port="5432"
    database="d6acmb8v2cqk01"

class DbClient:
    def connect(self):
        self.connection = psycopg2.connect(user=DbConsts.user,
                                           password=DbConsts.password,
                                           host=DbConsts.host,
                                           port=DbConsts.port,
                                           database=DbConsts.database)
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
