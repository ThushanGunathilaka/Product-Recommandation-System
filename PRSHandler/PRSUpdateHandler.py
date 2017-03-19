import tornado
from bson.objectid import ObjectId
from bson.json_util import dumps, loads
from slugify import slugify
from datetime import datetime
from PRSHandler.PRSHandlerAuthorize.PRSValidateUser import ValidateUser
from PRSHandler.PRSHandlerConfig.PRSConfig import Config
from contextlib import closing
import logging

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger("Update Handler")
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
class UpdateHandler(tornado.web.RequestHandler):
    '''
    To Store Client Data
    '''
    userID = -1
    productID = -1
    categoryID = -1
    suggestionID = -1

    password = None
    status = None
    type = None
    modelType = None
    bascketType = None
    suggestionType = None

    #status			[TRUE | FALSE]
    #type			[ADD | REMOVE]
    #modelType		[RANDOM | WITHGLOBAL | WITHOUTGLOBAL | REDUCED]
    #bascketType	[WISHLIST | CART | LIKE | VIEW | COMMENT | REDUCED]
    #suggestionType	[PRESONAL | SOCIAL | GLOBAL | REDUCED]

    score = None
    weight = None
    strength = None

    mongoDB = None
    mongoDBdatabaseName = None

    config = None

    def initialize(self, db):
        '''
        Initializes the instance with a mongodb instance
        :param dbData: an instance to pymongo database object
        '''
        self.mongoDB = db[0]
        self.mongoDBdatabaseName = db[1]
        self.config = Config()

    def get(self):
        '''
        Collect Validation Data
        '''
        self.userID = self.get_argument('userID', -1)
        self.productID = self.get_argument('productID', -1)
        self.categoryID = self.get_argument('categoryID', -1)
        self.suggestionID = self.get_argument('suggestionID', -1)

        self.password = self.get_argument('password', None)
        self.status = self.get_argument('status', None)
        self.type = self.get_argument('type', None)
        self.modelType = self.get_argument('modelType', None)
        self.bascketType = self.get_argument('bascketType', None)
        self.suggestionType = self.get_argument('suggestionType', None)

        self.score = self.get_argument('score', -1)
        self.weight = self.get_argument('weight', -1)
        self.strength = self.get_argument('strength', -1)

        LOGGER.info ('--------------------------------------------------------------------------------')
        if self.validateRequest():
            updateData = {}
            updateData["userID"] = self.userID
            updateData["productID"] = self.productID
            updateData["categoryID"] = self.categoryID

            updateData["status"] = self.status
            updateData["type"] = self.type
            updateData["date"] = datetime.utcnow()

            updateData["modelType"] = self.modelType
            updateData["bascketType"] = self.bascketType
            updateData["suggestionType"] = self.suggestionType
            updateData["suggestionID"] = self.suggestionID

            updateData["score"] = self.score
            updateData["weight"] = self.weight
            updateData["strength"] = self.strength

            try:
                storeCurrentSuggestions = Conf().getStoreOldSuggestions()
                result = DataAccess().storeUpdateRequest(self.mongoDB,self.mongoDBdatabaseName,updateData,storeCurrentSuggestions)
                if result is not None and result:
                    LOGGER.info ('--------------------------------------------------------------------------------')
                    LOGGER.info ('||||||||||Success|||||||||| Suggestions Request Updated')
                    self.write(dumps({'status':'TRUE'}))
                else:
                    LOGGER.info ('--------------------------------------------------------------------------------')
                    LOGGER.warn ('||||||||||Error|||||||||| Collection Not Found to Store Update Suggestions')
                    self.write(dumps({'status':'FALSE'}))
            except Exception as e:
                LOGGER.warn (e)
                LOGGER.info ('--------------------------------------------------------------------------------')
                LOGGER.warn ('||||||||||Error|||||||||| Failed To Store Suggestions Request')
                self.write(dumps({'status':'FALSE'}))
        else:
            LOGGER.info ('--------------------------------------------------------------------------------')
            LOGGER.info ('||||||||||Error|||||||||| Invalid Update Suggestions Request')
            self.write(dumps({'status':'FALSE'}))
        LOGGER.info ('--------------------------------------------------------------------------------')

    def validateRequest(self):
        '''
        Validate The Request
        '''
        userIDState = False
        productIDState = False
        categoryIDState = False
        suggestionIDState = False

        passwordState = False
        statusState = False
        typeState = False
        modelTypeState = False
        bascketTypeState = False
        suggestionTypeState = False

        try:
            self.userID = int(self.userID)
            self.productID = int(self.productID)
            self.categoryID = int(self.categoryID)
            self.suggestionID = int(self.suggestionID)
        except:
            return False

        if self.userID >= 0:
            userIDState = True
        if self.productID >= 0:
            productIDState = True
        if self.categoryID >= 0:
            categoryIDState = True
        if self.suggestionID >= 0:
            suggestionIDState = True

        if userIDState and self.password!=None and self.password.strip()!='' and self.validateUser(self.userID,self.password):
            passwordState = True
        if self.status=='TRUE' or self.status=='FALSE':
            statusState = True
        if self.type=='ADD' or self.type=='REMOVE':
            typeState = True
        if self.modelType=='RANDOM' or self.modelType=='WITHGLOBAL' or self.modelType=='WITHOUTGLOBAL' or self.modelType=='REDUCED':
            modelTypeState = True
        if self.bascketType=='WISHLIST' or self.bascketType=='CART' or self.bascketType=='COMMENT' or self.bascketType=='VIEW' or self.bascketType=='LIKE' or self.bascketType=='REDUCED':
            bascketTypeState = True
        if self.suggestionType=='PERSONAL' or self.suggestionType=='SOCIAL' or self.suggestionType=='GLOBAL' or self.suggestionType=='REDUCED':
            suggestionTypeState = True

        return userIDState and passwordState and productIDState and categoryIDState and suggestionIDState and statusState and typeState and modelTypeState and bascketTypeState and suggestionTypeState

    def validateUser(self,userID,password):
        if self.config.getValidateUsersWithDatabase():
            return ValidateUser().validateUser(userID,password)
        else:
            return True