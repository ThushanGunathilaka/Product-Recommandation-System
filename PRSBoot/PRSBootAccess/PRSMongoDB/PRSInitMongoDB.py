from contextlib import closing
from datetime import datetime
import logging

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger("Initialize MongoDB Database")
from PRSBoot.PRSConfig import Conf
LOGGER.propagate = Conf().getVerbose()

# file handler
handler = logging.FileHandler('PRS.log')
handler.setLevel(logging.INFO)
# logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

LOGGER.addHandler(handler)

class InitMongoDB(object):
    '''pymongo related initialization queries '''

    def initSuggestionDataMongoDB(self,mongoDBObject,databaseName):
        '''
        Create Suggestion Data MongoDB Collection for Recommandation Models
        '''
        with closing(mongoDBObject) as mongoDB:
            try:
                mongoDB[databaseName].create_collection(Conf().getSuggestionDataCollectionName())
                LOGGER.info ("MongoDB Collection [{}] Created".format(Conf().getSuggestionDataCollectionName()))
            except:
                LOGGER.info ("MongoDB Collection [{}] Not Created".format(Conf().getSuggestionDataCollectionName()))
                pass

            try:
                mongoDB[databaseName][Conf().getSuggestionDataCollectionName()].insert({"_id":0,"suggestionID":0,"userID":0,"status":"FALSE","suggestionList":[1,2,3,4,5]})
                LOGGER.info ("MongoDB Collection [{}] initial insert".format(Conf().getSuggestionDataCollectionName()))
            except:
                LOGGER.info ("MongoDB Collection [{}] initial insert Failed".format(Conf().getSuggestionDataCollectionName()))
                pass

            try:
                mongoDB[databaseName][Conf().getSuggestionDataCollectionName()].ensure_index('_id', unique=True)
                LOGGER.info ("MongoDB Collection [{}] is indexed on _id".format(Conf().getSuggestionDataCollectionName()))
            except:
                LOGGER.info ("Failed to Create Index on _id in MongoDB Collection [{}]".format(Conf().getSuggestionDataCollectionName()))
                pass

    def initSuggestionHistoryMongoDB(self,mongoDBObject,databaseName):
        '''
        Create Suggestion History MongoDB Collection for Recommandation Models
        '''
        with closing(mongoDBObject) as mongoDB:
            try:
                mongoDB[databaseName].create_collection(Conf().getSuggestionHistoryCollectionName())
                LOGGER.info ("MongoDB Collection [{}] Created".format(Conf().getSuggestionHistoryCollectionName()))
            except:
                LOGGER.info ("MongoDB Collection [{}] Not Created".format(Conf().getSuggestionHistoryCollectionName()))
                pass

            try:
                mongoDB[databaseName][Conf().getSuggestionHistoryCollectionName()].insert({"_id":0,"suggestionID":0,"userID":0,"status":"FALSE","date":datetime.utcnow(),"suggestionList":[1,2,3,4,5]})
                LOGGER.info ("MongoDB Collection [{}] initial insert".format(Conf().getSuggestionHistoryCollectionName()))
            except:
                LOGGER.info ("MongoDB Collection [{}] initial insert Failed".format(Conf().getSuggestionHistoryCollectionName()))
                pass

            try:
                mongoDB[databaseName][Conf().getSuggestionHistoryCollectionName()].ensure_index('_id', unique=True)
                LOGGER.info ("MongoDB Collection [{}] is indexed on _id".format(Conf().getSuggestionHistoryCollectionName()))
            except:
                LOGGER.info ("Failed to Create Index on _id in MongoDB Collection [{}]".format(Conf().getSuggestionHistoryCollectionName()))
                pass

    def initUpdateDataMongoDB(self,mongoDBObject,databaseName):
        '''
        Create Update Data MongoDB Collection for Recommandation Models
        '''
        with closing(mongoDBObject) as mongoDB:
            try:
                mongoDB[databaseName].create_collection(Conf().getUserDataCollectionName())
                LOGGER.info ("MongoDB Collection [{}] Created".format(Conf().getUserDataCollectionName()))
            except:
                LOGGER.info ("MongoDB Collection [{}] Not Created".format(Conf().getUserDataCollectionName()))
                pass

            try:
                mongoDB[databaseName][Conf().getUserDataCollectionName()].insert({"_id":0,"userID":0,"productID":0,"categoryID":0,"status":"FALSE","type":"REMOVE","date":datetime.utcnow(),"modelType":"Reduced","bascketType":"Reduced","suggestionType":"Reduced","suggestionID":0,"score":0,"weight":0,"strength":0})
                LOGGER.info ("MongoDB Collection [{}] initial insert".format(Conf().getUserDataCollectionName()))
            except:
                LOGGER.info ("MongoDB Collection [{}] initial insert Failed".format(Conf().getUserDataCollectionName()))
                pass

            try:
                mongoDB[databaseName][Conf().getUserDataCollectionName()].ensure_index('_id', unique=True)
                LOGGER.info ("MongoDB Collection [{}] is indexed on _id".format(Conf().getUserDataCollectionName()))
            except:
                LOGGER.info ("Failed to check Index on _id in MongoDB Collection [{}]".format(Conf().getUserDataCollectionName()))
                pass