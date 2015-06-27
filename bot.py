import requests
import time
import datetime
from update import Update
from message import Message
from collections import Iterator


class Bot:
    REQUEST_BASE="https://api.telegram.org/bot"
    def __init__(self, token, directoryName):
        self.directoryName = directoryName
        self.token = token
        self.last_update_id = 0
        self.listModules = []
        self.getListModules()
    
    def start(self, useWebhook=True, sleepingTime=2):
        lines = []
        self.useWebhook = useWebhook
        self.shouldStopPolling = False
        with open(self.directoryName+"/updates_log", 'r') as f:
            lines.extend(f.readlines())
        for line in lines:
            if self.token in line:
                self.last_update_id = int(line.split(":")[-1])
                break
        if not useWebhook:
            while not self.shouldStopPolling:
                self.getUpdates()
                time.sleep(sleepingTime)
 
    def stop(self):
        self.shouldStopPolling=True
        lines = []
        with open(self.directoryName+"/updates_log", 'r') as f:
            lines.extend(f.readlines())
            
        lines = [line for line in lines if self.token not in line]
        lines.append(self.token + ":" +str(self.last_update_id))
        
        with open(self.directoryName+"/updates_log", 'w') as f:
            for line in lines:
                f.write(line)
                f.write("\n")
                
            
    def notify(listUpdates):
        sorted(listUpdates, key= lambda x: x.update_id)
        if len(listUpdates) > 0:
            self.last_update_id = listUpdates[-1].update_id+1
        for update in listUpdates:
            for module in self.listModules:
                module.notify(update)
                
    #should not be used, since we're working using a webhook
    def getUpdates(self, purge = False):
        r = self.getJson("getUpdates", offset=self.last_update_id)
        listUpdates = []
        for update in r["result"]:
            listUpdates.append(Update(update))
            print(update)
        sorted(listUpdates, key= lambda x: x.update_id)
        if len(listUpdates) > 0:
            self.last_update_id = listUpdates[-1].update_id+1
        if not purge:
            for update in listUpdates:
                for module in self.listModules:
                    module.notify(update)
        
    def answerToMessage(self, text, message):
        if message is not None:
            r = self.getJson("sendMessage", chat_id=message.chat["id"], text=text, disable_web_page_preview="true")
            
    
    def getListModules(self):
        print ("Loading modules: ")
        self.listModules = []
        import os
        modules = [os.path.splitext(f)[0] for f in os.listdir("modules") if f.startswith("mod_") and f.endswith(".py")]
        for a in modules:
            try:
                module = __import__("modules.%s" % a, globals(), locals(), fromlist=["*"])
                # What goes here?
                # let's try to grab and instanciate objects
                for item_name in dir(module):
                    try:
                       newModule = getattr(module, item_name)()
                       # here we have a newModule that is the instanciated class, do what you want with ;)
                       self.listModules.append(newModule)
                    except:
                       pass
            except ImportError:
                pass
        for module in self.listModules:
            print(module.getName())
            module.setBot(self)
        
    #API methods
    def getMe(self):
        r = self.getJson("getMe")
        return r
        
    def sendMessage(self, text, chat_id, disable_web_page_preview="true", reply_to_message_id=None, reply_markup=None):
        r = self.getJson("sendMessage", chat_id=chat_id, text=text, disable_web_page_preview=disable_web_page_preview, reply_to_message_id=reply_to_message_id, reply_markup=reply_markup)
        
    def forwardMessage(self, chat_id, from_chat_id, message_id):
        r = self.getJson("forwardMessage", chat_id=chat_id, from_chat_id=from_chat_id, message_id=message_id)
        
    def setWebhook(self, url):
        r = self.getJson("setWebhook", url=url)
        
    #end API methods
        
    def getJson(self, requestName, **parameters):
        requestString = Bot.REQUEST_BASE+self.token+"/"+requestName+"?"
        for key in parameters:
            if parameters[key] is not None:
                requestString = requestString+key+"="+str(parameters[key])+"&"
        if requestString.endswith("&") or requestString.endswith("?"):
            requestString = requestString[:-1]
        print(str(datetime.datetime.now().time()) + requestString)
        r = requests.get(requestString)
        return r.json()
        
if __name__ == "__main__":
    token = None
    with open("botTest/token", 'r') as f:
        token = f.readline()[:-1]
    bot = Bot(token, "botTest")