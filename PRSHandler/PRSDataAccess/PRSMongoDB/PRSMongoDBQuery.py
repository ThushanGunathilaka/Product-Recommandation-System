from contextlib import closing
from bson.objectid import ObjectId
from datetime import datetime
import logging

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger("Query From MongoDB")
from PRSBoot.PRSConfig import Conf
LOGGER.propagate = Conf().getVerbose()

# file handler
handler = logging.FileHandler('PRS.log')
handler.setLevel(logging.INFO)
# logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

LOGGER.addHandler(handler)

class MongoDBQuery(object):
    '''pymongo related queries'''

    def pymongoInsertOne(self,mongoDB,mongoDBdatabaseName,collectionName,insertData):
        '''
        pymongo Insert and Check
        '''
        LOGGER.info (" MongoDB Insert On [{}][{}]".format(mongoDBdatabaseName,collectionName))
        LOGGER.info (" MongoDB Insert Value")
        LOGGER.info ("[{}]".format(insertData))
        with closing(mongoDB) as mongoDBObject:
            try:
                insertResult = mongoDBObject[mongoDBdatabaseName][collectionName].insert_one(insertData)
                LOGGER.info (" MongoDB Inserted Object ID : [{}]".format(insertResult.inserted_id))
                LOGGER.info (" MongoDB Inserted Value")
                LOGGER.info ("[{}]".format(mongoDBObject[mongoDBdatabaseName][collectionName].find_one({"_id": ObjectId(insertResult.inserted_id)})))
            except:
                LOGGER.info (" MongoDB Insert Failed")

    def checkMongoDBCollectionExists(self,mongoDBObject,database, colleactionName):
        '''
        pymongo collection check
        '''
        result = False
        with closing(mongoDBObject) as currentCursor:
            try:
                result = colleactionName in currentCursor[database].collection_names()
                if result is not None and result:
                    LOGGER.info ("MongoDB Collection [{}] Exists, [{}]".format(colleactionName, result))
                else:
                    LOGGER.info ("MongoDB Collection [{}] Does not Exists, [{}]".format(colleactionName, result))
            except:
                LOGGER.info ("MongoDB Collection [{}] Does not Exists".format(colleactionName))
        return result

    def pymongoUpdateOne(self,mongoDB,mongoDBdatabaseName,collectionName,updateFind,updateData):
        '''
        pymongo Update and Check
        '''
        LOGGER.info (" MongoDB Update On [{}][{}]".format(mongoDBdatabaseName,collectionName))
        LOGGER.info (" MongoDB Update Find")
        LOGGER.info (" {}".format(updateFind))
        LOGGER.info (" MongoDB Update Value")
        LOGGER.info (" {}".format(updateData))
        with closing(mongoDB) as mongoDBObject:
            try:
                updateResult = mongoDBObject[mongoDBdatabaseName][collectionName].update_one(updateFind,updateData, upsert=True)
                if updateResult.modified_count is not None and updateResult.modified_count > 0:
                    LOGGER.info (" MongoDB Updated Count : [{}]".format(updateResult.modified_count))
                    return True
                else:
                    LOGGER.info (" MongoDB Update Failed, Count : [{}]".format(updateResult.modified_count))
                    return False
            except:
                LOGGER.info (" MongoDB Update Failed")
                return True

    def pymongoSelect(self,mongoDB,mongoDBdatabaseName,collectionName,selectData):
        '''
        pymongo Select
        '''
        LOGGER.info (" MongoDB Select On [{}][{}]".format(mongoDBdatabaseName,collectionName))
        LOGGER.info (" MongoDB Select Value")
        LOGGER.info ("[{}]".format(selectData))
        outputData = []
        with closing(mongoDB) as mongoDBObject:
            try:
                selectResult = mongoDBObject[mongoDBdatabaseName][collectionName].find(selectData)
                if selectResult is not None:
                    LOGGER.info (" MongoDB Select")
                    for result in selectResult:
                        LOGGER.info (" {}".format(result))
                        outputData.append(result)
                    if outputData is not None and len(outputData)>0:
                        return outputData
                    else:
                        return None
                else:
                    LOGGER.info (" MongoDB Select Empty, Response : [{}]".format(selectResult))
                    return None
            except:
                LOGGER.info (" MongoDB Select Failed")
                return None