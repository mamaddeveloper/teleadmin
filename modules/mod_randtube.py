from modules.module_base import ModuleBase
import urllib
import json
import random

class ModuleRandTube(ModuleBase):
    BASE_SEARCH = "youtube.com%2Fwatch%3Fv%3D"
    URL = 'https://ajax.googleapis.com/ajax/services/search/web?v=1.0&q='

    def __init__(self, bot):
        ModuleBase.__init__(self, bot)
        self.name = "ModuleRandTube"
        self.availableChars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVW-"

    def notify_command(self, message_id, from_attr, date, chat, commandName, commandStr):
        if commandName == "randtube":
            response = urllib.request.urlopen(self.URL + self.BASE_SEARCH + self.random_code())

            str_response = response.read().decode('utf-8')
            objJSON = json.loads(str_response)

            if len(objJSON['responseData']['results']) > 0:
                youtubeUrl = objJSON['responseData']['results'][0]['unescapedUrl']
                title = objJSON['responseData']['results'][0]['titleNoFormatting']
                self.bot.sendMessage("%s: %s"%(title[:len(title)-9] ,youtubeUrl), chat['id'])

    def random_code(self):
        code = ""
        for i in range(0, 4):
            code += self.availableChars[random.randint(0, len(self.availableChars) - 1)]
        return code


    def get_commands(self):
        return [
            ("randtube", "Random youtube video"),
        ]
