import logging
import pymysql

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger("PyMySQL Basic Query")
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
from PRSHandler.PRSSuggestionManager.PRSValidateInput.PRSValidate import Validate
class PyMySQL(object):
    """pymysql Basic query"""

    def fetchCountFromMySQL(self,query):
        '''
        pymysql table fetch Count
        '''
        manager = Manager()
        host = manager.getMySQLHost()
        port = manager.getMySQLPort()
        database = manager.getMySQLDefaultDatabase()
        username = manager.getMySQLUsername()
        password = manager.getMySQLPassword()
        result = None
        if host != None and port != None and database != None and username != None and password != None:
            #open connection
            #localhost-url with port; root -username- ""-password beforecart-database_name
            mySQLConnection = pymysql.connect(host,username,password,database)
            # prepare a cursor object using cursor() method
            currentCursor = mySQLConnection.cursor()
            try:
                # Execute the SQL command
                currentCursor.execute(query)
                result = Validate().convertToInt(currentCursor.rowcount)
                LOGGER.info (" Row Count : {} Fetched From Query : {}".format(result,query))
            except Exception as e:
                LOGGER.info (" Failed to Fetch Row Count From Query : {}".format(query))
                pass
            currentCursor.close()
            mySQLConnection.close()
        return result

    def fetchValueFromMySQL(self,query):
        '''
        pymysql table fetch One
        '''
        manager = Manager()
        host = manager.getMySQLHost()
        port = manager.getMySQLPort()
        database = manager.getMySQLDefaultDatabase()
        username = manager.getMySQLUsername()
        password = manager.getMySQLPassword()
        result = None
        if host != None and port != None and database != None and username != None and password != None:
            #open connection
            #localhost-url with port; root -username- ""-password beforecart-database_name
            mySQLConnection = pymysql.connect(host,username,password,database)
            # prepare a cursor object using cursor() method
            currentCursor = mySQLConnection.cursor()
            try:
                # Execute the SQL command
                currentCursor.execute(query)
                result = list(currentCursor.fetchone())[0]
                LOGGER.info (" Row : {} Fetched From Query : {}".format(result,query))
            except Exception as e:
                LOGGER.info (" Failed to Fetch Row From Query : {}".format(query))
                pass
            currentCursor.close()
            mySQLConnection.close()
        return result

    def fetchListOfListsFromMySQL(self,query):
        '''
        pymysql table fetch all
        '''
        manager = Manager()
        host = manager.getMySQLHost()
        port = manager.getMySQLPort()
        database = manager.getMySQLDefaultDatabase()
        username = manager.getMySQLUsername()
        password = manager.getMySQLPassword()
        result = None
        if host != None and port != None and database != None and username != None and password != None:
            #open connection
            #localhost-url with port; root -username- ""-password beforecart-database_name
            mySQLConnection = pymysql.connect(host,username,password,database)
            # prepare a cursor object using cursor() method
            currentCursor = mySQLConnection.cursor()
            try:
                # Execute the SQL command
                currentCursor.execute(query)
                result = currentCursor.fetchall()
                result = [list(x) for x in result]
                LOGGER.info ('{}'.format(result))
                LOGGER.info (" Table Fetched From Query : {}".format(query))
            except Exception as e:
                LOGGER.info (" Failed to Fetch Row From Query : {}".format(query))
                pass
            currentCursor.close()
            mySQLConnection.close()
        return result

    def fetchListFromMySQL(self,query):
        '''
        pymysql table fetch all
        '''
        manager = Manager()
        host = manager.getMySQLHost()
        port = manager.getMySQLPort()
        database = manager.getMySQLDefaultDatabase()
        username = manager.getMySQLUsername()
        password = manager.getMySQLPassword()
        result = None
        if host != None and port != None and database != None and username != None and password != None:
            #open connection
            #localhost-url with port; root -username- ""-password beforecart-database_name
            mySQLConnection = pymysql.connect(host,username,password,database)
            # prepare a cursor object using cursor() method
            currentCursor = mySQLConnection.cursor()
            try:
                # Execute the SQL command
                currentCursor.execute(query)
                result = currentCursor.fetchall()
                result = [element for tupl in result for element in tupl]
                LOGGER.info ('{}'.format(result))
                LOGGER.info (" Table Fetched From Query : {}".format(query))
            except Exception as e:
                LOGGER.info (" Failed to Fetch Row From Query : {}".format(query))
                pass
            currentCursor.close()
            mySQLConnection.close()
        return result