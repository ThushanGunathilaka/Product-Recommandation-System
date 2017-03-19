import os
import sys
import tornado
import pymongo
from datetime import datetime
from tornado.options import  options
from tornado.options import define
from tornado import ioloop, web
import logging

from PRSBoot.PRSBootConfig.PRSManager import Manager
from PRSBoot.PRSBootConfig.PRSConnection import Connection
from PRSHandler.PRSSuggestionHandler import SuggestionHandler
from PRSHandler.PRSUpdateHandler import UpdateHandler

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger("Request Handler")
from PRSBoot.PRSConfig import Conf
LOGGER.propagate = Conf().getVerbose()

# file handler
handler = logging.FileHandler('PRS.log')
handler.setLevel(logging.INFO)
# logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

LOGGER.addHandler(handler)

class RequestHandler(object):
    '''
    Handles client requests
    '''
    manager = None
    mongodb = None
    mysql = None
    ioloop = None
    protocol = None
    host = None
    port = None

    def __init__(self):
        '''
        Initializes the instance with a configuration file name
        '''
        self.manager = Manager()
        self.connection = Connection()
        self.protocol = self.manager.getServerProtocol()
        self.host = self.manager.getServerHost()
        self.port = self.manager.getServerPort()

    def start_server(self):
        '''
        Start Tornado Server with configurations and database connections
        '''
        LOGGER.info ('MongoDB Database needs to be up and running on {}:{}'.format(str(self.manager.getMongoDBHost()),str(self.manager.getMongoDBPort())))
        LOGGER.info ('MySQL Database needs to be up and running on {}:{}'.format(str(self.manager.getMySQLHost()),str(self.manager.getMySQLPort())))
        
        #adding local directory to path
        sys.path.append(os.path.dirname(os.path.realpath(__file__)))
        define("static_path", default=os.path.join(os.path.dirname(os.path.realpath(__file__)),'..','client'), help='static path', type=str)
        #Server Port
        define("port", default=self.port, help="port", type=int)
        #Initialize Databases
        define("initMongoDB",default=1, help='Initisalize MongoDB Instance', type=int)
        define("initMySQL",default=1, help='Initisalize MySQL Instance', type=int)
        mongodb = self.connection.getMongoDBObject()
        mysql = self.connection.getMySQLConnection()
        static_path = options.static_path

        if mysql != None and mongodb != None and self.host != None and self.port != None and self.protocol != None:
            app = tornado.web.Application([
                (r'/prs/recommend', SuggestionHandler, dict(db=[mongodb,self.manager.getMongoDBDefaultDatabase()])),
                (r'/prs/update', UpdateHandler, dict(db=[mongodb,self.manager.getMongoDBDefaultDatabase()]))
            ],
                static_path=static_path,
                autoreload=True
            )

            #read settings from commandline
            options.parse_command_line()
            checkStatus = True
            if options.initMongoDB:
                if not self.connection.initMongoDB(mongodb):
                    checkStatus = False
            if options.initMySQL:
                if not self.connection.initMySQL(mysql):
                    checkStatus = False
            if checkStatus:
                print ('Tornado server running on {}{}:{}'.format(str(self.protocol),str(self.host),str(self.port)))
                app.listen(options.port,xheaders=True)
                ioloop = tornado.ioloop.IOLoop.instance()
                ioloop.start()
            return checkStatus
        else:
            return False

if __name__ == "__main__":
    '''
    Run Tornado server
    '''
    server = RequestHandler()
    server.start_server()