from io import StringIO
from configparser import ConfigParser
import os
from datetime import datetime
from PRSBoot.PRSConfig import Conf
import logging

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger("Handler Configuration")
LOGGER.propagate = Conf().getVerbose()

# file handler
handler = logging.FileHandler('PRS.log')
handler.setLevel(logging.INFO)
# logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

LOGGER.addHandler(handler)

class Config(object):
    '''Manage I/O Settings for Product Recommandation System(PRS)'''
    config = None
    preset = None  #[user adjusted preset]
    default = 1

    def __init__(self):
        '''
        Initializes the instance with a configuration file name
        '''
        self.config = ConfigParser()
        self.config.read(Conf().getHandlerConfig())

        if 'DEFAULT' in self.config:
            self.preset = self.config.get('DEFAULT', 'preset', fallback='preset1')
            value = self.config.get('DEFAULT', 'value_default_fallback', fallback='1')
            try:
                self.default = int(value)
            except:
                self.default = 1

    def getValidateProductsWithDatabase(self):
        '''Validate Products With Database'''
        section = self.preset + '.validate'
        if section in self.config:
            count = self.config.get(section, 'validate_products_with_database', fallback=1)
            try:
                count = int(count)
                if count == 1:
                    return True
                else:
                    return False
            except:
                return False
        else:
            return False

    def getValidateCategoryWithDatabase(self):
        '''Validate Categories With Database'''
        section = self.preset + '.validate'
        if section in self.config:
            count = self.config.get(section, 'validate_category_with_database', fallback=1)
            try:
                count = int(count)
                if count == 1:
                    return True
                else:
                    return False
            except:
                return False
        else:
            return False

    def getValidateUsersWithDatabase(self):
        '''Validate Users With Database'''
        section = self.preset + '.validate'
        if section in self.config:
            count = self.config.get(section, 'validate_user_with_database', fallback=1)
            try:
                count = int(count)
                if count == 1:
                    return True
                else:
                    return False
            except:
                return False
        else:
            return False

    def getPersonalSuggestionCount(self):
        '''Return Personal Suggestions Request Count'''
        section = self.preset + '.settings'
        if section in self.config:
            count = self.config.get(section, 'personal_suggestion_count', fallback=10)
            try:
                return int(count)
            except:
                return 10
        else:
            return 10

    def getSocialSuggestionCount(self):
        '''Return Social Suggestions Request Count'''
        section = self.preset + '.settings'
        if section in self.config:
            count = self.config.get(section, 'social_suggestion_count', fallback=10)
            try:
                return int(count)
            except:
                return 10
        else:
            return 10

    def getGlobalSuggestionCount(self):
        '''Return Global Suggestions Request Count'''
        section = self.preset + '.settings'
        if section in self.config:
            count = self.config.get(section, 'global_suggestion_count', fallback=10)
            try:
                return int(count)
            except:
                return 10
        else:
            return 10

    def getFriendSuggestionsPerCategoryCount(self):
        '''Return Friend Suggestions Per Category Request Count'''
        section = self.preset + '.settings'
        if section in self.config:
            count = self.config.get(section, 'friend_suggestion_count', fallback=10)
            try:
                return int(count)
            except:
                return 10
        else:
            return 10
        
    def getOldSuggestionsFromDate(self):
        '''Return Date Old Suggestions Query From'''
        section = self.preset + '.old_suggestions'
        if section in self.config:
            date = self.config.get(section, 'from_date', fallback=None)
            try:
                return datetime.strptime(date,"%Y-%m-%d %H:%M:%S.%f")
            except:
                return None
        else:
            return None

    def getOldSuggestionsToDate(self):
        '''Return Date Old Suggestions Query To'''
        section = self.preset + '.old_suggestions'
        if section in self.config:
            date = self.config.get(section, 'to_date', fallback=None)
            try:
                return datetime.strptime(date,"%Y-%m-%d %H:%M:%S.%f")
            except:
                return None
        else:
            return None

    def getUserFeedFromDate(self):
        '''Return Date User Feed Query From'''
        section = self.preset + '.user_feed'
        if section in self.config:
            date = self.config.get(section, 'from_date', fallback=None)
            try:
                return datetime.strptime(date,"%Y-%m-%d %H:%M:%S.%f")
            except:
                return None
        else:
            return None

    def getUserFeedToDate(self):
        '''Return Date User Feed Query To'''
        section = self.preset + '.user_feed'
        if section in self.config:
            date = self.config.get(section, 'to_date', fallback=None)
            try:
                return datetime.strptime(date,"%Y-%m-%d %H:%M:%S.%f")
            except:
                return None
        else:
            return None

    '''
    Input Filter
    '''
# (1) Current Suggestions
    def allowCurrentSuggestions(self):
        '''Allow Current Suggestions'''
        section = self.preset + '.input'
        if section in self.config:
            value = self.config.get(section, 'use_currentSuggestions')
            try:
                return int(value)
            except:
                return self.default
        else:
            return self.default
# (2) Previous Suggestions
    def allowPreviousSuggestions(self):
        '''Allow Previous Suggestions'''
        section = self.preset + '.input'
        if section in self.config:
            value = self.config.get(section, 'use_previousSuggestions')
            try:
                return int(value)
            except:
                return self.default
        else:
            return self.default
# (3) Global Suggestions
    def allowGlobalSuggestion(self):
        '''Allow Global Suggestions'''
        section = self.preset + '.input'
        if section in self.config:
            value = self.config.get(section, 'use_globalSuggestion')
            try:
                return int(value)
            except:
                return self.default
        else:
            return self.default
# (4) Personal Suggestion
    def allowPersonalSuggestion(self):
        '''Allow Personal Suggestions'''
        section = self.preset + '.input'
        if section in self.config:
            value = self.config.get(section, 'use_personalSuggestion')
            try:
                return int(value)
            except:
                return self.default
        else:
            return self.default
# (5) Friend List
    def allowFriendList(self):
        '''Allow Friend List'''
        section = self.preset + '.input'
        if section in self.config:
            value = self.config.get(section, 'use_friendList')
            try:
                return int(value)
            except:
                return self.default
        else:
            return self.default
# (6) Social Suggestions
    def allowSocialSuggestion(self):
        '''Allow Social Suggestions'''
        section = self.preset + '.input'
        if section in self.config:
            value = self.config.get(section, 'use_socialSuggestion')
            try:
                return int(value)
            except:
                return self.default
        else:
            return self.default
# (7) Liked Products
    def allowLikedProducts(self):
        '''Allow Liked Products'''
        section = self.preset + '.input'
        if section in self.config:
            value = self.config.get(section, 'use_likedProducts')
            try:
                return int(value)
            except:
                return self.default
        else:
            return self.default
# (8) Disliked Products
    def allowDisLikedProducts(self):
        '''Allow Disliked Products'''
        section = self.preset + '.input'
        if section in self.config:
            value = self.config.get(section, 'use_disLikedProducts')
            try:
                return int(value)
            except:
                return self.default
        else:
            return self.default
# (9) Commented Products
    def allowCommentedProducts(self):
        '''Allow Commented Products'''
        section = self.preset + '.input'
        if section in self.config:
            value = self.config.get(section, 'use_commentedProducts')
            try:
                return int(value)
            except:
                return self.default
        else:
            return self.default
# (10) Cart Added Products
    def allowCartAddedProducts(self):
        '''Allow Cart Added Products'''
        section = self.preset + '.input'
        if section in self.config:
            value = self.config.get(section, 'use_cartAddedProducts')
            try:
                return int(value)
            except:
                return self.default
        else:
            return self.default
# (11) Cart Removed Products
    def allowCartRemovedProducts(self):
        '''Allow Cart Removed Products'''
        section = self.preset + '.input'
        if section in self.config:
            value = self.config.get(section, 'use_cartRemovedProducts')
            try:
                return int(value)
            except:
                return self.default
        else:
            return self.default
# (12) Wishlist Added Products
    def allowWishListAddedProducts(self):
        '''Allow  Wishlist Added Products'''
        section = self.preset + '.input'
        if section in self.config:
            value = self.config.get(section, 'use_wishListAddedProducts')
            try:
                return int(value)
            except:
                return self.default
        else:
            return self.default
# (13) Wishlist Removed Products
    def allowWishListRemovedProducts(self):
        '''Allow Wishlist Removed Products'''
        section = self.preset + '.input'
        if section in self.config:
            value = self.config.get(section, 'use_wishListRemovedProducts')
            try:
                return int(value)
            except:
                return self.default
        else:
            return self.default
# (14) Suggestions From Request (Before Save)
    def allowRequestSuggestion(self):
        '''Allow Suggestions From Request'''
        section = self.preset + '.input'
        if section in self.config:
            value = self.config.get(section, 'use_requestSuggestion')
            try:
                return int(value)
            except:
                return self.default
        else:
            return self.default
# (15) Cart From Request (Before Save)
    def allowRequestCart(self):
        '''Allow Cart From Request'''
        section = self.preset + '.input'
        if section in self.config:
            value = self.config.get(section, 'use_requestCart')
            try:
                return int(value)
            except:
                return self.default
        else:
            return self.default
# (16) WishList From Request (Before Save)
    def allowRequestWishList(self):
        '''Allow WishList From Request'''
        section = self.preset + '.input'
        if section in self.config:
            value = self.config.get(section, 'use_requestWishList')
            try:
                return int(value)
            except:
                return self.default
        else:
            return self.default
# (17) Requested Categories
    def allowRequestedCategories(self):
        '''Allow Requested Categories'''
        section = self.preset + '.input'
        if section in self.config:
            value = self.config.get(section, 'use_requestedCategories')
            try:
                return int(value)
            except:
                return self.default
        else:
            return self.default
# (18) Requested Number of Suggestions
    def allowRequestedSuggestionCount(self):
        '''Allow Requested Number of Suggestions'''
        section = self.preset + '.input'
        if section in self.config:
            value = self.config.get(section, 'use_requestedSuggestionCount')
            try:
                return int(value)
            except:
                return self.default
        else:
            return self.default