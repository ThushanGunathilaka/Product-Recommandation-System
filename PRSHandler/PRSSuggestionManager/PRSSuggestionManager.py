#from PRSManager import Manager
from PRSHandler.PRSSuggestionManager.PRSSuggestionEngine.PRSPrediction import Prediction
#from datetime import datetime
from contextlib import closing
import logging
from datetime import datetime

from PRSHandler.PRSSuggestionManager.PRSValidateInput.PRSValidate import Validate
from PRSHandler.PRSSuggestionManager.PRSValidateInput.PRSConvert import Convert
from PRSHandler.PRSHandlerConfig.PRSConfig import Config
from PRSHandler.PRSSuggestionManager.PRSSuggestionSource.PRSGlobalSuggestion import GlobalSuggestion
from PRSHandler.PRSSuggestionManager.PRSSuggestionSource.PRSPersonalSuggestion import PersonalSuggestion
from PRSHandler.PRSSuggestionManager.PRSGeneratedSource.PRSSocialSuggestions import SocialSuggestions
from PRSHandler.PRSSuggestionManager.PRSUserSource.PRSFriendList import FriendList
from PRSHandler.PRSSuggestionManager.PRSFilterSource.PRSUserFeed import UserFeed
from PRSHandler.PRSSuggestionManager.PRSRequestModel.PRSRequestData import RequestData
from PRSHandler.PRSSuggestionManager.PRSSuggestionEngine.PRSCollect import Collect
from PRSHandler.PRSSuggestionManager.PRSPrepareResponse.PRSResponseModel import ResponseModel
logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger("Suggestion Handler Manager")
from PRSBoot.PRSConfig import Conf
LOGGER.propagate = Conf().getVerbose()

# file handler
handler = logging.FileHandler('PRS.log')
handler.setLevel(logging.INFO)
# logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

LOGGER.addHandler(handler)

class Manager(object):
    requestData = None
    convert = None
    config = None
    userFeed = None
    userFeedFromDate = None
    userFeedToDate = None
    friendsLimitPerCategory = -1
    personalSuggestionLimit = -1
    socialSuggestionLimit = -1
    globalSuggestionLimit = -1
    # (5) Friend List
    friendList = None
 

    def generateResponse(self,requestData):
        self.requestData = requestData
        #self.userFeed = UserFeed(self.requestData.getMongoDB(),self.requestData.getMongoDBdatabaseName(),self.userFeedFromDate,self.userFeedToDate,self.reuirementCheck())
        #INPUT
        source = self.processInputSources()
        collect = Collect(source)
        meanPoints = collect.getMeanPoints()
        gridProducts = collect.getFixedInputs()
        model = Prediction(int(self.requestData.getUserID()),int(self.requestData.getRequestedSuggestionCount()),gridProducts,meanPoints) #(id,count,products,pickers)
        suggestions = model.run_model()
        outputList = []
        for item in gridProducts:
            if item['gridID'] in suggestions:
                outputList.append(item)
        for item in outputList:
            item.update({'modelType': 'WITHGLOBAL'})
            item.update({'suggestionID': 0})
        result = ResponseModel().applyResponseAttributes(self.requestData.getUserID(),outputList)
        return {'status':'TRUE','suggestionList':result}

    def processInputSources(self):
        convert = Convert()
        self.config = Config()
        start = datetime.now()
        end = datetime.now()
        item = {}
        self.friendsLimitPerCategory = self.config.getFriendSuggestionsPerCategoryCount()
        self.personalSuggestionLimit = self.config.getPersonalSuggestionCount()
        self.socialSuggestionLimit = self.config.getSocialSuggestionCount()
        self.globalSuggestionLimit = self.config.getGlobalSuggestionCount()
        self.userFeedFromDate = self.config.getUserFeedFromDate()
        self.userFeedToDate = self.config.getUserFeedToDate()
        LOGGER.info('Friend List Limit {}'.format(self.friendsLimitPerCategory))
        LOGGER.info('Personal Suggestion List Limit {}'.format(self.personalSuggestionLimit))
        LOGGER.info('Social Suggestion List Limit {}'.format(self.socialSuggestionLimit))
        LOGGER.info('Global Suggestion List Limit {}'.format(self.globalSuggestionLimit))
        LOGGER.info('User Feed Start From {}'.format(self.userFeedFromDate))
        LOGGER.info('User Feed End In {}'.format(self.userFeedToDate))

        if self.requestData is not None and len(self.requestData.getRequestedCategories())>0:
            item.update({'categories': self.requestData.getRequestedCategories()})
        else:
            item.update({'categories': [1,2,3,4,5,6,7,8]})

        # (3) Global Suggestions
        if convert.binaryToBool(self.config.allowGlobalSuggestion()):
            start = datetime.now()
            item.update({'GLOBAL': self.useGlobalSuggestions()})
            end = datetime.now()
            elapsed = end-start
            LOGGER.info('Global Suggestions Elapsed : {} #(minutes, seconds)'.format(divmod(elapsed.days*86400+elapsed.seconds,60)))
        # (4) Personal Suggestion
        if convert.binaryToBool(self.config.allowPersonalSuggestion()):
            start = datetime.now()
            item.update({'PERSONAL': self.usePersonalSuggestions()})
            end = datetime.now()
            elapsed = end-start
            LOGGER.info('Personal Suggestions Elapsed : {} #(minutes, seconds)'.format(divmod(elapsed.days*86400+elapsed.seconds,60)))
        # (5) Friend List
        if convert.binaryToBool(self.config.allowFriendList()):
            start = datetime.now()
            self.friendList = self.useFriendList(item['categories'])
            #print(self.friendList)
            end = datetime.now()
            elapsed = end-start
            LOGGER.info('Friend List Elapsed : {} #(minutes, seconds)'.format(divmod(elapsed.days*86400+elapsed.seconds,60)))
        # (6) Social Suggestions
        if convert.binaryToBool(self.config.allowSocialSuggestion()):
            start = datetime.now()
            item.update({'SOCIAL': self.useSocialSuggestions(self.friendList)})
            end = datetime.now()
            elapsed = end-start
            LOGGER.info('Social Suggestions Elapsed : {} #(minutes, seconds)'.format(divmod(elapsed.days*86400+elapsed.seconds,60)))
        return item

    def useFriendList(self,requestedCategoriesSet):
        friendList = {}
        validUserID = Validate().checkValidInt(self.getUserID())
        validCategoryLimit = Validate().checkValidInt(self.friendsLimitPerCategory)
        if requestedCategoriesSet is not None and len(requestedCategoriesSet)>0:
            for categoryID in requestedCategoriesSet:
                if Validate().checkValidInt(categoryID) and validUserID and validCategoryLimit:
                    friendList.update({categoryID: FriendList().getFriendList(self.getUserID(),self.friendsLimitPerCategory,categoryID)})
                else:
                    LOGGER.info ('Rejected Friends Category {}, In User ID : {} With Category Limit {}'.format(categoryID,self.requestData.getUserID(),self.friendsLimitPerCategory))
        LOGGER.info ('Requested Suggestion Category Set : {}'.format(requestedCategoriesSet))
        LOGGER.info ('Requested Number of Friends Per Category : {}'.format(self.friendsLimitPerCategory))
        if bool(friendList):
            return friendList
        else:
            return None

    def useSocialSuggestions(self,friendList):
        validUserID = Validate().checkValidInt(self.getUserID())
        validSocialSuggestionsLimit = Validate().checkValidInt(self.socialSuggestionLimit)
        LOGGER.info ('Social Suggestions Limit : {}'.format(self.socialSuggestionLimit))
        if validUserID and validSocialSuggestionsLimit:
            return SocialSuggestions().getSocialSuggestion(self.socialSuggestionLimit,friendList)
        else:
            return None

    def useGlobalSuggestions(self):
        validUserID = Validate().checkValidInt(self.getUserID())
        validGlobalSuggestionsLimit = Validate().checkValidInt(self.globalSuggestionLimit)
        LOGGER.info ('Global Suggestions Limit : {}'.format(self.globalSuggestionLimit))
        if validUserID and validGlobalSuggestionsLimit:
            return GlobalSuggestion().getGlobalSuggestion(self.getUserID(),self.globalSuggestionLimit)
        else:
            return None


    def usePersonalSuggestions(self):
        validUserID = Validate().checkValidInt(self.getUserID())
        validPersonalSuggestionsLimit = Validate().checkValidInt(self.personalSuggestionLimit)
        LOGGER.info ('Personal Suggestions Limit : {}'.format(self.personalSuggestionLimit))
        if validUserID and validPersonalSuggestionsLimit:
            return PersonalSuggestion().getPersonalSuggestion(self.getUserID(),self.personalSuggestionLimit)
        else:
            return None

    def getUserID(self):
        if self.requestData is not None and self.requestData.getUserID() is not None and self.requestData.getUserID() >=0:
            return self.requestData.getUserID()
        else:
            return 0