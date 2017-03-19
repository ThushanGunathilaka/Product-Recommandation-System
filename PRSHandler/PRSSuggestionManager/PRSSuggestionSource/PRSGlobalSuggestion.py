import logging
import random

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger("Suggestion Source Global")
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
#from DataAccess.GetPopularityDetailsGMI import GetPopularityDetailsGMI
class GlobalSuggestion(object):
    '''
    Get Global Suggestions
    '''
    def getGlobalSuggestion(self,id,total):
        #list = GetPopularityDetailsGMI().getListWithCategoriesGMI(20)
        list = self.getRandomListWithCategoriesPRS(id,total)
        LOGGER.info ('Global Suggestions : {}'.format(list))
        LOGGER.info ('Global Suggestions Introduced')
        return Validate().checkSuggestionInput(list)

    def getRandomListWithCategoriesPRS(self,id,total):
        list =[]
        countID = 1
        count = 0
        idList =random.sample(range(100), int(total))
        while (count < int(total)):
            item = {}
            item.update({'id': idList[count]})
            item.update({'score': random.randrange(100)})
            item.update({'weight': random.randrange(100)})
            item.update({'category': random.randint(1,6)})
            list.extend([item])
            count = count + 1
        return list

