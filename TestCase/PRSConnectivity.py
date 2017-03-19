import unittest
from PRSBoot.PRSBootConfig.PRSManager import Manager
from PRSBoot.PRSBootConfig.PRSConnection import Connection
from PRSBoot.PRSBootAccess.PRSAccess import Access
from PRSBoot.PRSConfig import Conf
from PRSHandler.PRSDataAccess.PRSMySQL.PRSPyMySQL import PyMySQL
from PRSHandler.PRSDataAccess.PRSMongoDB.PRSMongoDBQuery import MongoDBQuery

import logging

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger("Test")
from PRSBoot.PRSConfig import Conf
LOGGER.propagate = Conf().getVerbose()

# file handler
handler = logging.FileHandler('PRS.log')
handler.setLevel(logging.INFO)
# logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

LOGGER.addHandler(handler)
from PRSHandler.PRSSuggestionManager.PRSInputs import Inputs

class Test_Connectivity(unittest.TestCase):
    '''
    Test cases for Tornado Server
    '''
    manager = Manager()
    query = Access()
    config = Conf()
    mySQL =PyMySQL()
    mongoDB = MongoDBQuery()
    connection = Connection()

    def test_selectAndUpdateMongoDB(self):
        updateFind = {'userID':0}
        selectData = self.mongoDB.pymongoSelect(self.connection.getMongoDBObject(),self.manager.getMongoDBDefaultDatabase(),self.config.getSuggestionDataCollectionName(),updateFind)
        #self.assertEqual(len(selectData),1)
        self.assertEqual(selectData[0]['userID'],0)
        updateValue = None
        if selectData[0]['status'] == 'FALSE':
            updateValue = 'TRUE'
        elif selectData[0]['status'] == 'TRUE':
            updateValue = 'FALSE'
        updateValue = {"$set": {'status':updateValue}}
        self.assertEqual(self.mongoDB.pymongoUpdateOne(self.connection.getMongoDBObject(),self.manager.getMongoDBDefaultDatabase(),self.config.getSuggestionDataCollectionName(),updateFind,updateValue),True)

#    def test_checkCurrentSuggestions(self):
#        self.assertNotEqual(Inputs(self.connection.getMongoDBObject(),self.manager.getMongoDBDefaultDatabase(),0).useCurrentSuggestions(),None)

    def test_checkMySQLFetchCount(self):
        query = "SELECT * FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = 'beforecart' AND TABLE_NAME = '{}' AND COLUMN_NAME = '{}'".format('Category','CATEGORY_ID')   
        self.assertNotEqual(self.mySQL.fetchCountFromMySQL(query),None)

    def test_checkMySQLCellValue(self):
        query = "SELECT VERSION()" 
        self.assertNotEqual(self.mySQL.fetchValueFromMySQL(query),None)

    def test_checkMySQLFetchTable(self):
        query = "SELECT * FROM Category"   
        self.assertNotEqual(self.mySQL.fetchListOfListsFromMySQL(query),None)

    def test_checkMySQLFetchColumn(self):
        query = "SELECT CATEGORY_ID FROM Category"   
        self.assertNotEqual(self.mySQL.fetchListFromMySQL(query),None)

    def test_getProductTableInStock(self):
        self.assertNotEqual(self.config.getProductTableInStock(),None)

    def test_getCatalogTableIDName(self):
        self.assertNotEqual(self.config.getCatalogTableIDName(),None)

    def test_getCategoryTableIDName(self):
        self.assertNotEqual(self.config.getCategoryTableIDName(),None)

    def test_getCatalogTableName(self):
        self.assertNotEqual(self.config.getCatalogTableName(),None)

    def test_getCategoryTableName(self):
        self.assertNotEqual(self.config.getCategoryTableName(),None)

    def test_getUserDataCollectionName(self):
        self.assertNotEqual(self.config.getUserDataCollectionName(),None)

    def test_getSuggestionDataCollectionName(self):
        self.assertNotEqual(self.config.getSuggestionDataCollectionName(),None)

    def test_getSuggestionHistoryCollectionName(self):
        self.assertNotEqual(self.config.getSuggestionHistoryCollectionName(),None)

    def test_getServerConfigFile(self):
        self.assertNotEqual(self.config.getServerConfig(),None)

    def test_getHandlerConfigFile(self):
        self.assertNotEqual(self.config.getHandlerConfig(),None)

    def test_getEngineConfigFile(self):
        self.assertNotEqual(self.config.getEngineConfig(),None)

    def test_CheckMySQLServer(self):
        self.assertEqual(self.query.initMySQL(self.connection.getMySQLConnection()),True)

    def test_CheckMongoDBServer(self):
        self.assertEqual(self.query.initMongoDB(self.connection.getMongoDBObject(),self.manager.getMongoDBDefaultDatabase()),True)

    def test_getServerHost(self):
        self.assertNotEqual(self.manager.getServerHost(),None)

    def test_getServerPort(self):
        self.assertNotEqual(self.manager.getServerPort(),None)

    def test_getServerProtocol(self):
        self.assertNotEqual(self.manager.getServerProtocol(),None)

    def test_getMySQLHost(self):
        self.assertNotEqual(self.manager.getMySQLHost(),None)

    def test_getMySQLPort(self):
        self.assertNotEqual(self.manager.getMySQLPort(),None)

    def test_getMySQLUsername(self):
        self.assertNotEqual(self.manager.getMySQLUsername(),None)

    def test_getMySQLPassword(self):
        self.assertNotEqual(self.manager.getMySQLPassword(),None)

    def test_getMySQLDefaultDatabase(self):
        self.assertNotEqual(self.manager.getMySQLDefaultDatabase(),None)

    def test_getMongoDBHost(self):
        self.assertNotEqual(self.manager.getMongoDBHost(),None)

    def test_getMongoDBPort(self):
        self.assertNotEqual(self.manager.getMongoDBPort(),None)

    def test_getMongoDBUsername(self):
        self.assertNotEqual(self.manager.getMongoDBUsername(),None)

    def test_getMongoDBPassword(self):
        self.assertNotEqual(self.manager.getMongoDBPassword(),None)

    def test_getMongoDBDefaultDatabase(self):
        self.assertNotEqual(self.manager.getMongoDBDefaultDatabase(),None)
if __name__ == '__main__':
    unittest.main()
