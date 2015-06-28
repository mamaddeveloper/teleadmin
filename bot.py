import requests
import time
import datetime
from update import Update
from message import Message
from collections import Iterator


class Bot:
    REQUEST_BASE = "https://api.telegram.org/bot"
    LIST_MESSAGE_MANDATORY_FIELDS = ["message_id","from_attr","date","chat"]
    LIST_MESSAGE_OPTIONNAL_FIELDS = ["reply_to_message","text","audio","document","photo","sticker","video","contact","location","new_chat_participant","left_chat_participant","new_chat_title","new_chat_photo","delete_chat_photo","group_chat_created"]
    LIST_MESSAGE_FORWARD_FIELDS = ["forward_from","forward_date"]
    
    

    def __init__(self, token, directoryName):
        self.directoryName = directoryName
        self.token = token
        self.last_update_id = 0
        self.listModules = []
        self.getListModules()
        
        self.initCommandList()
        self.useWebhook = None
        self.shouldStopPolling = None

    def start(self, useWebhook=True, sleepingTime=2):
        lines = []
        self.useWebhook = useWebhook
        self.shouldStopPolling = False
        with open(self.directoryName + "/updates_log", 'r') as f:
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
        self.shouldStopPolling = True
        lines = []
        with open(self.directoryName + "/updates_log", 'r') as f:
            lines.extend(f.readlines())

        lines = [line for line in lines if self.token not in line]
        lines.append(self.token + ":" + str(self.last_update_id))

        with open(self.directoryName + "/updates_log", 'w') as f:
            for line in lines:
                f.write(line)
                f.write("\n")
                
    def initCommandList(self):
        listStringCommands = None
        with open("commandlist", 'r') as f:
            listStringCommands = f.readlines()
        self.listCommands = [item.split(" ")[0] for item in listStringCommands if item != "" and item != None]
    
    @staticmethod
    def checkForAttribute(object, attribute):
        exists = getattr(object, attribute, None)
        return exists is not None
    
    def notify(self, listUpdates):
        sorted(listUpdates, key=lambda x: x.update_id)
        if len(listUpdates) > 0:
            self.last_update_id = listUpdates[-1].update_id + 1
        for update in listUpdates:
            for forwardField in Bot.LIST_MESSAGE_FORWARD_FIELDS:
                if Bot.checkForAttribute(update.message, forwardField):
                    message = update.message
                    for module in self.listModules:
                        module.notify_forward(message.message_id, message.from_attr, message.date, message.chat, message.forward_from, message.forward_date)
                    return
            for optionnalField in Bot.LIST_MESSAGE_OPTIONNAL_FIELDS:
                if Bot.checkForAttribute(update.message, optionnalField):
                    message = update.message
                    for module in self.listModules:
                        toCall = getattr(module, "notify_"+optionnalField)
                        toCall(message.message_id, message.from_attr, message.date, message.chat, getattr(message, optionnalField))
                    return
                    
    # should not be used, since we're working using a webhook
    def getUpdates(self, purge=False):
        r = self.getJson("getUpdates", offset=self.last_update_id)
        listUpdates = []
        for update in r["result"]:
            listUpdates.append(Update(update))
        if not purge:
            self.notify(listUpdates)

    def answerToMessage(self, text, message):
        if message is not None:
            r = self.getJson("sendMessage", chat_id=message.chat["id"], text=text, disable_web_page_preview="true")

    def getListModules(self):
        print("Loading modules: ")
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
                        if "Module" in item_name and not "ModuleBase" in item_name:
                            newModule = getattr(module, item_name)(self)
                            # here we have a newModule that is the instanciated class, do what you want with ;)
                            self.listModules.append(newModule)
                    except Exception as e:
                        print(e)
            except ImportError as e:
                print (e)

    # API methods
    def getMe(self):
        r = self.getJson("getMe")
        return r

    def sendMessage(self, text, chat_id, disable_web_page_preview="true", reply_to_message_id=None, reply_markup=None):
        self.getJson("sendMessage", chat_id=chat_id, text=text, disable_web_page_preview=disable_web_page_preview,
                         reply_to_message_id=reply_to_message_id, reply_markup=reply_markup)

    def forwardMessage(self, chat_id, from_chat_id, message_id):
        self.getJson("forwardMessage", chat_id=chat_id, from_chat_id=from_chat_id, message_id=message_id)

    def setWebhook(self, url):
        self.getJson("setWebhook", url=url)
        
    def sendPhoto(self, chat_id, photoPath, caption=None, reply_to_message_id=None, reply_markup=None):
        #self.getJson("sendPhoto", chat_id=chat_id, photo=photo, caption=caption, reply_to_message_id=reply_to_message_id, reply_markup=reply_markup)
        #self.postFile("sendPhoto", photo, chat_id=chat_id, caption=caption, reply_to_message_id=reply_to_message_id, reply_markup=reply_markup)
        self.sendPhotoDict(chat_id, photoPath, caption=caption, reply_to_message_id=reply_to_message_id, reply_markup=reply_markup)
    def sendPhotoDict(self, chat_id, photoPath, **optionnalParameters):
        data= {}
        for key in optionnalParameters:
            if optionnalParameters[key] is not None:
                data[key] = optionnalParameters[key]
        
        #data = {key:value for (key, value) in optionnalParameters if value is not None}
        
        data["chat_id"] = chat_id
        files = {'photo':(photoPath, open(photoPath, 'rb'))}
        self.postFile("sendPhoto", data=data, files = files)

    def setReplyKeyboardMarkup(self, keyboard):
        self.getJson("ReplyKeyboardMarkup", keyboard)
    # end API methods
    
    

    def postFile(self, requestName, files, data):
        requestString = Bot.REQUEST_BASE + self.token + "/" + requestName
        requests.post(requestString, data=data, files=files)
    
    #creates a request "requestName", with each key, value pair from parameters as parameters
    def getJson(self, requestName, **parameters):
        requestString = Bot.REQUEST_BASE + self.token + "/" + requestName + "?"
        for key in parameters:
            if parameters[key] is not None:
                requestString = requestString + key + "=" + str(parameters[key]) + "&"
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