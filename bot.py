import logging
import os
import os.path
import queue
import requests
import stoppable_thread
import time
from modules import module_base
from tools.admin import AdminAll
from tools.commandParser import CommandParser
from tools.isType import is_type


class Bot(stoppable_thread.StoppableThread):
    REQUEST_BASE = "https://api.telegram.org/bot"
    MESSAGE_TEXT_FIELD = "text"
    LIST_MESSAGE_OPTIONAL_FIELDS = ["reply_to_message", "audio", "document", "photo", "sticker", "video",
                                     "contact", "location", "new_chat_participant", "left_chat_participant",
                                     "new_chat_title", "new_chat_photo", "delete_chat_photo", "group_chat_created"]
    LIST_MESSAGE_FORWARD_FIELDS = ["forward_from", "forward_date"]

    def __init__(self, token, directoryName):
        super(Bot, self).__init__()
        self.name = "Thread-Bot"
        self.logger = logging.getLogger(__name__)
        self.listCommands = None
        self.listCommandsWithDesc = None
        self.commandParser = None
        self.admin = AdminAll()
        self.directoryName = directoryName
        self.token = token
        self.last_update_id = 0
        self.queue = queue.Queue()
        self.last_update_id_path = "%s/last_update_id" % self.directoryName
        self.listModules = []

        self.listExclusion = []
        file = os.path.join(self.directoryName, "modules_exclude_local")
        if os.path.exists(file):
            with open(file, 'r') as f:
                for line in f:
                    self.listExclusion.append(line.rstrip())
        else:
            with open(file, 'w') as f:
                f.write("")
        self.logger.info("listExclusion = %s", self.listExclusion)

        if os.path.exists(self.last_update_id_path):
            with open(self.last_update_id_path, 'r') as f:
                try:
                    self.last_update_id = int(f.readline().strip())
                except ValueError:
                    pass

    def stop(self):
        self.logger.info("Stopping")
        super(Bot, self).stop()
        self.logger.info("Stopped")

    def run(self):
        self.__load_modules()
        #init command list
        while self.can_loop():
            try:
                self.logger.debug("Geting in queue")
                update = self.queue.get(timeout=15)
                self.logger.debug("Get in queue")
                self.__process_update(update)
            except queue.Empty:
                self.logger.debug("Queue empty")
        self.logger.info("Stopping modules")
        for module in self.listModules:
            module.stop()
        self.logger.info("Modules stopped")

    def add_updates(self, list_updates):
        self.__set_last_update_id(list_updates)
        for update in list_updates:
            self.queue.put_nowait(update)

    def __process_update(self, update):
        msg = update["message"]
        if Bot.MESSAGE_TEXT_FIELD in msg:
            text = msg[Bot.MESSAGE_TEXT_FIELD]
            cmd = self.commandParser.parse(text)
            if cmd.isValid :
                self.logger.info("cmd %s", text)
                if not cmd.isKnown:
                    self.sendMessage("Command '%s' unknown !" % cmd.command, msg["chat"]["id"])
                    return
            for module in self.listModules:
                try:
                    if cmd.isValid:
                        module.notify_command(msg["message_id"], msg["from"], msg["date"], msg["chat"], cmd.command, cmd.args)
                    else:
                        module.notify_text(msg["message_id"], msg["from"], msg["date"], msg["chat"], text)
                except:
                    self.logger.exception("Module '%s' crash (notify_text/notify_command)", module.name, exc_info=True)
            return
        for forward_field in Bot.LIST_MESSAGE_FORWARD_FIELDS:
            if forward_field in msg:
                for module in self.listModules:
                    try:
                        module.notify_forward(msg["message_id"], msg["from"], msg["date"], msg["chat"],
                                              msg["forward_from"], msg["forward_date"])
                    except:
                        self.logger.exception("Module '%s' crash (notify_forward)", module.name, exc_info=True)
                return
        for optional_field in Bot.LIST_MESSAGE_OPTIONAL_FIELDS:
            if optional_field in msg:
                method_name = "notify_%s" % optional_field
                for module in self.listModules:
                    try:
                        method = getattr(module, method_name)
                        method(msg["message_id"], msg["from"], msg["date"], msg["chat"], msg[optional_field])
                    except:
                        self.logger.exception("Module '%s' crash (%s)", module.name, method_name, exc_info=True)
                return

    def __set_last_update_id(self, list_updates):
        if len(list_updates) > 0:
            self.last_update_id = list_updates[-1]["update_id"] + 1
            with open(self.last_update_id_path, 'w') as f:
                f.write(str(self.last_update_id))

    def purge(self):
        self.setWebhook("")
        list_updates = self.getUpdates()
        self.__set_last_update_id(list_updates)

    def __load_modules(self):
        self.logger.info("Loading modules")
        self.listModules = []
        self.listCommandsWithDesc = []
        files = [os.path.splitext(f)[0] for f in os.listdir("modules")
                 if f.startswith("mod_") and f.endswith(".py") and f not in self.listExclusion]
        for file in files:
            try:
                modules = __import__("modules.%s" % file, globals(), locals(), fromlist=["*"])
                for module_name in [m for m in dir(modules)
                                    if m.startswith("Module") and not m.startswith("ModuleBase")]:
                    try:
                        self.logger.debug("Loading module %s", module_name)
                        module = getattr(modules, module_name)(self)
                        is_type(module_base.ModuleBase, module, module_name)
                        self.listModules.append(module)
                        self.listCommandsWithDesc.extend(module.get_commands())
                        self.logger.debug("Loaded module %s", module_name)
                    except:
                        self.logger.exception("Fail to load module %s", module_name, exc_info=True)
            except:
                self.logger.exception("Fail to load file %s", file, exc_info=True)

        self.listCommandsWithDesc.sort(key=lambda tup: tup[0])
        self.listCommands = tuple([tup[0] for tup in self.listCommandsWithDesc])
        self.logger.debug("listCommands %s", repr(self.listCommands))
        self.commandParser = CommandParser(self.listCommands)

    # API methods
    def getUpdates(self):
        r = self.__send_message("getUpdates", offset=self.last_update_id)
        list_updates = r["result"]
        sorted(list_updates, key=lambda x: x["update_id"])
        return list_updates

    def answerToMessage(self, text, message):
        if message is not None:
            self.__send_message("sendMessage", chat_id=message["chat"]["id"], text=text, disable_web_page_preview=True)

    def getMe(self):
        return self.__send_message("getMe")

    def sendMessage(self, text, chat_id, disable_web_page_preview=True, reply_to_message_id=None, reply_markup=None, parse_mode=None):
        self.__send_message("sendMessage", chat_id=chat_id, text=text, disable_web_page_preview=disable_web_page_preview,
                            reply_to_message_id=reply_to_message_id, reply_markup=reply_markup, parse_mode=parse_mode)

    def forwardMessage(self, chat_id, from_chat_id, message_id):
        self.__send_message("forwardMessage", chat_id=chat_id, from_chat_id=from_chat_id, message_id=message_id)

    def setWebhook(self, url, certificate=None):
        files = None
        if certificate:
            files = {'certificate': (certificate, open(certificate, 'rb'))}
        self.__send_file("setWebhook", data={"url":url}, files=files)

    def sendDocument(self, chat_id, file_path):
        self.__send_file("sendDocument", data={"chat_id": chat_id}, files={"document": (file_path, open(file_path, "rb"))})

    def sendPhoto(self, chat_id, photo_path, caption=None, reply_to_message_id=None, reply_markup=None):
        self.__send_file("sendPhoto", data={
            "chat_id": chat_id,
            "caption": caption,
            "reply_to_message_id": reply_to_message_id,
            "reply_markup": reply_markup,
        }, files={
            'photo': (photo_path, open(photo_path, 'rb'))
        })

    def sendPhotoUrl(self, chat_id, photo_url, capiton=None, reply_to_message_id=None, reply_markup=None):
        try:
            response = requests.get(photo_url, stream=True, timeout=5)
            with open("out.jpg", "wb") as f:
                for block in response.iter_content(1024):
                    f.write(block)
            self.sendPhoto(chat_id, "out.jpg", capiton, reply_to_message_id, reply_markup)
            return True
        except:
            self.logger.exception("Fail to download and send image %s", photo_url, exc_info=True)
        return False

    def sendSticker(self, chat_id, sticker):
        self.__send_message("sendSticker", chat_id=chat_id, sticker=sticker)

    def setReplyKeyboardMarkup(self, keyboard):
        self.__send_message("ReplyKeyboardMarkup", keyboard)
    # end API methods

    def __send_file(self, request_name, data, files):
        try:
            while True:
                url = "%s%s/%s" % (Bot.REQUEST_BASE, self.token, request_name)
                self.logger.info("send %s %s %s", url, data, files)
                r = requests.post(url, data=data, files=files)
                json_response = r.json()
                self.logger.info("recieve %s", json_response)
                if json_response['ok']:
                    return json_response
                else:
                    self.logger.error("No ok response %s", json_response)
                    if json_response["error_code"] != 429:
                        return json_response
                    self.logger.warning("Wait + loop")
                    time.sleep(30)
        except:
            self.logger.exception("fail to get response", exc_info=True)
        return {"result": [], "ok": False}

    # creates a request "request_name", with each key, value pair from parameters as parameters
    def __send_message(self, request_name, **data):
        return self.__send_file(request_name, data=data, files=None)
