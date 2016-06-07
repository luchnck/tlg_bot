import sys
import logging
import re

import tornado.gen
from tornado.web import  RequestHandler
from models.models import User,Task,Game


logging.basicConfig(level = logging.DEBUG)

class Action(object):

#    def __new__(cls,*args, **kwargs):
#        print("__new__",cls)
#        obj = super(Action,cls).__new__(Action)
#        print ("created object", obj)
#        return obj    

    def __init__(self,*args,**kwargs):
        handler = args[0]
        message = args[1]
        #logging.debug("__init__(",args,") initialised")
        self._app = handler.application
        self._message = message

    def __call__(self, *args, **kwargs ):
        #logging.debug("__call__",self)
        return self
   
    @property
    def application(self):
        return self._app

    @property
    def message(self):
        return self._message

    def do(self):
        pass

class startAction(Action):

    def __init__(self,handler,message):
        super(startAction,self).__init__(handler,message)

    @tornado.gen.coroutine
    def do(self):
        user = User(self._app.db)
        user.chat_id = ''.join(filter(str.isdigit,str(self.message['message']['chat']['id'])))
        conterQuery = { 
                        'chat_id' : self.message['message']['chat']['id'],
                        'text'    : ''
                      }

        yield user.selectThis()
        logging.debug("gotted user from db is %s " % str(user.chat_id))
        if user.game_id != '':
            conterQuery['text'] = 'You are already registered!!! Then task'
        else:
            yield user.insertThis()
            conterQuery['text'] = 'You will be registered in system, task will be sended in seconds!!!'
        
        game = Game(self._app.db)
        game.id = user.game_id
        yield game.selectThis()
        
        task = Task(self._app.db)
        task.id = game.getTask()
        yield task.selectThis() 
        
        conterQuery['text'] = task.text
        
        raise tornado.gen.Return(conterQuery)

class answerAction(Action):

    def __init__(self,handler,message):
        super(answerAction,self).__init__(handler,message)

    @tornado.gen.coroutine
    def do(self):
        user = User(self._app.db)
        user.chat_id = ''.join(filter(str.isdigit,str(self.message['message']['chat']['id'])))
        find = re.match("/answer[ ]*(.+)", str(self.message['message']['text']), re.IGNORECASE)
        
        conterQuery = {
                        'chat_id' : self.message['message']['chat']['id'],
                        'text'    : ''
                      }

        if find is None:
            conterQuery['text'] = "There is no answer!"
            logging.warning("answerAction.do(): User's answer don't contain text: \n %s", (self.message['message']['text']))
            raise tornado.gen.Return(conterQuery)
        answer = find.groups()[0]

        yield user.selectThis()
        logging.debug("answerAction.do(): gotted user from db is %s " % str(user.chat_id))
        

        if (user.game_id == ''):
            conterQuery['text'] = 'You not take a competition in game, please register by typing "/start" or "/help" for help'
            logging.warning("answerAction.do(): user dont have permissions to game \n user - %s " % str(user.chat_id))
            raise tornado.gen.Return(conterQuery)

        game = Game(self._app.db)
        game.id = user.game_id
        yield game.selectThis()

        task = Task(self._app.db)
        task.id = game.getTask()
        if not (task.id):
            logging.error("answerAction.do(): task id is not defined for user %s " % str(user.chat_id))
            conterQuery['text'] = "we don't have any tasks for you, please send /start or /help"
            raise tornado.gen.Return(conterQuery)

        yield task.selectThis()
        if not (task.compareAnswer(answer)):
            logging.info("answerAction.do(): User sended wrong answer: \n user %s, task.answer %s, answer %s", (user.chat_id, task.answer, answer))
            conterQuery['text'] = "This is wrong answer! Try another"
            raise tornado.gen.Return(conterQuery)
        
        conterQuery['text'] = "Thats right!!, we give you new task soon! Wait.."
        logging.info("answerAction.do(): User sended right answer and will take new task \n user %s, task.answer %s, answer %s", (user.chat_id, task.answer, answer))
        raise tornado.gen.Return(conterQuery)




class defaultAction(Action):

    def __init__(self,handler,message):
        super(defaultAction, self).__init__(handler,message)

    @tornado.gen.coroutine
    def do(self):
        conterQuery = {
                        'chat_id' : self.message['message']['chat']['id'],
                        'text'    : 'standard help message'
                      }
        logging.debug("defaultAction.do() string is %s" % conterQuery)
        raise tornado.gen.Return(conterQuery)


class abstractHandler(tornado.web.RequestHandler):
   
   # def __init__(self, application):
   #     self.application = application
 
    @property
    def db(self):
       return self.application.db

    @property
    def actions(self):
       return {
                  '/default' : defaultAction,
                  '/start' : startAction,
                  '/answer' : answerAction
              }

    def getAction(self, message = {}):
       action = '/default'
       try:
            action = str(message['message']['text'])
       except Exception as e:
            logging.warning("abstractHandler.getAction():User's input don't have a action, or text field in request: %s" % message)
            return 
       if (action[0] == '/'):
            count = len(action)
            space = action.find(' ')
            if (space > 0):
                 pos = space
            else:
                 pos = count
            action = action[0:pos]
       if action in self.actions.keys():
            return self.actions[action](self,message)
       else:
            return self.actions['/default'](self,message)
            
class mainHandler(abstractHandler):
    @tornado.gen.coroutine
    def post(self):
        message = tornado.escape.json_decode(self.request.body)
        logging.debug("got request from telegram server as %s " % message)

        action = self.getAction(message)(self, message)
        conterQuery = yield action.do() 

        responseConter = yield self.application.sendMessage(conterQuery)
        logging.debug("recieved answer from tlgServer is %s" % responseConter)
        self.finish() 


