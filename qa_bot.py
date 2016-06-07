#! /usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import requests
import tornado.web
import logging
from tornado import gen,log,options,httpclient
import momoko
from pprint import pprint
from inspect import getmembers
import json

sys.path.append(os.path.abspath('routes'))
sys.path.append(os.path.abspath('models'))

from routes.routes import mainHandler


logging.basicConfig(level = logging.DEBUG)

BOT_TOKEN = '235765450:AAGWZ5N-0OFylLjOpmYXUQfBZlI-Cd0y-28'
URL = "https://api.telegram.org/bot%s/" % BOT_TOKEN
MyURL = "https://54.199.228.119/"
#URL = "http://localhost:8001/"

dsn = "user=postgres password=postgres dbname=qa_bot host=localhost port=5432"


class app(tornado.web.Application):

    def sendedMessage(self,response):
        logging.debug('Message sended successifilly response is %s' % response)
    
    @gen.coroutine
    def sendMessage(self,response):
        logging.debug('Message will be sent on url %s' % URL)
        httpClient = tornado.httpclient.AsyncHTTPClient()
        postRequest = tornado.httpclient.HTTPRequest( url= URL + "sendMessage",
                                                      method="POST", 
                                                      body=json.dumps(response), 
                                                      headers=tornado.httputil.HTTPHeaders( {
                                                                                             "content-type": "application/json",
                                                                                             "method": "POST"
                                                                                             } ) 
                                                    )
        response = yield httpClient.fetch( postRequest )
        self.sendedMessage(response)

if __name__ == '__main__':
        tornado.httpclient.AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")
        ioloop = tornado.ioloop.IOLoop.instance() 
        api = requests.Session()
        application = app([
            (r"/", mainHandler),
        ])

        url = URL + "setWebhook?url=%s" % MyURL
        files = {'certificate' : open('/usr/share/nginx/qa_bot/qa_bot_company.pem','rb')}
        set_hook = api.post(url, files = files)
        if set_hook.status_code != 200:
               logging.error("Cant set hook: %s. Quit", set_hook.text)
               exit(1)
        
        
        application.db = momoko.Pool(
            dsn=dsn,
            size=1,
            max_size=3,
            ioloop=ioloop,
            setsession=("SET TIME ZONE UTC",),
            raise_connect_errors=False,
        )

        future = application.db.connect()
        ioloop.add_future(future, lambda f: ioloop.stop())
        ioloop.start()
        future.result()

        application.listen(8001)
        ioloop.start()
