class Model():
    def select(self, fields = '*', where = {}, table = ''):
        queryStr = "SELECT %s FROM %s %s"
        whereStr = ''
        if (len(where.keys()) > 0):
            if_where = []
            for i in where.keys():
                if_where.append(i + ' = "' + str(where[i])+'"')
                whereStr = str.join(' AND ',if_where)
                whereStr = "WHERE " + whereStr
        query = (str.join(',', fields), table, whereStr)
        return queryStr, query

    def insert(self, fields, table):
        queryStr = "INSERT INTO %s(%s) VALUES(%s)"
        if (len(fields.keys()) <= 0 ):
             return
        insertStr = (table, str.join(',',fields.keys()),'"'+str.join('","',[str(item) for item in fields.values()]) + '"')
        return queryStr, insertStr
        
    def _getNotEmptyVars(self):
        vars =  [ arg for arg in dir(self) if (not arg.startswith('_')) & ( not callable(getattr(self,arg))) ]
        return [arg for arg in vars if getattr(self,arg) != '']

    def selectThis(self):
        notEmpty = self._getNotEmptyVars()
        where = {}
        for item in notEmpty:
            where[item] = getattr(self,item)
        return  self.select(where = where,table = self._table)

    def selectAll(self, fields = ''):
        return self.select(where = {},table = self._table)
    
    def selectMany(self, fields = '*', where = {}, table = ''):
        return self.select(fields = fields, where = where,table = self._table)

    def insertThis(self):
        notEmpty = self._getNotEmptyVars()
        fields = {}
        for var in notEmpty:
            fields[var] = getattr(self,var)
        return self.insert(fields,self._table)


class User(Model):

    def __init__(self):
        self.chat_id = ''
        self.task_id = ''
        self.progress = ''
        self.timescore = ''
        self._table = "public.user"
    


class Task(Model):
    def __init__(self):
        self.id = ''
        self.text = ''
        self.images = ''
        self.topic = ''
        self.answer = ''
        self._table = "public.task"

def main():    
     import momoko
     import tornado.ioloop

     ioloop = tornado.ioloop.IOLoop.instance()
     dsn = "user=postgres password=postgres dbname=qa_bot host=localhost port=5432"
     db =  momoko.Pool(
            dsn=dsn,
            size=1,
            max_size=3,
            ioloop=ioloop,
            setsession=("SET TIME ZONE UTC",),
            raise_connect_errors=False,
        )

     a = User()
     a.chat_id = 5
     a.progress = 2
     a.timescore = "123456"
     print(a.insertThis())

     b = Task()
     b.id = 5
     b.text = "blabla"
     print(b.selectThis())

