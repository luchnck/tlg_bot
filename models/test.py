from models import *
import logging, momoko
import psycopg2
import tornado

logging.basicConfig(level = logging.DEBUG)
#db = psycopg2.connect("user=postgres password=postgres dbname=qa_bot host=localhost port=5432")

@gen.coroutine
def main():    

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
     a = User(db)
     a.chat_id = 6 
     a.progress = 2
     a.time_score = "123456"

     future = a.insertThis()
     ioloop.add_future(future, lambda x: ioloop.stop())
     ioloop.start()
     print(future.result())
    
     
     future = a.selectThis()
     ioloop.add_future(future, lambda x: ioloop.stop())
     ioloop.start()
     print(future.result())


#print(user.execute(user.selectThis()))

main()
