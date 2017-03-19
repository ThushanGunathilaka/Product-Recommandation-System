from PRSBoot.PRSBootAccess.PRSMongoDB.PRSInitMongoDB import InitMongoDB
from PRSBoot.PRSBootAccess.PRSMySQL.PRSInitMySQL import InitMySQL
from PRSBoot.PRSBootAccess.PRSMongoDB.PRSQueryMongoDB import QueryMongoDB
from PRSBoot.PRSBootAccess.PRSMySQL.PRSQueryMySQL import QueryMySQL
import logging

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger("Boot Database Access")
from PRSBoot.PRSConfig import Conf
LOGGER.propagate = Conf().getVerbose()

# file handler
handler = logging.FileHandler('PRS.log')
handler.setLevel(logging.INFO)
# logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

LOGGER.addHandler(handler)

class Access(object):
    '''
    pymysql and pymongo instance related queries
    '''

    ''' Create MongoDB Collections and MySQl Tables for Recommandation Models '''

    def initMongoDB(self,mongoDBObject,databaseName):
        checkStatus = True
        #LOGGER.info ('************************************************************')
        #LOGGER.info ("Failures occur in following statements only when objects already exists in MongoDB server")
        #LOGGER.info ('************************************************************')
        #InitMongoDB().initSuggestionDataMongoDB(mongoDBObject,databaseName)
        #InitMongoDB().initSuggestionHistoryMongoDB(mongoDBObject,databaseName)
        #InitMongoDB().initUpdateDataMongoDB(mongoDBObject,databaseName)
        LOGGER.info ('************************************************************')
        LOGGER.info ("When All Following Tests Fail check mongoDB Server Status")
        LOGGER.info ('************************************************************')
        if not self.checkMongoDBTableExists(mongoDBObject,databaseName,Conf().getSuggestionDataCollectionName()):
            checkStatus = False
        if not self.checkMongoDBTableExists(mongoDBObject,databaseName,Conf().getUserDataCollectionName()):
            checkStatus = False
        if not self.checkMongoDBTableExists(mongoDBObject,databaseName,Conf().getSuggestionHistoryCollectionName()):
            checkStatus = False
        LOGGER.info ('************************************************************')
        return checkStatus

    def initMySQL(self,mySQLCursorConnection):
        checkStatus = True
        #LOGGER.info ('************************************************************')
        #LOGGER.info ("Failures occur in following statements only when objects already exists in MySQL server")
        #LOGGER.info ('************************************************************')
        #InitMySQL().initCatalogMySQL(mySQLCursorConnection)
        #InitMySQL().initDropCategoryMySQL(mySQLCursorConnection)
        #InitMySQL().initCreateCategoryMySQL(mySQLCursorConnection)
        #InitMySQL().initInsertCategoryMySQL(mySQLCursorConnection)
        LOGGER.info ('************************************************************')
        LOGGER.info ("When All Following Tests Fail check MySQl Server Status")
        LOGGER.info ('************************************************************')
        if not self.checkMySQLTableExists(mySQLCursorConnection,Conf().getCatalogTableName()):
            checkStatus = False
        if not self.checkMySQLTableExists(mySQLCursorConnection,Conf().getCategoryTableName()):
            checkStatus = False
        if not self.checkMySQLColumnExists(mySQLCursorConnection,Conf().getCategoryTableName(),Conf().getCategoryTableIDName()):
            checkStatus = False
        if not self.checkMySQLColumnExists(mySQLCursorConnection,Conf().getCatalogTableName(),Conf().getCatalogTableIDName()):
            checkStatus = False
        if not self.checkMySQLColumnExists(mySQLCursorConnection,Conf().getCatalogTableName(),Conf().getProductTableInStock()):
            checkStatus = False
        LOGGER.info ('************************************************************')
        mySQLCursorConnection.close()
        return checkStatus

    ''' Check MongoDB Collection Availability '''

    def checkMongoDBTableExists(self,mongoDBObject,database, colleactionName):
        return  QueryMongoDB().checkMongoDBTableExists(mongoDBObject,database, colleactionName)

    def checkMySQLTableExists(self,mySQLCursorConnection, tableName):
        return QueryMySQL().checkMySQLTableExists(mySQLCursorConnection, tableName)

    def checkMySQLColumnExists(self,mySQLCursorConnection, tableName, column):
        return QueryMySQL().checkMySQLColumnExists(mySQLCursorConnection, tableName, column)