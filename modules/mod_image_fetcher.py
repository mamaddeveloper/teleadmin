from modules.module_base import ModuleBase
import urllib.request
import json
import random
from tools.limitator import Limitator, LimitatorLimitted, LimitatorMultiple

#Module for fecthing an image on Google Image
class ModuleImageFetcher(ModuleBase):

    def __init__(self, bot):
        ModuleBase.__init__(self, bot)
        self.name = "ModuleImageFetcher"
        self.limitator = LimitatorMultiple(
            Limitator(10, 900, True),
            Limitator(120, 60*60, False),
        )

    #Usage : /img query [--index | --random]
    #Example : /img cara -2
    def notify_command(self, message_id, from_attr, date, chat, commandName, commandStr):
        if commandName == "img":

            args = commandStr.split()

            if len(args) > 0:
                try:
                    self.limitator.next(from_attr)
                except LimitatorLimitted:
                    self.bot.sendMessage("Tu as abusé, réssaye plus tard !", chat["id"])
                    return
                searchTerm = ""
                startIndex = 0

                #If the last argument start with "-", it means that it's an index parameter
                if args[-1][0] == "-":

                    #So the search query is composed by every argument but the last one
                    searchTerm = "%20".join(args[:-1]) # %20 -> espace

                    #Check if it's a random or a value
                    if args[-1] == "-random" or args[-1] == "-r":
                        startIndex = random.randint(0,50); #TODO put this values in a variable
                    else:
                        try:
                            startIndex = int(args[-1][1:])
                        except ValueError:
                            pass
                #Otherwise, the start index is still 0 and all the arguments are part of the search query
                else:
                    searchTerm = "%20".join(args) # %20 -> espace

                searchUrl = "https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=" + searchTerm + "&start=" + str(startIndex)
                print("searchUrl : " + searchUrl)

                response = urllib.request.urlopen(searchUrl)

                str_response = response.read().decode('utf-8')
                objJSON = json.loads(str_response)

                if len(objJSON['responseData']['results']) > 0:
                    imageUrl = objJSON['responseData']['results'][0]['unescapedUrl']
                    print("Image URL : " + imageUrl)

                    urllib.request.urlretrieve(imageUrl, "out.jpg")
                    self.bot.sendPhoto(chat["id"], "out.jpg", " ".join(searchTerm.split("%20")))
                else:
                    self.bot.sendMessage("Désolé mon petit %s, aucune image trouvé pour %s" % (from_attr['first_name'], searchTerm), chat["id"])
            else:
                self.bot.sendMessage("Not enough argument, usage : /img query [-index | -random]", chat["id"])

    def get_commands(self):
        return [
            ("img", "Fetch an image on Google Image"),
        ]

