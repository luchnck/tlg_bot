#! /usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import requests
import tornado.web
import logging
from tornado import gen,log,options,httpclient
from tornado.options import define, options, parse_config_file
import momoko
from pprint import pprint
from inspect import getmembers
import json
from snaql.factory import Snaql

sys.path.append(os.path.abspath('routes'))
sys.path.append(os.path.abspath('models'))

from routes.routes import mainHandler

logging.basicConfig(level = logging.DEBUG)

define("token", default="basictoken")
define("url", default="basicurl")
define("myurl", default="basicurl")
define("serverurl", default="basicurl")
define("serverport", default="defaultport")
define("dsn", default="basicdsn")
#BOT_TOKEN = '235765450:AAGWZ5N-0OFylLjOpmYXUQfBZlI-Cd0y-28'
#URL = "https://api.telegram.org/bot%s/" % BOT_TOKEN
#MyURL = "https://54.199.228.119/"
#URL = "http://localhost:8001/"
#dsn = "user=postgres password=postgres dbname=qa_bot host=localhost port=5432"


class app(tornado.web.Application):

    def __init__(self, *args, **kwargs):
        super(app,self).__init__(*args,**kwargs)
        self._db_templates = ''

    def sendedMessage(self,response):
        logging.debug('Message sended successifilly response is %s' % response)
    
    @gen.coroutine
    def sendMessage(self,response):
        logging.debug('Message will be sent on url %s' % options.url)
        httpClient = tornado.httpclient.AsyncHTTPClient()
        postRequest = tornado.httpclient.HTTPRequest( url= options.url % options.token + "sendMessage",
                                                      method="POST", 
                                                      body=json.dumps(response), 
                                                      headers=tornado.httputil.HTTPHeaders( {
                                                                                             "content-type": "application/json",
                                                                                             "method": "POST"
                                                                                             } ) 
                                                    )
        response = yield httpClient.fetch( postRequest )
        self.sendedMessage(response)
   
    @gen.coroutine 
    def sendLocalMessage(self,response,time):
        yield gen.sleep(time)
        logging.debug('Message will be sent on url %s' % options.serverurl)
        httpClient = tornado.httpclient.AsyncHTTPClient()
        postRequest = tornado.httpclient.HTTPRequest( url= options.serverurl,
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
        parse_config_file(os.path.abspath('')+'/options.conf')
        tornado.httpclient.AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")
        ioloop = tornado.ioloop.IOLoop.instance() 
        api = requests.Session()
        application = app([
            (r"/", mainHandler),
        ])

        url = options.url % options.token + "setWebhook?url=%s" % options.myurl
        files = {'certificate' : open('/usr/share/nginx/qa_bot/qa_bot_company.pem','rb')}
        set_hook = api.post(url, files = files)
        if set_hook.status_code != 200:
               logging.error("Cant set hook: %s. Quit", set_hook.text)
               exit(1)
        
        
        application.db = momoko.Pool(
            dsn=options.dsn,
            size=1,
            max_size=3,
            ioloop=ioloop,
            setsession=("SET TIME ZONE UTC",),
            raise_connect_errors=False,
        )

        application._db_templates = Snaql('models/','queries').load_queries('model.sql')

        future = application.db.connect()
        ioloop.add_future(future, lambda f: ioloop.stop())
        ioloop.start()
        future.result()

        application.listen(options.serverport)
        ioloop.start()



