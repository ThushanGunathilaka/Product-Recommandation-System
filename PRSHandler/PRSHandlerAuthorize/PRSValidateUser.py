#from  DataAccess  import UserManagerFRS
import logging

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger("Validate User")
from PRSBoot.PRSConfig import Conf
LOGGER.propagate = Conf().getVerbose()

# file handler
handler = logging.FileHandler('PRS.log')
handler.setLevel(logging.INFO)
# logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

LOGGER.addHandler(handler)

class ValidateUser(object):
    '''
    Authorize Request
    '''
    def validateUser(self,userID,password):
        authorizedUser = True
        if authorizedUser:
            LOGGER.info (' User ID : {} Authorized'.format(userID))
            return authorizedUser
        else:
            LOGGER.info (' User ID : {} Not Authorized'.format(userID))
            return False

    #def validateUser(self,userID,password):
    #    try:
    #        authorizedUser = False
    #        email = UserManagerFRS.UserManagerFRS().getUserEmail(userID)
    #        if email != None and email != '':
    #            authorizedUser = UserManagerFRS.UserManagerFRS().booleanValidation(email,password)
    #        if authorizedUser is not None and authorizedUser:
    #            LOGGER.info (' User ID : {} Authorized'.format(userID))
    #        else:
    #            LOGGER.info (' User ID : {} Not Authorized'.format(userID))
    #            authorizedUser = False
    #        return authorizedUser
    #    except:
    #        return False

