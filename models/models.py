import os,sys,re,collections
from tornado import gen
import logging
from snaql.factory import Snaql

class Model():
    def __init__(self,db):
        self._db = db
        self._snaql = Snaql(os.path.dirname(__file__), 'queries')
        
#    @property
#    def db(self):
#        return self._db
    
    @gen.coroutine
    def execute(self, query):
        result = False
        try:
            result = yield self._db.execute(query)
        except Exception as e:
            logging.error("Model.execute(): Unable to execute query: %s becouse %s" % (query, e) )
            raise gen.Return(False)
        if ((re.match('SELECT', query, re.IGNORECASE))!= None):
            rows = result.fetchall()
            raise gen.Return(rows)
        else:
            raise gen.Return(True)
    
    @gen.coroutine
    def select(self, fields = '*', where = {}, table = ''):
        queryStr = "SELECT %s FROM %s %s"
        whereStr = ''
        if (len(where.keys()) > 0):
            if_where = []
            for i in where.keys():
                if i in self._strings:
                    if_where.append(i + " = '" + str(where[i])+"'")
                else:
                    if_where.append(i + ' = ' + str(where[i]))
                whereStr = str.join(' AND ',if_where)
                whereStr = "WHERE " + whereStr
        query = (str.join(',', fields), table, whereStr)
        logging.debug("Model.select(): query will be executed: %s" % str(query))
        result = yield self.execute(queryStr % query)
        raise gen.Return(result)

    @gen.coroutine
    def selectSnaql(self, *args, **kwargs):
        template = self._snaql.load_queries('model.sql')
        query = template.select_from_where(**kwargs)
        print(kwargs)
        result = yield self.execute(query)
        logging.debug("Model.selectThis: query was finished, query is %s " % query)
        raise gen.Return(result)
        

    @gen.coroutine
    def insert(self, fields, table):
        queryStr = "INSERT INTO %s(%s) VALUES(%s)"
        if (len(fields.keys()) <= 0 ):
             raise gen.Return()
        values = []
        for val in fields.keys():
             if val in self._strings:
                 values.append("'%s'" % fields[val])
             else:
                 values.append('%s' %  fields[val])
        insertStr = (table, str.join(',',fields.keys()),str.join(',',values))
        logging.debug("Model.insert(): query will be executed: %s" % str(insertStr))
        result = yield self.execute(queryStr % insertStr)
        raise gen.Return(result)
        
    def _getNotEmptyVars(self):
        vars =  [ arg for arg in dir(self) if (not arg.startswith('_')) & ( not callable(getattr(self,arg))) ]
        return [arg for arg in vars if getattr(self,arg) != '']

    @gen.coroutine
    def selectThis(self):
        notEmpty = self._getNotEmptyVars()
        where = {}
        for item in notEmpty:
            where[item] = getattr(self,item)
        result = yield  self.selectSnaql(conds = collections.OrderedDict(where),table = self._table, limit = 1)
        raise gen.Return(result)

    def selectAll(self, fields = ''):
        return self.select(where = {},table = self._table)
    
    def selectMany(self, fields = '*', where = {}, table = ''):
        return self.select(fields = fields, where = where,table = self._table)

    @gen.coroutine
    def insertThis(self):
        notEmpty = self._getNotEmptyVars()
        fields = {}
        for var in notEmpty:
            fields[var] = getattr(self,var)
        result = yield self.insert(fields,self._table)
        raise gen.Return(result)


class User(Model):

    def __init__(self,db):
        super(User,self).__init__(db)
        self.chat_id = ''
        self.game_id = ''
        self.progress = ''
        self.time_score = ''
        self._table = "public.user"
        self._strings = []

    def isUserRegistered(self):
        pass   


class Task(Model):
    def __init__(self):
        super(Task,self).__init__(db)
        self.id = ''
        self.text = ''
        self.images = ''
        self.topic = ''
        self.answer = ''
        self._table = "public.task"
        self._strings = ['text', 'images','topic','answer']

class Game(Model):

    def __init__(self):
        super(Game, self).__init__(db)
        self.id = ''
        self.task_list = ''
        self._start_timestamp = ''
        self._end_timestamp = ''
        self._table = 'public.game'
        
    @property
    def start_timestamp(self):
        return "'%s'::timestamp" % self._start_timestamp

    @property
    def end_timestamp(self):
        return "'%s'::timestamp" % self._end_timestamp

   
    


