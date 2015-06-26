from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
import ssl
from bot import Bot
from json import loads

class HandlerMaison(BaseHTTPRequestHandler):
    
    ''' must be called BEFORE run '''
    def addBot(self, bot):
        if self.listBots == None:
            self.listBots = []
        if not bot in self.listBots:
            self.listBots.append(bot)
            bot.start()
    
    #server stuff
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        print("GET RECEIVED")
        self.wfile.write(bytes("<html><body>Get Called <br> Ce site est parfaitement ouf</body></html>", "utf-8"))

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        print ("THE POST")
        jsonListString = []
        for line in self.rfile:
            jsonListString.append(str(line, 'utf-8'))
            print ("line:"+str(line, 'utf-8'))
        jsonObject = loads(''.join(jsonListString))
        print(jsonObject)
        
        
class Server():
    def __init__(self):
        self.handlerMaison = HandlerMaison
        
    def addBot(self, bot):
        #self.handlerMaison.addBot(bot)
        pass
        
    def run(self, server_class=HTTPServer, port=443):
        try:
            server_address = ('', port)
            httpd = server_class(server_address, self.handlerMaison)

            # SSL
            httpd.socket = ssl.wrap_socket( httpd.socket,
                                            server_side=True,
                                            certfile='ignore/server.pem',
                                            #keyfile='./ignore/cert.pem',
                                            ssl_version=ssl.PROTOCOL_TLSv1)

            print("Starting BotServer")
            httpd.serve_forever()
        except KeyboardInterrupt:
            for bot in self.handlerMaison.listBots:
                bot.stop()
            return
        for bot in self.handlerMaison.listBots:
            bot.stop()
    #end server stuff