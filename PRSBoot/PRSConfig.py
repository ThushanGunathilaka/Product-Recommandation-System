from io import StringIO
from configparser import ConfigParser
import os
from tornado.options import  options,define
import logging

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger("Boot Config")
#LOGGER.propagate = False

# file handler
handler = logging.FileHandler('PRS.log')
handler.setLevel(logging.INFO)
# logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

LOGGER.addHandler(handler)

class Conf(object):
    '''Manage Server Settings'''
    configFileName = None
    config = None
    environment = None  #[DEV|PROD]

    def __init__(self):
        '''
        Initializes the instance with a configuration file name
        '''
        self.configFileName = 'PRSBoot\config.ini'
        self.config = ConfigParser()
        self.config.read(self.configFileName)

    def getStoreOldSuggestions(self):
        '''Store Old Suggestions'''
        if 'PRS' in self.config:
            value = self.config.get('PRS', 'store_old_suggestions', fallback='0')
            try:
                value = int(value)
            except:
                value = 0
            if value == 1:
                return True
            else:
                return False
        else:
            return False

    def getProductTableInStock(self):
        '''Return MySQL Product Table Availability Column Name'''
        if 'MYSQL.CATALOG.WAREHOUSE' in self.config:
            return self.config.get('MYSQL.CATALOG.WAREHOUSE', 'catalog_table_product_availability_column_name', fallback='inStock')
        else:
            return 'inStock'

    def getCatalogTableIDName(self):
        '''Return MySQL Catalog Table ID Name'''
        if 'MYSQL.COULMN' in self.config:
            return self.config.get('MYSQL.COULMN', 'catalog_table_id_name', fallback='id')
        else:
            return 'id'

    def getCategoryTableIDName(self):
        '''Return MySQL Category Table ID Name'''
        if 'MYSQL.COULMN' in self.config:
            return self.config.get('MYSQL.COULMN', 'category_table_id_name', fallback='id')
        else:
            return 'id'

    def getCatalogTableName(self):
        '''Return MySQL Catalog Table Name'''
        if 'MYSQL' in self.config:
            return self.config.get('MYSQL', 'catalog_table_name', fallback='product')
        else:
            return 'product'

    def getCategoryTableName(self):
        '''Return MySQL Category Table Name'''
        if 'MYSQL' in self.config:
            return self.config.get('MYSQL', 'category_table_name', fallback='category')
        else:
            return 'category'

    def getUserDataCollectionName(self):
        '''Return MongoDB User Data Collection Name'''
        if 'MONGODB' in self.config:
            return self.config.get('MONGODB', 'user_data_collection_name', fallback='UpdateData')
        else:
            return 'UpdateData'

    def getSuggestionDataCollectionName(self):
        '''Return MongoDB Suggestion Data Collection Name'''
        if 'MONGODB' in self.config:
            return self.config.get('MONGODB', 'suggestion_data_collection_name', fallback='SuggestionData')
        else:
            return 'SuggestionData'

    def getSuggestionHistoryCollectionName(self):
        '''Return MongoDB Suggestion History Collection Name'''
        if 'MONGODB' in self.config:
            return self.config.get('MONGODB', 'suggestion_history_collection_name', fallback='SuggestionHistory')
        else:
            return 'SuggestionHistory'

    def getServerEnvironment(self):
        '''Return Server Environment Type'''
        if 'DEFAULT' in self.config:
            return self.config.get('DEFAULT', 'environment', fallback='DEV')
        else:
            return None

    def getServerConfig(self):
        '''Return Server Configuration File Name'''
        if 'DEFAULT' in self.config:
            return self.config.get('DEFAULT', 'server_config', fallback='PRSBoot\PRSBootConfig\config.ini')
        else:
            return None

    def getHandlerConfig(self):
        '''Return Handler ConfigurationFile Name Port'''
        if 'DEFAULT' in self.config:
            return self.config.get('DEFAULT', 'handler_config', fallback='PRSHandler\PRSHandlerConfig\config.ini')
        else:
            return None

    def getEngineConfig(self):
        '''Return Suggestion Engine Configuration File Name'''
        if 'DEFAULT' in self.config:
            return self.config.get('DEFAULT', 'engine_config', fallback=None)
        else:
            return None

    def getVerbose(self):
        '''Return Verbose Status'''
        if 'DEFAULT' in self.config:
            count = self.config.get('DEFAULT', 'verbose', fallback=1)
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