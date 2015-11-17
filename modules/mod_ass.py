from modules.module_base import ModuleBase
import urllib.request
import json


class ModuleAss(ModuleBase):

    def __init__(self, bot):
        ModuleBase.__init__(self, bot)
        self.name = "ModuleAss"
        self.Url = "http://api.obutts.ru/noise/1";
        self.mediaUrl = "http://media.obutts.ru/"

    def notify_command(self, message_id, from_attr, date, chat, commandName, commandStr):
        if commandName == "ass":
            response = urllib.request.urlopen(self.Url)
            str_response = response.read().decode('utf-8')
            objJSON = json.loads(str_response)
            print(objJSON)
            imgPath = objJSON[0]['preview']
            if len(imgPath) > 0:
                urllib.request.urlretrieve(self.mediaUrl + "/" + imgPath, "out.jpg")
                self.bot.sendPhoto(chat["id"], "out.jpg", "Et un petit cul pour monsieur !")

    def get_commands(self):
        return [
            ("ass", "Random pretty ass on demand"),
        ]

