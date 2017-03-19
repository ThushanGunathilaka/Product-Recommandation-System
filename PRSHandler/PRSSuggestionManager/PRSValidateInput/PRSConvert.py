import logging

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger("Input Convert")
from PRSBoot.PRSConfig import Conf
#LOGGER.propagate = Conf().getVerbose()
LOGGER.propagate = False

# file handler
handler = logging.FileHandler('PRS.log')
handler.setLevel(logging.INFO)
# logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

LOGGER.addHandler(handler)

class Convert(object):
    ''' Convert Values '''
    def binaryToBool(self,number):
        value = number
        result = False
        try:
            value = int(value)
        except:
            value = 0
        if value == 1:
            result = True
        else:
            result = False
        LOGGER.info(' binaryToBool : input = [{}] ==> output = [{}]'.format(number,result))
        return result

    def listToIntList(self,inputValue):
        value = inputValue
        try:
            value = list(map(int, value))
            if not len(value) > 0:
                value = None
        except:
            value = None
        LOGGER.info(' listToIntList : input = {} ==> output = {}'.format(inputValue,value))
        return value

