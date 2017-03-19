from datetime import datetime
import logging

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger("Query From MySQL")
from PRSBoot.PRSConfig import Conf
LOGGER.propagate = Conf().getVerbose()

# file handler
handler = logging.FileHandler('PRS.log')
handler.setLevel(logging.INFO)
# logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

LOGGER.addHandler(handler)

from PRSHandler.PRSDataAccess.PRSMySQL.PRSPyMySQL import PyMySQL
class MySQLQuery(object):
    '''pymysql related queries '''

    def getAvailableSetFromIntList(self,tableName,column,items,appendWhereClause):
        '''
        Return available list in MySQl Database Using pymysql
        '''
        result = []
        itemSet = items
        try:
            itemSet = list(map(int,items))
        except:
            pass
        whereClause = self.iterateForWhereClause(tableName,column,itemSet)
        if whereClause is not None and len(whereClause) > 0 and appendWhereClause is not None and len(appendWhereClause)>0:
            whereClause = whereClause + ' AND ' + appendWhereClause
        query = 'SELECT {}.{} FROM beforecart.{} WHERE {};'.format(tableName,column,tableName,whereClause)
        filteredList = PyMySQL().fetchListFromMySQL(query)
        if filteredList is not None and len(filteredList)>0:
            result = filteredList
            LOGGER.info ("Items : {} Available From List : {} In Table [{}], Column [{}]".format(filteredList,itemSet,tableName,column))
        else:
            LOGGER.info ("List : {} not available in Table [{}], Column [{}]".format(itemSet,tableName,column))
        return result

    def iterateForWhereClause(self,tableName,column,items):
        queryString = ''
        cloumnCheck = self.checkColumnInMySQLTableExists(tableName,column)
        if column != None and len(column)> 0 and cloumnCheck and list != None and len(items)> 0:
            for item in items:
                queryString = queryString + ' or '+ column + ' = ' + str(item)
            queryString = queryString[3:]
        LOGGER.info ("Where clause Append [{}]".format(queryString))
        return queryString

    def checkColumnInMySQLTableExists(self,tableName,column):
        '''
        pymysql table column check
        '''
        result = False
        query = "SELECT * FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = 'beforecart' AND TABLE_NAME = '{}' AND COLUMN_NAME = '{}'".format(tableName,column)
        resultsCount = PyMySQL().fetchCountFromMySQL(query)
        if resultsCount is not None and resultsCount == 1:
            LOGGER.info ("Cloumn [{}], Found in MySQL table [{}]".format(column,tableName))
            result = True
        else:
            LOGGER.info ("Cloumn [{}], Does not Exists in MySQL table [{}]".format(column,tableName))
            result = False
        return result
