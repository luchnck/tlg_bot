#!/bin/bash python 
# -*- coding: utf-8 -*-

import psycopg2
import momoko
from tornado.ioloop import IOLoop
ioloop = IOLoop.instance()

dsn="user=postgres password=postgres dbname=qa_bot host=localhost port=5432"
conn = momoko.Pool(dsn=dsn)
future = conn.connect()
ioloop.add_future(future, lambda x: ioloop.stop())
ioloop.start()
future.result()  # raises exception on connection error


future = conn.execute("SELECT * FROM public.test_table")
ioloop.add_future(future, lambda x: ioloop.stop())
ioloop.start()
cursor = future.result()
rows = cursor.fetchall()
print(rows)
