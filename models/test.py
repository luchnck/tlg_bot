from models import *
import logging, momoko
import psycopg2
import tornado
from snaql.factory import Snaql

logging.basicConfig(level = logging.DEBUG)
#db = psycopg2.connect("user=postgres password=postgres dbname=qa_bot host=localhost port=5432")

@gen.coroutine
def main():    

     template = Snaql('','queries').load_queries('model.sql')

     ioloop = tornado.ioloop.IOLoop.current()
     dsn = "user=postgres password=postgres dbname=qa_bot host=localhost port=5432"
     db =  momoko.Pool(
            dsn=dsn,
            size=1,
            max_size=3,
            ioloop=ioloop,
            setsession=("SET TIME ZONE UTC",),
            raise_connect_errors=False,
        )
     
     future = db.connect()
     ioloop.add_future(future, lambda x: ioloop.stop())
     ioloop.start()
     
     a = User(db,template)
     a.chat_id = 135195422 

     future = a.selectThis()
     ioloop.add_future(future, lambda x: ioloop.stop())
     ioloop.start()
     print(future.result())

     a.game_id = 4 
     future = a.updateThis()
     ioloop.add_future(future, lambda x: ioloop.stop())
     ioloop.start()
     print(future.result())
    
     
#print(user.execute(user.selectThis()))

main()
