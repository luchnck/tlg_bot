import sys
import logging

import tornado.gen
from tornado.web import  RequestHandler
from models.models import User,Task

class StartHandler(tornado.web.RequestHandler):
    
    @property
    def db(self):
       return self.application.db

    @tornado.gen.coroutine
    def post(self):
        user = User()
        message = tornado.escape.json_decode(self.request.body)
        conterQuery = { 'chat_id' : message['message']['chat']['id']}
        logging.debug("got request from telegram server as %s " % message)
        user.chat_id = ''.join(filter(str.isdigit,str(message['message']['chat']['id'])))
        cursor = yield self.db.execute(user.selectThis())
        result = cursor.fetchone()
        logging.debug("gotted result from db is %s " % str(result))
        if result != None:
            conterQuery['text'] = 'You are already registered!!! Then task'
        else:
            self.db.execute(user.insertThis())
            conterQuery['text'] = 'You will be registered in system, task will be sended in seconds!!!'
        responseConter = yield self.application.sendMessage(conterQuery)
        logging.debug("recieved answer from tlgServer is %s" % responseConter)
        self.finish() 


class InitHandler(tornado.web.RequestHandler):
    def post(self):
        message = tornado.escape.json_decode(self.request.body)
        logging.debug(" nswer will be sended to tlgServer %s" % message)
        self.finish()
    
