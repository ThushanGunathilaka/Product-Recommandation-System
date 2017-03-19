from io import StringIO
from configparser import ConfigParser
import os
from tornado.options import  options,define
#import pymongo
#import pymysql
import logging
#from PRSBoot.PRSBootAccess.PRSAccess import Access

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger("Configuration Manager")
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
    '''Manage Server Settings for Product Recommandation System(PRS)'''
    configFileName = None
    config = None
    environment = None  #[DEV|PROD]

    def __init__(self):
        '''
        Initializes the instance with a configuration file name
        '''
        self.configFileName = Conf().getServerConfig()
        self.config = ConfigParser()
        self.config.read(self.configFileName)
        self.environment = Conf().getServerEnvironment()

    def getServerHost(self):
        '''Return Server Host'''
        if 'DEFAULT' in self.config:
            return self.config.get('DEFAULT', 'server_host', fallback='localhost')
        else:
            return None

    def getServerPort(self):
        '''Return Server Port'''
        if 'DEFAULT' in self.config:
            return self.config.get('DEFAULT', 'server_port', fallback='9915')
        else:
            return None

    def getServerProtocol(self):
        '''Return Server Protocol'''
        if 'DEFAULT' in self.config:
            return self.config.get('DEFAULT', 'server_protocol', fallback='http://')
        else:
            return None

    def getSection(self,package):
        '''Return package from correct environment'''
        prefix = None
        if self.environment == 'DEV':
            prefix = 'dev.'
        elif self.environment == 'PROD':
            prefix = 'prod.'
        return prefix + str(package)

    '''
    MySQL Functions
    '''

    def getMySQLHost(self):
        '''Return MySQL Host'''
        section = self.getSection('mysql')
        if section in self.config:
            return self.config.get(section, 'mysql_host', fallback='localhost')
        else:
            return None

    def getMySQLPort(self):
        '''Return MySQL Port'''
        section = self.getSection('mysql')
        if section in self.config:
            return self.config.get(section, 'mysql_port', fallback='3306')
        else:
            return None

    def getMySQLUsername(self):
        '''Return MySQL Username'''
        section = self.getSection('mysql')
        if section in self.config:
            return self.config.get(section, 'mysql_username', fallback='root')
        else:
            return None

    def getMySQLPassword(self):
        '''Return MySQL Password'''
        section = self.getSection('mysql')
        if section in self.config:
            return self.config.get(section, 'mysql_password', fallback='')
        else:
            return None

    def getMySQLDefaultDatabase(self):
        '''Return MySQL Password'''
        section = self.getSection('mysql')
        if section in self.config:
            return self.config.get(section, 'mysql_default_database', fallback='beforecart')
        else:
            return None


    '''
    MongoDB Functions
    '''

    def getMongoDBHost(self):
        '''Return MongoDB Host'''
        section = self.getSection('mongodb')
        if section in self.config:
            return self.config.get(section, 'mongodb_host', fallback='localhost')
        else:
            return None

    def getMongoDBPort(self):
        '''Return MongoDB Port'''
        section = self.getSection('mongodb')
        if section in self.config:
            return self.config.get(section, 'mongodb_port', fallback='3306')
        else:
            return None

    def getMongoDBUsername(self):
        '''Return MongoDB Username'''
        section = self.getSection('mongodb')
        if section in self.config:
            return self.config.get(section, 'mongodb_username', fallback='root')
        else:
            return None

    def getMongoDBPassword(self):
        '''Return MongoDB Password'''
        section = self.getSection('mongodb')
        if section in self.config:
            return self.config.get(section, 'mongodb_password', fallback='')
        else:
            return None

    def getMongoDBDefaultDatabase(self):
        '''Return MongoDB Password'''
        section = self.getSection('mongodb')
        if section in self.config:
            return self.config.get(section, 'mongodb_default_database', fallback='beforecart')
        else:
            return None

    #def initMongoDB(self,mongoDB):
    #    return self.initDatabase.initMongoDB(mongoDB,self.getMongoDBDefaultDatabase())

    #def initMySQL(self,mySQLCursorConnection):
    #    return self.initDatabase.initMySQL(mySQLCursorConnection)

    #def getMongoDBObject(self):
    #    '''
    #    Return MongoDB Object
    #    '''
    #    host = self.getMongoDBHost()
    #    port = self.getMongoDBPort()
    #    database = self.getMongoDBDefaultDatabase()

    #    if host != None and port != None and database != None:
    #        #Mongodb Connection Settings
    #        if self.environment == 'PROD':
    #            define("mongodb_host",host, help='MongoDB Host Name', type=str)
    #        else:
    #            define("mongodb_host",host+':'+port, help='MongoDB Host Name', type=str)

    #        define("mongodb_name",default=database, help='MongoDBDefault Database Name', type=str)
    #        #define("user", default=self.getMongoDBUsername(), help="MongoDB Username")
    #        #define("password", default=self.getMongoDBPassword(), help="MongoDB Password")

    #        try:
    #            maxSevSelDelay = 5
    #            mongoClient = pymongo.MongoClient(options.mongodb_host,serverSelectionTimeoutMS=maxSevSelDelay)
    #            self.mongoDBObject = mongoClient
    #            LOGGER.info ('New MongoDB Connection Created')

    #            mongoClient.server_info()
    #            return self.mongoDBObject
    #        except:
    #            LOGGER.warn ('Unable to create MongoDB Connection')
    #            return None
    #    else:
    #        return None

    #def getMySQLConnection(self):
    #    '''Return Mysql Connection'''
    #    host = self.getMySQLHost()
    #    port = self.getMySQLPort()
    #    database = self.getMySQLDefaultDatabase()
    #    username = self.getMySQLUsername()
    #    password = self.getMySQLPassword()

    #    if host != None and port != None and database != None and username != None and password != None:
    #        try:
    #            #open connection
    #            #localhost-url with port; root -username- ""-password beforecart-database_name
    #            self.mySQLCursorConnection = pymysql.connect(host,username,password,database)
    #            LOGGER.info ('New Mysql Connection Created')
    #            return self.mySQLCursorConnection
    #        except:
    #            LOGGER.warn ('Unable to create Mysql Connection')
    #            return None
    #    else:
    #        return None