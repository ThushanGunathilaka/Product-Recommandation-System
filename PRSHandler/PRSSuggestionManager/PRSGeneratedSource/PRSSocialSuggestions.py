import logging
import random

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger("Suggestion Source Social")
from PRSBoot.PRSConfig import Conf
LOGGER.propagate = Conf().getVerbose()
LOGGER.propagate = False

# file handler
handler = logging.FileHandler('PRS.log')
handler.setLevel(logging.INFO)
# logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

LOGGER.addHandler(handler)

from PRSHandler.PRSSuggestionManager.PRSValidateInput.PRSValidate import Validate
from PRSHandler.PRSSuggestionManager.PRSSuggestionSource.PRSPersonalSuggestion import PersonalSuggestion
class SocialSuggestions(object):
    '''
    Get Social Suggestions
    '''
    def getSocialSuggestion(self,total,friendList):
        list = self.generateSocialSuggestions(friendList,total)
        LOGGER.info ('Social Suggestions : {}'.format(list))
        LOGGER.info ('Social Suggestions Introduced')
        return Validate().checkSuggestionInput(list)

    def generateSocialSuggestions(self,friendList,total):
        '''Best Strength Products from Friends'''
        socialSuggestions = []
        friendSet = []
        if friendList is not None and bool(friendList):
            for key, value in dict(friendList).items():
                if value is not None and len(value)>0:
                    for friend in value:
                        friendSet.append([friend['id'],friend['strength'],key])
        if friendSet is not None and len(friendSet)>0:
            for friend in friendSet:
                friendSuggestion = []
                friendSuggestion = PersonalSuggestion().getPersonalSuggestion(friend,total)
                if friendSuggestion is not None and len(friendSuggestion)>0:
                    for suggestion in friendSuggestion:
                        if friend[2] == suggestion['category']:
                            product = {}
                            product.update({'userID': friend[0]})
                            product.update({'id': suggestion['id']})
                            product.update({'score': suggestion['score']})
                            product.update({'weight': suggestion['weight']})
                            product.update({'strength': friend[1]})
                            product.update({'category': suggestion['category']})
                            socialSuggestions.append(product)

            result = {}
            for item in socialSuggestions:
                if not item['id'] in result:
                    result.update({item['id']: item})
                else:
                    if result[item['id']]['strength'] < item['strength']:
                        result.update({item['id']: item})
                    elif result[item['id']]['strength'] == item['strength']:
                        if result[item['id']]['score'] < item['score']:
                            result.update({item['id']: item})
                        if result[item['id']]['weight'] < item['weight']:
                            result.update({item['id']: item})
            result = list(result.values())
            return sorted(result, key=lambda x: x['strength'],reverse = True)