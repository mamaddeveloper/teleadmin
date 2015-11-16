from http.server import BaseHTTPRequestHandler, HTTPServer
import ssl
import json
import logging
import requests
import uuid
import threading
import time

class HandlerMaison(BaseHTTPRequestHandler):
    logger = logging.getLogger("HandlerMaison")
    #server stuff
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        return self.do_POST()

    def do_POST(self):
        try:
            print(self.path)
            print(Server.Path)
            if self.path == Server.Path:
                self.logger.info("Recieve post")
                print ("THE POST")
                jsonListString = []
                #for line in self.rfile:
                #    jsonListString.append(str(line, 'utf-8'))
                #    print ("line:"+str(line, 'utf-8'))
                print ("THE END")
                #jsonObject = json.loads(''.join(jsonListString))
                #print(jsonObject)
                self.ok()
            else:
                self.error_access()
        except:
            self.logger.exception("Handler error", exc_info=True)
            self.error()

    def error_access(self):
        self.send_response(403)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(bytes("Access denied", "utf-8"))

    def error(self):
        self.send_response(500)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(bytes("Server error", "utf-8"))

    def ok(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(bytes("Ok", "utf-8"))


class Server:
    Bot = None
    Path = None

    def __init__(self, bot, public, private):
        self.logger = logging.getLogger(type(self).__name__)
        Server.Bot = bot
        self.__public_path = public
        self.__private_path = private
        self.key = None
        self.url = None
        
    def run(self, server_class=HTTPServer, port=8443):
        try:
            self.logger.info("Starting getting public ip")
            #response = json.loads(requests.get("https://api.ipify.org/?format=json").text)
            #ip = response["ip"]
            ip = "fa18swiss.no-ip.biz"
            self.logger.warning("Ip : %s", ip)
            self.key = str(uuid.uuid4())
            self.logger.warning("Key : '%s'", self.key)
            Server.Path = "/%s/" % self.key
            self.url = "https://%s:%d%s" % (ip, port, self.Path)
            self.logger.warning("Url : '%s'", self.url)
            self.logger.info("Init server on port %d", port)
            server_address = ('', port)
            httpd = HTTPServer(server_address, HandlerMaison)

            # SSL
            httpd.socket = ssl.wrap_socket( httpd.socket,
                                            server_side=True,
                                            certfile=self.__public_path,
                                            keyfile=self.__private_path,
                                            ssl_version=ssl.PROTOCOL_TLSv1_2)

            self.logger.info("Bot starting")
            self.Bot.start()
            self.logger.info("Bot started")
            self.logger.info("Starting")
            thread = WebHootSetter(self.Bot, self.url, self.__public_path)
            thread.start()
            httpd.serve_forever()
            self.logger.info("Started")
        except KeyboardInterrupt:
            self.logger.info("KeyboardInterrupt")
        except:
            self.logger.exception("Server fail", exc_info=True)
        self.logger.info("Stoppring bot")
        self.Bot.setWebhook("")
        self.Bot.stop()
        self.logger.info("Stopped bot")
    def setWebhook(self):
        self.Bot.setWebhook(self.url, self.__public_path)


class WebHootSetter(threading.Thread):
    def __init__(self, bot, url, certificate):
        threading.Thread.__init__(self)
        self.__bot = bot
        self.__url = url
        self.__certificate = certificate
        #self.__certificate = None
        self.logger = logging.getLogger("WebHootSetter")

    def run(self):
        self.logger.debug("Start wait")
        time.sleep(1)
        self.logger.debug("End wait")
        self.__bot.setWebhook(self.__url, self.__certificate)
        self.logger.debug("End set")
