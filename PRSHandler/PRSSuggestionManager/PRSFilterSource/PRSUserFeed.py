from contextlib import closing
import logging

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger("User Feed")
from PRSBoot.PRSConfig import Conf
LOGGER.propagate = Conf().getVerbose()

# file handler
handler = logging.FileHandler('PRS.log')
handler.setLevel(logging.INFO)
# logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

LOGGER.addHandler(handler)

class UserFeed(object):
    '''
    Get User Liked, Disliked and commented products
    '''
    mongoDB = None
    mongoDBdatabaseName = None
    fromDate = None
    toDate = None

    def __init__(self,mongoDB,mongoDBdatabaseName,fromDate,toDate,sanityCheck):
        '''
        Initializes the user feed with mysql and mongodb
        '''
        self.mongoDB = mongoDB
        self.mongoDBdatabaseName = mongoDBdatabaseName
        self.fromDate = fromDate
        self.toDate = toDate

        if sanityCheck:
            mongoHistory = []
            likesHistory = []
            commentsHistory = []
            with closing(mongoDB) as currentCursor:
                try:
                    LOGGER.info ("User Feed MongoDB Fetch Success")
                except:
                    LOGGER.info ("User Feed MongoDB Fetch Failed")

            #create connection
            #with closing(mySQLCursor) as currentCursor:
            #    try:
            #        LOGGER.info ("User Feed MySQL Fetch Success")
            #    except:
            #        LOGGER.info ("User Feed MySQL Fetch Failed")

    def getUserFeedLikedProducts(self):
        return [1,2,3,4,5]

    def getUserFeedDisLikedProducts(self):
        return [1,2,3,4,5]

    def getUserFeedCommentedProducts(self):
        return [1,2,3,4,5]

    def getUserFeedCartAddedProducts(self):
        return [1,2,3,4,5]

    def getUserFeedCartRemovedProducts(self):
        return [1,2,3,4,5]

    def getUserFeedWishListAddedProducts(self):
        return [1,2,3,4,5]

    def getUserFeedWishListRemovedProducts(self):
        return [1,2,3,4,5]

    def usePreviousSuggestions(self,fromDate,toDate):
        previousSuggestionSet = []
        with closing(self.requestData.getMongoDB()) as previousCursor:
            try:
                if fromDate == None and toDate == None:
                    previousSuggestionSet = list(previousCursor[self.requestData.getMongoDBdatabaseName()]['SuggestionHistory'].find({'userID': int(self.requestData.getUserID())}))
                elif fromDate != None and toDate == None:
                    previousSuggestionSet = list(previousCursor[self.requestData.getMongoDBdatabaseName()]['SuggestionHistory'].find({'userID': int(self.requestData.getUserID()),'date':{'$gte':fromDate}}))
                elif fromDate == None and toDate != None:
                    previousSuggestionSet = list(previousCursor[self.requestData.getMongoDBdatabaseName()]['SuggestionHistory'].find({'userID': int(self.requestData.getUserID()),'date':{'$lt':toDate}}))
                elif fromDate != None and toDate != None:
                    previousSuggestionSet = list(previousCursor[self.requestData.getMongoDBdatabaseName()]['SuggestionHistory'].find({'userID': int(self.requestData.getUserID()),'date':{'$gte':fromDate,'$lt':toDate}}))
            except:
                pass
        self.previousSuggestions = []
        for suggestionSet in previousSuggestionSet:
            self.previousSuggestions.extend(suggestionSet['suggestionList'])
        self.previousSuggestions = list(set(self.previousSuggestions))

    #def useCurrentSuggestions(self):
    #    currentSuggestionSet = []
    #    currentSuggestions = []
    #    with closing(self.mongoDB) as currentCursor:
    #        try:
    #            currentSuggestionSet = list(currentCursor[self.mongoDBdatabaseName]['SuggestionData'].find({'userID': int(self.userID)}))
    #        except:
    #            pass
    #    if currentSuggestionSet is not None and len(currentSuggestionSet)>0:
    #        for suggestionSet in currentSuggestionSet:
    #            currentSuggestions.extend(suggestionSet['suggestionList'])
    #        currentSuggestions = list(set(currentSuggestions))
    #    else:
    #        currentSuggestions = None
    #    LOGGER.info (' Current Suggestions : {}'.format(currentSuggestions))
    #    return currentSuggestions

    #def usePreviousSuggestions(self,fromDate,toDate):
    #    previousSuggestionSet = []
    #    with closing(self.requestData.getMongoDB()) as previousCursor:
    #        try:
    #            if fromDate == None and toDate == None:
    #                previousSuggestionSet = list(previousCursor[self.requestData.getMongoDBdatabaseName()]['SuggestionHistory'].find({'userID': int(self.requestData.getUserID())}))
    #            elif fromDate != None and toDate == None:
    #                previousSuggestionSet = list(previousCursor[self.requestData.getMongoDBdatabaseName()]['SuggestionHistory'].find({'userID': int(self.requestData.getUserID()),'date':{'$gte':fromDate}}))
    #            elif fromDate == None and toDate != None:
    #                previousSuggestionSet = list(previousCursor[self.requestData.getMongoDBdatabaseName()]['SuggestionHistory'].find({'userID': int(self.requestData.getUserID()),'date':{'$lt':toDate}}))
    #            elif fromDate != None and toDate != None:
    #                previousSuggestionSet = list(previousCursor[self.requestData.getMongoDBdatabaseName()]['SuggestionHistory'].find({'userID': int(self.requestData.getUserID()),'date':{'$gte':fromDate,'$lt':toDate}}))
    #        except:
    #            pass
    #    self.previousSuggestions = []
    #    for suggestionSet in previousSuggestionSet:
    #        self.previousSuggestions.extend(suggestionSet['suggestionList'])
    #    self.previousSuggestions = list(set(self.previousSuggestions))
