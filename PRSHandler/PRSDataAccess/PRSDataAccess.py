from PRSHandler.PRSDataAccess.PRSMongoDB.PRSMongoDBQuery import MongoDBQuery
from PRSHandler.PRSDataAccess.PRSMySQL.PRSMySQLQuery import MySQLQuery
import logging

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger("Database")
from PRSBoot.PRSConfig import Conf
LOGGER.propagate = Conf().getVerbose()

# file handler
handler = logging.FileHandler('PRS.log')
handler.setLevel(logging.INFO)
# logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

LOGGER.addHandler(handler)

class DataAccess(object):
    '''
    pymysql and pymongo instance related queries
    '''
    def checkCategoriesInTable(self,list):
        return MySQLQuery().getAvailableSetFromIntList(Conf().getCategoryTableName(),Conf().getCategoryTableIDName(),list,'')

    def checkProductsInTable(self,list):
        return MySQLQuery().getAvailableSetFromIntList(Conf().getCatalogTableName(),Conf().getCatalogTableIDName(),list,Conf().getProductTableInStock()+' = 1')

    def storeUpdateRequest(self,mongoDB,mongoDBdatabaseName,updateRequest,storeSuggestions):
        collectionName = Conf().getUserDataCollectionName()
        result = False
        if MongoDBQuery().checkMongoDBCollectionExists(mongoDB,mongoDBdatabaseName,collectionName):
            MongoDBQuery().pymongoInsertOne(mongoDB,mongoDBdatabaseName,collectionName,updateRequest)
            LOGGER.info('Store Old Suggestions : [{}]'.format(storeSuggestions))
            if storeSuggestions:
                collectionName = Conf().getSuggestionDataCollectionName()
                if MongoDBQuery().checkMongoDBCollectionExists(mongoDB,mongoDBdatabaseName,collectionName):
                    updateFind = {'userID':updateRequest["userID"]}
                    updateValue = {"$set": {'status':'FALSE'}}
                    currentFindValues = MongoDBQuery().pymongoSelect(mongoDB,mongoDBdatabaseName,collectionName,updateFind)
                    if currentFindValues is not None and len(currentFindValues) == 1 and currentFindValues[0]['status']=='TRUE':
                        MongoDBQuery().pymongoUpdateOne(mongoDB,mongoDBdatabaseName,collectionName,updateFind,updateValue)
                        del currentFindValues[0]["_id"]
                        MongoDBQuery().pymongoInsertOne(mongoDB,mongoDBdatabaseName,collectionName,currentFindValues[0])
                        LOGGER.info(' Suggestions Successfully Stored')
                    else:
                        LOGGER.info(' Suggestions Already Stored')
                    result = True
                else:
                    result = False
            else:
                result = True
            LOGGER.info(' User Data Stored')
        else:
            result = False
        return result
