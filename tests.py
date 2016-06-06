import logging

class mockApp():
      def __init__(self):
          self.db = ''
print("first create")
import sys,os; sys.path.append(os.path.abspath(''));from routes.routes import *;  andler = abstractHandler(mockApp())
#actions = {"/start" : Action }
action = andler.getAction({'message':{'text':'/start action'}})(andler, {'message':{'text':'/start action'}})
print("call done!")
print(action.message)
print(action)
