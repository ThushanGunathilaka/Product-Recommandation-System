import logging
from contextlib import closing
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger("PRS Input")
from PRSBoot.PRSConfig import Conf
#LOGGER.propagate = Conf().getVerbose()

# file handler
handler = logging.FileHandler('PRS.log')
handler.setLevel(logging.INFO)
# logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

LOGGER.addHandler(handler)
from PRSHandler.PRSHandlerConfig.PRSConfig import Config
from PRSHandler.PRSSuggestionManager.PRSValidateInput.PRSConvert import Convert
class Inputs(object):
    ''' Manage PRS Inputs '''
    item = None
    config = None
    convert = None
    mongoDB = None
    mongoDBdatabaseName = None
    userID = None

    def __init__(self,mongoDB,mongoDBdatabaseName,userID):
        '''
        Initializes PRS Inputs
        '''
        self.config = Config()
        self.convert = Convert()
        self.mongoDB = mongoDB
        self.mongoDBdatabaseName = mongoDBdatabaseName
        self.userID = userID
        item = {}
        
    def processInputs(self):
        '''
        User History Data
        '''
        start = datetime.now()
        end = datetime.now()
        # (1) Current Suggestions
        if self.convert.binaryToBool(self.config.allowCurrentSuggestions()):
            start = datetime.now()
            self.useCurrentSuggestions();
            end = datetime.now()
            elapsed = end-start
            LOGGER.info('Current Suggestions Elapsed : {} #(minutes, seconds)'.format(divmod(elapsed.days*86400+elapsed.seconds,60)))
        # (2) Previous Suggestions
        if self.convert.binaryToBool(self.config.allowPreviousSuggestions()):
            start = datetime.now()
            self.oldSuggestionsFromDate = self.config.getOldSuggestionsFromDate()
            self.oldSuggestionsToDate = self.config.getOldSuggestionsToDate()
            self.usePreviousSuggestions(self.oldSuggestionsFromDate,self.oldSuggestionsToDate)
            end = datetime.now()
            elapsed = end-start
            LOGGER.info('Previous Suggestions Elapsed : {} #(minutes, seconds)'.format(divmod(elapsed.days*86400+elapsed.seconds,60)))
        # (7) Liked Products
        if self.convert.binaryToBool(self.config.allowLikedProducts()):
            start = datetime.now()
            self.likedProducts = self.userFeed.getUserFeedLikedProducts()
            end = datetime.now()
            elapsed = end-start
            LOGGER.info('Liked Products Elapsed : {} #(minutes, seconds)'.format(divmod(elapsed.days*86400+elapsed.seconds,60)))
        # (8) Disliked Products
        if self.convert.binaryToBool(self.config.allowDisLikedProducts()):
            start = datetime.now()
            self.disLikedProducts = self.userFeed.getUserFeedDisLikedProducts()
            end = datetime.now()
            elapsed = end-start
            LOGGER.info('Disliked Products Elapsed : {} #(minutes, seconds)'.format(divmod(elapsed.days*86400+elapsed.seconds,60)))
        # (9) Commented Products
        if self.convert.binaryToBool(self.config.allowCommentedProducts()):
            start = datetime.now()
            self.commentedProducts = self.userFeed.getUserFeedCommentedProducts()
            end = datetime.now()
            elapsed = end-start
            LOGGER.info('Commented Products Elapsed : {} #(minutes, seconds)'.format(divmod(elapsed.days*86400+elapsed.seconds,60)))
        # (10) Cart Added Products
        if self.convert.binaryToBool(self.config.allowCartAddedProducts()):
            start = datetime.now()
            self.cartAddedProducts = self.userFeed.getUserFeedCartAddedProducts()
            end = datetime.now()
            elapsed = end-start
            LOGGER.info('Cart Added Products Elapsed : {} #(minutes, seconds)'.format(divmod(elapsed.days*86400+elapsed.seconds,60)))
        # (11) Cart Removed Products
        if self.convert.binaryToBool(self.config.allowCartRemovedProducts()):
            start = datetime.now()
            self.cartRemovedProducts = self.userFeed.getUserFeedCartRemovedProducts()
            end = datetime.now()
            elapsed = end-start
            LOGGER.info('Cart Removed Products Elapsed : {} #(minutes, seconds)'.format(divmod(elapsed.days*86400+elapsed.seconds,60)))
        # (12) Wishlist Added Products
        if self.convert.binaryToBool(self.config.allowWishListAddedProducts()):
            start = datetime.now()
            self.wishListAddedProducts = self.userFeed.getUserFeedWishListAddedProducts()
            end = datetime.now()
            elapsed = end-start
            LOGGER.info('Wishlist Added Products Elapsed : {} #(minutes, seconds)'.format(divmod(elapsed.days*86400+elapsed.seconds,60)))
        # (13) Wishlist Removed Products
        if self.convert.binaryToBool(self.config.allowWishListRemovedProducts()):
            start = datetime.now()
            self.wishListRemovedProducts = self.userFeed.getUserFeedWishListRemovedProducts()
            end = datetime.now()
            elapsed = end-start
            LOGGER.info('Wishlist Removed Products Elapsed : {} #(minutes, seconds)'.format(divmod(elapsed.days*86400+elapsed.seconds,60)))

    ## (1) Current Suggestions
    #currentSuggestions = []
    #currentSuggestionStatus = False
    ## (2) Previous Suggestions
    #oldSuggestionsFromDate = None
    #oldSuggestionsToDate = None
    #previousSuggestions = []

    #def reuirementCheck(self):
    #    check = False
    #    check = self.numToBool(self.config.allowWishListRemovedProducts())
    #    check = self.numToBool(self.config.allowWishListAddedProducts())
    #    check = self.numToBool(self.config.allowCartRemovedProducts())
    #    check = self.numToBool(self.config.allowCartAddedProducts())
    #    check = self.numToBool(self.config.allowCommentedProducts())
    #    check = self.numToBool(self.config.allowDisLikedProducts())
    #    check = self.numToBool(self.config.allowLikedProducts())
    #    return check