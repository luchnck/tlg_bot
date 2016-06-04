import sys
import logging

import tornado.gen
from tornado.web import  RequestHandler
from models.models import User,Task


class Action():

    def __init__(self,handler,message = ''):
        self._app = handler.application
        self._message = message

    @property
    def application(self):
        return self._app

    @property
    def message(self):
        return self._message

    def do(self):
        pass

class startAction(Action):

    @tornado.gen.coroutine
    def do(self):
        user = User()
        user.chat_id = ''.join(filter(str.isdigit,str(self.message['message']['chat']['id'])))
        
        conterQuery = { 
                        'chat_id' : self.message['message']['chat']['id'],
                        'text'    : ''
                      }

        cursor = yield self.application.db.execute(user.selectThis())
        result = cursor.fetchone()
        logging.debug("gotted result from db is %s " % str(result))
        if result != None:
            conterQuery['text'] = 'You are already registered!!! Then task'
        else:
            self.application.db.execute(user.insertThis())
            conterQuery['text'] = 'You will be registered in system, task will be sended in seconds!!!'
        return conterQuery


class StartHandler(tornado.web.RequestHandler):
    
    @property
    def db(self):
       return self.application.db

    @tornado.gen.coroutine
    def post(self):
        message = tornado.escape.json_decode(self.request.body)
        logging.debug("got request from telegram server as %s " % message)

        action = startAction(self, message)
        conterQuery = yield action.do() 

        responseConter = yield self.application.sendMessage(conterQuery)
        logging.debug("recieved answer from tlgServer is %s" % responseConter)
        self.finish() 


class InitHandler(tornado.web.RequestHandler):
    def post(self):
        message = tornado.escape.json_decode(self.request.body)
        logging.debug(" nswer will be sended to tlgServer %s" % message)
        self.finish()
   


