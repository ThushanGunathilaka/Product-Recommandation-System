from contextlib import closing
from datetime import datetime
import logging
import pymysql

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger("Query From MySQL Database")
from PRSBoot.PRSConfig import Conf
LOGGER.propagate = Conf().getVerbose()

# file handler
handler = logging.FileHandler('PRS.log')
handler.setLevel(logging.INFO)
# logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

LOGGER.addHandler(handler)
from PRSBoot.PRSBootConfig.PRSManager import Manager
class QueryMySQL(object):
    '''pymysql related queries '''

    def checkMySQLTableExists(self,currentConnection, tableName):
        '''
        pymysql table check
        '''
        # prepare a cursor object using cursor() method
        currentCursor = currentConnection.cursor(pymysql.cursors.DictCursor)
        # Prepare SQL query
        result = False
        query = """
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_name = '{}'
            AND  TABLE_SCHEMA = '{}'
            """.format(tableName,Manager().getMySQLDefaultDatabase())
        try:
            # Execute the SQL command
            currentCursor.execute(query)
            count = currentCursor.fetchone()['COUNT(*)']
            if count is not None and count == 1:
                LOGGER.info (" MySQL table [{}].[{}] Exists, count [{}]".format(Manager().getMySQLDefaultDatabase(),tableName,count))
                result = True
            else:
                LOGGER.info (" MySQL table [{}].[{}] Does not Exists, count [{}]".format(Manager().getMySQLDefaultDatabase(),tableName,count))
                result = False
        except Exception as e:
            LOGGER.info (" MySQL table [{}].[{}] Does not Exists, count [{}]".format(Manager().getMySQLDefaultDatabase(),tableName,count))
            result = False
        currentConnection.commit()
        currentCursor.close()
        return result

    def checkMySQLColumnExists(self,currentConnection, tableName, column):
        '''
        pymysql column check
        '''
        # prepare a cursor object using cursor() method
        currentCursor = currentConnection.cursor(pymysql.cursors.DictCursor)
        # Prepare SQL query
        result = False
        query = """
            SELECT * 
            FROM information_schema.COLUMNS 
            WHERE 
                TABLE_SCHEMA = '{}' 
            AND TABLE_NAME = '{}' 
            AND COLUMN_NAME = '{}'
            """.format(Manager().getMySQLDefaultDatabase(),tableName, column)
        try:
            # Execute the SQL command
            currentCursor.execute(query)
            count = currentCursor.rowcount
            if count is not None and count == 1:
                LOGGER.info (" MySQL column [{}] Exists in Table [{}].[{}], count [{}]".format(column,Manager().getMySQLDefaultDatabase(),tableName,count))
                result = True
            else:
                LOGGER.info (" MySQL column [{}] Does not Exists in Table [{}].[{}], count [{}]".format(column,Manager().getMySQLDefaultDatabase(),tableName,count))
                result = False
        except Exception as e:
            LOGGER.info (" MySQL column [{}] Does not Exists in Table [{}].[{}], count [{}]".format(column,Manager().getMySQLDefaultDatabase(),tableName,count))
            result = False
        currentConnection.commit()
        currentCursor.close()
        return result