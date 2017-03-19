import logging
import random

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger("Suggestion Source Personal")
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
#from DataAccess.HistoryAnaylzerPPM import HistoryAnaylzerPPM
class PersonalSuggestion(object):
    '''
    Get Personal Suggestions
    '''
    def getPersonalSuggestion(self,id,total):
        #
        list = self.getRandomListWithCategoriesPRS(id,total)
        LOGGER.info ('Personal Suggestions : {}'.format(list))
        LOGGER.info ('Personal Suggestions Introduced')
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