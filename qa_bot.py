#! /usr/bin/python
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

logging.basicConfig(level = logging.DEBUG)

BOT_TOKEN = '235765450:AAGWZ5N-0OFylLjOpmYXUQfBZlI-Cd0y-28'
URL = "https://api.telegram.org/bot%s/" % BOT_TOKEN
MyURL = "https://54.199.228.119/"
#URL = "http://localhost:8001/"

dsn = "user=postgres password=postgres dbname=qa_bot host=localhost port=5432"


CMD = {}
not_found = '/help'

def start(arguments, message):
        response = {'chat_id': message['chat']['id']}
        result = ["Hey, %s!" % message["from"].get("first_name"),tr("\rЗдесь будем выдавать задания")]
        for command in CMD:
                result.append(command)
        response['text'] = "\n\t".join(result)
        return response

class app(tornado.web.Application):

    def sendedMessage(self,response):
        logging.debug('Message sended successifilly response is %s' % response)
    
    @gen.coroutine
    def sendMessage(self,response):
        logging.debug('Message will be sent on url %s' % URL)
        httpClient = tornado.httpclient.AsyncHTTPClient()
        postRequest = tornado.httpclient.HTTPRequest( url= URL + "sendMessage",method="POST", body=json.dumps(response), headers=tornado.httputil.HTTPHeaders( {"content-type": "application/json","method": "POST"} ) )
        response = yield httpClient.fetch( postRequest )
        self.sendedMessage(response)

class TestHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    @gen.coroutine
    def post(self):
        update = tornado.escape.json_decode(self.request.body)

        cursor = yield self.db.execute('SELECT * FROM public.qa')
        request =  {
                                  "text" : "Query results: %s" % cursor.fetchall(),
                                  "chat_id" : update['message']['chat']['id'],
                   }
        response = yield self.application.sendMessage(request)
        self.finish()       

class Handler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    @gen.coroutine
    def post(self):
#        try:
            logging.debug("Got request: %s" % self.request.body)
            update = tornado.escape.json_decode(self.request.body)
            message = update['message']
            text = message.get('text')
            logging.debug("message is: %s" % text)
            if text:
                logging.info("MESSAGE\t%s\t%s" % (message['chat']['id'], text))
                if (text[0] == '/'):
                    command = text
                    arguments = ''
                    if (text.find(' ') == True):
                        command, arguments = text.split(" ", 1)
#                    if (CMD.has_key(command)):i
# ToDo:
# сделать словари парсинга команд 
# 
                        response = CMD.get(command)(arguments,message)
                    else:
                        response = CMD.get(not_found)(arguments,message)
                    logging.info("REPLY\t%s\t%s" % (message['chat']['id'], response))
                    yield self.application.sendMessage(response)
            self.finish() 
#        except Exception as e:
#            logging.warning(str(e))




def send_reply(response):
        if 'text' in response:
            api.post(URL + "sendMessage", data=response)

def help_message(arguments, message):
        response = {'chat_id': message['chat']['id']}
        result = ["Hey, %s!" % message["from"].get("first_name"),
              "\rI can accept only these commands:"]
        for command in CMD:
                result.append(command)
        response['text'] = "\n\t".join(result)
        return response


if __name__ == '__main__':
        tornado.httpclient.AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")
        ioloop = tornado.ioloop.IOLoop.instance() 
        api = requests.Session()
        application = app([
            (r"/connectiontest", TestHandler),
            (r"/", TestHandler),
        ])

        CMD['/help'] = help_message
        CMD['/start'] = start
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
