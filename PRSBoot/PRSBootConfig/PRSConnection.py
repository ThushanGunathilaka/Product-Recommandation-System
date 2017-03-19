from io import StringIO
from configparser import ConfigParser
import os
from tornado.options import  options,define
import pymongo
import pymysql
import logging
from PRSBoot.PRSBootAccess.PRSAccess import Access

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger("Boot Connection")
from PRSBoot.PRSConfig import Conf
LOGGER.propagate = Conf().getVerbose()

# file handler
handler = logging.FileHandler('PRS.log')
handler.setLevel(logging.INFO)
# logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

LOGGER.addHandler(handler)

from PRSBoot.PRSBootConfig.PRSManager import Manager
class Connection(object):
    """description of class"""
    def getMongoDBObject(self):
        '''
        Return MongoDB Object
        '''
        manager = Manager()
        host = manager.getMongoDBHost()
        port = manager.getMongoDBPort()
        database = manager.getMongoDBDefaultDatabase()

        if host != None and port != None and database != None:
            #Mongodb Connection Settings
            if manager.environment == 'PROD':
                define("mongodb_host",host, help='MongoDB Host Name', type=str)
            else:
                define("mongodb_host",host+':'+port, help='MongoDB Host Name', type=str)

            define("mongodb_name",default=database, help='MongoDBDefault Database Name', type=str)
            #define("user", default=manager.getMongoDBUsername(), help="MongoDB Username")
            #define("password", default=manager.getMongoDBPassword(), help="MongoDB Password")

            try:
                maxSevSelDelay = 5
                mongoDBObject = pymongo.MongoClient(options.mongodb_host,serverSelectionTimeoutMS=maxSevSelDelay)
                LOGGER.info ('New MongoDB Connection Created')
                #LOGGER.info (mongoDBObject.server_info())
                return mongoDBObject
            except:
                LOGGER.warn ('Unable to create MongoDB Connection')
                return None
        else:
            return None

    def getMySQLConnection(self):
        '''Return Mysql Connection'''
        manager = Manager()
        host = manager.getMySQLHost()
        port = manager.getMySQLPort()
        database = manager.getMySQLDefaultDatabase()
        username = manager.getMySQLUsername()
        password = manager.getMySQLPassword()

        if host != None and port != None and database != None and username != None and password != None:
            try:
                #open connection
                #localhost-url with port; root -username- ""-password beforecart-database_name
                mySQLCursorConnection = pymysql.connect(host,username,password,database)
                LOGGER.info ('New Mysql Connection Created')
                return mySQLCursorConnection
            except:
                LOGGER.warn ('Unable to create Mysql Connection')
                return None
        else:
            return None

    def initMongoDB(self,mongoDB):
        return Access().initMongoDB(mongoDB,Manager().getMongoDBDefaultDatabase())

    def initMySQL(self,mySQLCursorConnection):
        return Access().initMySQL(mySQLCursorConnection)


