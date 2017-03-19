import logging

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger("Request Model")
from PRSBoot.PRSConfig import Conf
#LOGGER.propagate = Conf().getVerbose()

# file handler
handler = logging.FileHandler('PRS.log')
handler.setLevel(logging.INFO)
# logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

LOGGER.addHandler(handler)
from PRSHandler.PRSDataAccess.PRSDataAccess import DataAccess
class RequestData(object):
    '''
    Data from the Suggestion Request
    '''
    userID = -1
    requestedSuggestionCount = -1
    currentSuggestions = []
    currentWishlist = []
    currentCart = []
    requestedCategories = []
    mongoDB = None
    mongoDBdatabaseName = None
    config = None

    def setConfig(self,config):
        self.config = config

    def setUserID(self,userID):
        self.userID = userID
        LOGGER.info('UserID : {}'.format(self.userID))

    def setRequestedSuggestionCount(self,requestedSuggestionCount):
        self.requestedSuggestionCount = requestedSuggestionCount
        LOGGER.info('Required Suggestion Count : {}'.format(self.requestedSuggestionCount))

    def setCurrentSuggestions(self,currentSuggestions):
        LOGGER.info(' Current Suggestions From Request : {}'.format(currentSuggestions))
        if currentSuggestions is not None:
            if self.config.getValidateProductsWithDatabase():
                availableList = DataAccess().checkProductsInTable(currentSuggestions)
                self.currentSuggestions = availableList
            else:
                self.currentSuggestions = currentSuggestions
            LOGGER.info(' Current Suggestions Validate And Check Availability of Products : {}'.format(self.config.getValidateProductsWithDatabase()))
            LOGGER.info(' Current Suggestions Selected : {}'.format(self.currentSuggestions))
       
    def setCurrentWishlist(self,currentWishlist):
        LOGGER.info(' Current Wishlist From Request : {}'.format(currentWishlist))
        if currentWishlist is not None:
            if self.config.getValidateProductsWithDatabase():
                availableList = DataAccess().checkProductsInTable(currentWishlist)
                self.currentWishlist = availableList
            else:
                self.currentWishlist = currentWishlist
            LOGGER.info(' Current Wishlist Validate And Check Availability of Products : {}'.format(self.config.getValidateProductsWithDatabase()))
            LOGGER.info(' Current Wishlist Selected : {}'.format(self.currentSuggestions))

    def setCurrentCart(self,currentCart):
        LOGGER.info(' Current Cart From Request : {}'.format(currentCart))
        if currentCart is not None:
            if self.config.getValidateProductsWithDatabase():
                availableList = DataAccess().checkProductsInTable(currentCart)
                self.currentCart = availableList
            else:
                self.currentCart = currentCart
            LOGGER.info(' Current Cart Validate And Check Availability of Products : {}'.format(self.config.getValidateProductsWithDatabase()))
            LOGGER.info(' Current Cart Selected : {}'.format(self.currentSuggestions))

    def setRequestedCategories(self,requestedCategories):
        LOGGER.info(' Requested Categories : {}'.format(requestedCategories))
        if requestedCategories is not None:
            if self.config.getValidateCategoryWithDatabase():
                availableList = DataAccess().checkCategoriesInTable(requestedCategories)
                self.requestedCategories = availableList
            else:
                self.requestedCategories = requestedCategories
            LOGGER.info(' Requested Categories Validate And Check Availability of Categories : {}'.format(self.config.getValidateProductsWithDatabase()))
            LOGGER.info(' Requested Categories Selected : {}'.format(self.requestedCategories))

    def setMongoDB(self,mongoDB):
        self.mongoDB = mongoDB

    def setMongoDBdatabaseName(self,mongoDBdatabaseName):
        self.mongoDBdatabaseName = mongoDBdatabaseName

    def getUserID(self):
        return self.userID

    def getRequestedSuggestionCount(self):
        return self.requestedSuggestionCount

    def getCurrentSuggestions(self):
        return self.currentSuggestions

    def getCurrentWishlist(self):
        return self.currentWishlist

    def getCurrentCart(self):
        return self.currentCart

    def getRequestedCategories(self):
        return self.requestedCategories

    def getMongoDB(self):
        return self.mongoDB

    def getMongoDBdatabaseName(self):
        return self.mongoDBdatabaseName