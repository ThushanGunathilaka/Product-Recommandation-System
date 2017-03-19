import logging
import random

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger("User Source Friends")
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
#from DataAccess.FriendshipManagerFRS import FriendshipManagerFRS
class FriendList(object):
    '''
    Get Friend List
    '''
    def getFriendList(self,id,total,categoryID):
        #list =  FriendshipManagerFRS().getFriendListFRS(id,total,categoryID)   
        list = self.getRandomListPRS(id,total,categoryID)
        LOGGER.info ('Friend List For Category ID {} : {}'.format(categoryID,list))
        LOGGER.info ('Friend List Introduced For Category ID : {}'.format(categoryID))
        return Validate().checkUserInput(list)

    def getRandomListPRS(self,id,total,categoryID):
        list =[]
        countID = 1
        count = 0
        idList =random.sample(range(100), int(total))
        while (count < int(total)):
            item = {}
            item.update({'id': idList[count]})
            item.update({'strength': random.randrange(100)})
            list.extend([item])
            count = count + 1
        return list
