import logging
import tornado.web

CMD = {
        '/start': 'start',
        '/help' : 'help_message',
}

not_found = '/help'

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
                    command, arguments = text.split(" ", 1)
                    response = CMD.get(command, not_found)(arguments, message)
                    logging.info("REPLY\t%s\t%s" % (message['chat']['id'], response))
                    send_reply(response)
#        except Exception as e:
            logging.warning(str(e))
