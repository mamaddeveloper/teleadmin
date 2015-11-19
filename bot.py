import logging
import os.path
import queue
import requests
import stoppable_thread
import time
from update import Update
from tools.commandParser import CommandParser
from tools.admin import AdminAll

class Bot(stoppable_thread.StoppableThread):
    REQUEST_BASE = "https://api.telegram.org/bot"
    MESSAGE_TEXT_FIELD = "text"
    LIST_MESSAGE_MANDATORY_FIELDS = ["message_id", "from_attr", "date", "chat"]
    LIST_MESSAGE_OPTIONNAL_FIELDS = ["reply_to_message", "audio", "document", "photo", "sticker", "video",
                                     "contact", "location", "new_chat_participant", "left_chat_participant",
                                     "new_chat_title", "new_chat_photo", "delete_chat_photo", "group_chat_created"]
    LIST_MESSAGE_FORWARD_FIELDS = ["forward_from", "forward_date"]

    def __init__(self, token, directoryName):
        super(Bot, self).__init__()
        self.logger = logging.getLogger(__name__)
        self.listCommands = None
        self.listCommandsWithDesc = None
        self.commandParser = None
        self.admin = AdminAll()
        self.directoryName = directoryName
        self.token = token
        self.last_update_id = 0
        self.last_update_id_path = "%s/last_update_id" % self.directoryName
        self.listModules = []
        self.listExclusion = ['mod_spelling.py','mod_chatterbot.py']
        self.loadLocalExclusion()
        self.getListModules()
        self.queue = queue.Queue()

        #init command list
        self.logger.debug("listCommands %s", repr(self.listCommands))
        self.commandParser = CommandParser(self.listCommands)
        if os.path.exists(self.last_update_id_path):
            with open(self.last_update_id_path, 'r') as f:
                try:
                    self.last_update_id = int(f.readline().strip())
                except ValueError:
                    pass

    def save_last_update_id(self):
        with open(self.last_update_id_path, 'w') as f:
            f.write(str(self.last_update_id))

    def stop(self):
        self.logger.info("Stopping")
        super(Bot, self).stop()
        self.logger.info("Stopping modules")
        for module in self.listModules:
            module.stop()
        self.logger.info("Stopped")

    def join(self, timeout=None):
        self.logger.info("Joining")
        super(Bot, self).join(timeout)
        self.logger.info("Thread joinied")
        self.queue.join()
        self.logger.info("Joinied")

    def run(self):
        while self.can_loop():
            try:
                self.logger.debug("Geting in queue")
                update = self.queue.get(timeout=5)
                self.logger.debug("Get in queue")
                self.process_update(update)
            except queue.Empty:
                self.logger.debug("Queue empty")

    def add_updates(self, list_updates):
        if len(list_updates) > 0:
            self.last_update_id = list_updates[-1].update_id + 1
            self.save_last_update_id()
            for update in list_updates:
                self.queue.put_nowait(update)

    @staticmethod
    def checkForAttribute(object, attribute):
        exists = getattr(object, attribute, None)
        return exists is not None

    def process_update(self, update):
        message = update.message
        if Bot.checkForAttribute(message, Bot.MESSAGE_TEXT_FIELD):
            cmd = self.commandParser.parse(message.text)
            if cmd.isValid :
                self.logger.info("cmd %s", message.text)
                if not cmd.isKnown:
                    self.sendMessage("Command '%s' unknown !" % cmd.command, message.chat["id"])
                    return
            for module in self.listModules:
                try:
                    if cmd.isValid:
                        module.notify_command(message.message_id, message.from_attr, message.date, message.chat, cmd.command, cmd.args)
                    else:
                        module.notify_text(message.message_id, message.from_attr, message.date, message.chat, message.text)
                except:
                    self.logger.exception("Module '%s' crash (notify_text/notify_command)", module.name, exc_info=True)
            return
        for forwardField in Bot.LIST_MESSAGE_FORWARD_FIELDS:
            if Bot.checkForAttribute(message, forwardField):
                for module in self.listModules:
                    try:
                        module.notify_forward(message.message_id, message.from_attr, message.date, message.chat,
                                              message.forward_from, message.forward_date)
                    except:
                        self.logger.exception("Module '%s' crash (notify_forward)", module.name, exc_info=True)
                return
        for optionnalField in Bot.LIST_MESSAGE_OPTIONNAL_FIELDS:
            if Bot.checkForAttribute(message, optionnalField):
                for module in self.listModules:
                    try:
                        toCall = getattr(module, "notify_" + optionnalField)
                        toCall(message.message_id, message.from_attr, message.date, message.chat,
                           getattr(message, optionnalField))
                    except:
                        self.logger.exception("Module '%s' crash (toCall)", module.name, exc_info=True)
                return

    def getUpdateFromApi(self):
        r = self.getJson("getUpdates", offset=self.last_update_id)
        list_updates = list([Update(u) for u in r["result"]])
        sorted(list_updates, key=lambda x: x.update_id)
        return list_updates

    def getUpdates(self):
        list_updates = self.getUpdateFromApi()
        self.add_updates(list_updates)

    def purge(self):
        self.setWebhook("")
        list_updates = self.getUpdateFromApi()
        if len(list_updates) > 0:
            self.last_update_id = max([x.update_id for x in list_updates]) + 1
            self.save_last_update_id()

    def answerToMessage(self, text, message):
        if message is not None:
            r = self.getJson("sendMessage", chat_id=message.chat["id"], text=text, disable_web_page_preview="true")
    def loadLocalExclusion(self):
        import os.path
        file = "botTest/modules_exclude_local"
        if os.path.exists(file):
            with open(file, 'r') as f:
                for line in f:
                    self.listExclusion.append(line.rstrip())
        self.logger.info("listExclusion = %s", self.listExclusion)

    def getListModules(self):
        self.logger.info("Loading modules")
        self.listModules = []
        self.listCommandsWithDesc = []
        import os

        modules = [os.path.splitext(f)[0] for f in os.listdir("modules") if
                   f.startswith("mod_") and f.endswith(".py") and (not f in self.listExclusion)]
        for a in modules:
            try:
                module = __import__("modules.%s" % a, globals(), locals(), fromlist=["*"])
                # What goes here?
                # let's try to grab and instanciate objects
                for item_name in dir(module):
                    try:
                        if "Module" in item_name and not "ModuleBase" in item_name:
                            self.logger.debug("Loading module %s", item_name)
                            newModule = getattr(module, item_name)(self)
                            # here we have a newModule that is the instanciated class, do what you want with ;)
                            self.listModules.append(newModule)
                            self.listCommandsWithDesc.extend(newModule.get_commands())
                            self.logger.debug("Loaded module %s", item_name)
                    except:
                        self.logger.exception("Fail to load module %s", item_name, exc_info=True)
            except:
                self.logger.exception("Fail to load module %s", a, exc_info=True)

        self.listCommandsWithDesc.sort(key=lambda tup: tup[0])
        self.listCommands = tuple([tup[0] for tup in self.listCommandsWithDesc])

    # API methods
    def getMe(self):
        r = self.getJson("getMe")
        return r

    def sendMessage(self, text, chat_id, disable_web_page_preview="true", reply_to_message_id=None, reply_markup=None):
        self.getJson("sendMessage", chat_id=chat_id, text=text, disable_web_page_preview=disable_web_page_preview,
                     reply_to_message_id=reply_to_message_id, reply_markup=reply_markup)

    def forwardMessage(self, chat_id, from_chat_id, message_id):
        self.getJson("forwardMessage", chat_id=chat_id, from_chat_id=from_chat_id, message_id=message_id)

    def setWebhook(self, url, certificate=None):
        if certificate:
            #with open(certificate, "r") as f:
            #    certificate = "".join([l.strip() for l in f.readlines()])
            certificate =  {"certificate":(certificate,open(certificate, "rb"))}
        self.postFile("setWebhook", data={"url":url}, files=certificate)

    def sendDocument(self, chat_id, file_path):
        self.postFile("sendDocument", data={"chat_id": chat_id}, files={"document": (file_path, open(file_path, "rb"))})

    def sendPhoto(self, chat_id, photoPath, caption=None, reply_to_message_id=None, reply_markup=None):
        self.sendPhotoDict(chat_id, photoPath, caption=caption, reply_to_message_id=reply_to_message_id,
                           reply_markup=reply_markup)

    def sendPhotoDict(self, chat_id, photoPath, **optionnalParameters):
        data = {}
        for key in optionnalParameters:
            if optionnalParameters[key] is not None:
                data[key] = optionnalParameters[key]

        # data = {key:value for (key, value) in optionnalParameters if value is not None}

        data["chat_id"] = chat_id
        files = {'photo': (photoPath, open(photoPath, 'rb'))}
        self.postFile("sendPhoto", data=data, files=files)

    def sendPhotoUrl(self, chat_id, photo_url, capiton=None, reply_to_message_id=None, reply_markup=None):
        try:
            response = requests.get(photo_url, stream=True, timeout=5)
            with open("out.jpg", "wb") as f:
                for block in response.iter_content(1024):
                    f.write(block)
            self.sendPhoto(chat_id, "out.jpg", capiton, reply_to_message_id, reply_markup)
        except:
            self.logger.exception("Fail to download and send image %s", photo_url, exc_info=True)
            return False
        return True

    def sendSticker(self, chat_id, sticker):
        self.getJson("sendSticker", chat_id=chat_id, sticker=sticker)

    def setReplyKeyboardMarkup(self, keyboard):
        self.getJson("ReplyKeyboardMarkup", keyboard)

    # end API methods



    def postFile(self, requestName, files, data):
        requestString = Bot.REQUEST_BASE + self.token + "/" + requestName
        self.logger.info("postfile %s %s", requestString, data)
        response = requests.post(requestString, data=data, files=files)
        self.logger.info("postfile response %s %s", response, response.json())

    # creates a request "requestName", with each key, value pair from parameters as parameters
    def getJson(self, requestName, **parameters):
        try:
            while True:
                url = "%s%s/%s" % (Bot.REQUEST_BASE, self.token, requestName)
                self.logger.info("send %s %s", url, parameters)
                r = requests.post(url, parameters)
                jsonResponse = r.json()
                self.logger.info("recieve %s", jsonResponse)
                if jsonResponse['ok']:
                    return jsonResponse
                else:
                    self.logger.error("No ok response %s", jsonResponse)
                    if jsonResponse["error_code"] != 429:
                        return {"result": []}
                    self.logger.warning("Wait + loop")
                    time.sleep(30)
        except:
            self.logger.exception("fail to get response", exc_info=True)
            return {"result": []}
