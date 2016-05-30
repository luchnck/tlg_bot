#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import requests
import tornado.web
import logging

logging.basicConfig(level = logging.DEBUG)

BOT_TOKEN = '235765450:AAGWZ5N-0OFylLjOpmYXUQfBZlI-Cd0y-28'
URL = "https://api.telegram.org/bot%s/" % BOT_TOKEN
MyURL = "https://54.199.228.119/"

CMD = {}
not_found = '/help'

def start(arguments, message):
	response = {'chat_id': message['chat']['id']}
        result = ["Hey, %s!" % message["from"].get("first_name"),
              tr("\rЗдесь будем выдавать задания")]
        for command in CMD:
                result.append(command)
        response['text'] = "\n\t".join(result)
        return response

class Handler(tornado.web.RequestHandler):
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
                    response = CMD.get(command,not_found)(arguments,message)
                    logging.info("REPLY\t%s\t%s" % (message['chat']['id'], response))
                    send_reply(response)
#        except Exception as e:
#            logging.warning(str(e))


api = requests.Session()
application = tornado.web.Application([
    (r"/", Handler),
])




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

	CMD['/help'] = help_message
	CMD['/start'] = start
	url = URL + "setWebhook?url=%s" % MyURL
	files = {'certificate' : open('/usr/share/nginx/qa_bot/qa_bot_company.pem','rb')}
	set_hook = api.post(url, files = files)
	if set_hook.status_code != 200:
		logging.error("Cant set hook: %s. Quit", set_hook.text)
		exit(1)
	application.listen(8001)
	tornado.ioloop.IOLoop.current().start()
