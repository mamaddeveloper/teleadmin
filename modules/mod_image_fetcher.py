from modules.module_base import ModuleBase
import urllib.request
import json

#Module for fecthing an image on Google Image
class ModuleImageFetcher(ModuleBase):

    def __init__(self, bot):
        ModuleBase.__init__(self, bot)
        self.name = "ModuleImageFetcher"

    #Usage : /img query [index]
    #Example : /img cara 2
    def notify_command(self, message_id, from_attr, date, chat, commandName, commandStr):
        if commandName == "img":

            args = commandStr.split()

            text = ""
            if len(args) > 0:

                fetcher = urllib.request.build_opener()
                #TODO multiple words search term
                searchTerm = args[0]
                startIndex = 0
                if len(args) > 1:
                    startIndex = args[1]

                searchUrl = "http://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=" + searchTerm + "&start=" + str(startIndex)

                response = urllib.request.urlopen(searchUrl)

                str_response = response.read().decode('utf-8')
                objJSON = json.loads(str_response)

                imageUrl = objJSON['responseData']['results'][0]['unescapedUrl']
                text = imageUrl

                urllib.request.urlretrieve(imageUrl, "out.jpg")
                self.bot.sendPhoto(chat["id"], "out.jpg", args[0])

            else:
                self.bot.sendMessage("Not enough argument, usage : /img query [index]", chat["id"])

    def get_commands(self):
        return [
            ("img", "Fetch an image on Google Image"),
        ]

