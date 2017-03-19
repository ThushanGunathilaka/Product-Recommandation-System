import tornado
from bson.objectid import ObjectId
from bson.json_util import dumps, loads
from slugify import slugify
#import pymysql
from datetime import datetime
from PRSHandler.PRSSuggestionManager.PRSSuggestionManager import Manager
from PRSHandler.PRSSuggestionManager.PRSRequestModel.PRSRequestData import RequestData
from PRSHandler.PRSHandlerAuthorize.PRSValidateUser import ValidateUser
from PRSHandler.PRSHandlerConfig.PRSConfig import Config
from PRSHandler.PRSSuggestionManager.PRSValidateInput.PRSConvert import Convert
import logging

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger("Suggestion Handler")
from PRSBoot.PRSConfig import Conf
#LOGGER.propagate = Conf().getVerbose()

# file handler
handler = logging.FileHandler('PRS.log')
handler.setLevel(logging.INFO)
# logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

LOGGER.addHandler(handler)

class SuggestionHandler(tornado.web.RequestHandler):
    '''
    To Provide Client Data [Suggestions]
    '''
    mongoDB = None
    mongoDBdatabaseName = None
    userID = -1
    requestedSuggestionCount = -1
    password = None
    currentSuggestions = [-1]
    currentWishlist = [-1]
    currentCart = [-1]
    requestedCategories = [-1]

    manager = None
    config = None
    convert = None

    def initialize(self, db):
        """
        Initializes the instance with a MongoDB and MySQL
        :param dbData: database objects
        """
        self.mongoDB = db[0]
        self.mongoDBdatabaseName = db[1]
        
        self.manager = Manager()
        self.config = Config()
        self.convert = Convert()

    def get(self):
        """
        Return suggestion list
        """
        self.userID = self.get_argument('userID', -1)
        self.password = self.get_argument('password', None)
        self.requestedSuggestionCount = self.get_argument('requestedSuggestionCount', -1)
        self.currentSuggestions = self.get_arguments('currentSuggestionItemID', strip=True)
        self.currentWishlist = self.get_arguments('currentWishlistItemID', strip=True)
        self.currentCart = self.get_arguments('currentCartItemID', strip=True)
        self.requestedCategories = self.get_arguments('requestedCategoryID', strip=True)


        if self.validateRequest():
            try:
                response = {}
                response = self.manager.generateResponse(self.prepareRequestData())
                if response != None:
                    response['status'] = 'TRUE'
                    LOGGER.info ('||||||||||Success||||||||||Suggestions Request Updated')
                    self.write(dumps(response))
                else:
                    LOGGER.warn ('||||||||||Error||||||||||Failed To Validate Suggestions Request')
                    self.write(dumps({'status':'FALSE'}))
            except Exception as e:
                print(e)
                LOGGER.warn ('||||||||||Error||||||||||Failed To Complete Suggestions Request')
                self.write(dumps({'status':'FALSE'}))
        else:
            LOGGER.info ('||||||||||Error||||||||||Invalid Suggestions Request')
            self.write(dumps({'status':'FALSE'}))

    def validateRequest(self):
        '''
        Validate The Request
        '''
        userIDState = False
        requestedSuggestionCountState = False
        passwordState = False

        try:
            self.userID = int(self.userID)
            self.requestedSuggestionCount = int(self.requestedSuggestionCount)
            self.currentSuggestions = self.convert.listToIntList(self.currentSuggestions)
            self.currentWishlist = self.convert.listToIntList(self.currentWishlist)
            self.currentCart = self.convert.listToIntList(self.currentCart)
            self.requestedCategories = self.convert.listToIntList(self.requestedCategories)
        except:
            return False

        if self.userID >=0:
            userIDState = True
        if self.requestedSuggestionCount >0:
            requestedSuggestionCountState = True
        if userIDState and self.password!=None and self.password.strip()!='' and self.validateUser(self.userID,self.password):
            passwordState = True
        return userIDState and passwordState and requestedSuggestionCountState

    def validateUser(self,userID,password):
        if self.config.getValidateUsersWithDatabase():
            return ValidateUser().validateUser(userID,password)
        else:
            return True

    def prepareRequestData(self):
        requestData = RequestData()
        requestData.setConfig(self.config)
        requestData.setMongoDB(self.mongoDB)
        requestData.setMongoDBdatabaseName(self.mongoDBdatabaseName)
        requestData.setUserID(self.userID)

        # (14) Suggestions From Request (Before Save)
        if self.convert.binaryToBool(self.config.allowRequestSuggestion()):
            start = datetime.now()
            requestData.setCurrentSuggestions(self.currentSuggestions)
            end = datetime.now()
            elapsed = end-start
            LOGGER.info(' Suggestions From Request Elapsed : {} #(minutes, seconds)'.format(divmod(elapsed.days*86400+elapsed.seconds,60)))
        else:
            requestData.setCurrentSuggestions(None)
            LOGGER.info(' Suggestions From Request Not Allowed')

        # (15) Cart From Request (Before Save)
        if self.convert.binaryToBool(self.config.allowRequestCart()):
            start = datetime.now()
            requestData.setCurrentCart(self.currentCart)
            end = datetime.now()
            elapsed = end-start
            LOGGER.info(' Cart From Request Elapsed : {} #(minutes, seconds)'.format(divmod(elapsed.days*86400+elapsed.seconds,60)))
        else:
            requestData.setCurrentCart(None)
            LOGGER.info(' Cart From Request Not Allowed')

        # (16) WishList From Request (Before Save)
        if self.convert.binaryToBool(self.config.allowRequestWishList()):
            start = datetime.now()
            requestData.setCurrentWishlist(self.currentWishlist)
            end = datetime.now()
            elapsed = end-start
            LOGGER.info(' WishList From Request Elapsed : {} #(minutes, seconds)'.format(divmod(elapsed.days*86400+elapsed.seconds,60)))
        else:
            requestData.setCurrentWishlist(None)
            LOGGER.info(' WishList From Request Not Allowed')

        # (17) Requested Categories
        if self.convert.binaryToBool(self.config.allowRequestedCategories()):
            start = datetime.now()
            requestData.setRequestedCategories(self.requestedCategories)
            end = datetime.now()
            elapsed = end-start
            LOGGER.info(' Requested Categories From Request Elapsed : {} #(minutes, seconds)'.format(divmod(elapsed.days*86400+elapsed.seconds,60)))
        else:
            requestData.setRequestedCategories(None)
            LOGGER.info(' Requested Categories From Request Not Allowed')

        # (18) Requested Number of Suggestions
        if self.convert.binaryToBool(self.config.allowRequestedSuggestionCount()):
            start = datetime.now()
            requestData.setRequestedSuggestionCount(self.requestedSuggestionCount)
            end = datetime.now()
            elapsed = end-start
            LOGGER.info(' Requested Number of Suggestions From Request Elapsed : {} #(minutes, seconds)'.format(divmod(elapsed.days*86400+elapsed.seconds,60)))
        else:
            requestData.setRequestedSuggestionCount(None)
            LOGGER.info(' Number of Suggestions From Request Not Allowed')
        return requestData
