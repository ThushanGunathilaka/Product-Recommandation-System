from contextlib import closing
from datetime import datetime
import logging

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger("Query From MongoDB Database")
from PRSBoot.PRSConfig import Conf
LOGGER.propagate = Conf().getVerbose()

# file handler
handler = logging.FileHandler('PRS.log')
handler.setLevel(logging.INFO)
# logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

LOGGER.addHandler(handler)

class QueryMongoDB(object):
    '''pymongo related queries'''

    def checkMongoDBTableExists(self,mongoDBObject,database, colleactionName):
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
