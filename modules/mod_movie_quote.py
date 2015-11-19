from modules.module_base import ModuleBase
import urllib.request
import json
import random
from tools.limitator import Limitator, LimitatorLimitted, LimitatorMultiple

#Module for fecthing a movie quote on www.quodb.com
class ModuleMovieQuote(ModuleBase):

    def __init__(self, bot):
        ModuleBase.__init__(self, bot)
        self.name = "ModuleMovieQuote"

    #Usage : /quote query
    #Example : /quote blue pill
    def notify_command(self, message_id, from_attr, date, chat, commandName, commandStr):
        if commandName == "quote":

            args = commandStr.split()

            if len(args) > 0:

                searchTerm = "%20".join(args) # %20 -> espace

                searchUrl = "http://api.quodb.com/search/" + searchTerm + "?titles_per_page=1&phrases_per_title=1&page=1"
                print("searchUrl : " + searchUrl)

                response = urllib.request.urlopen(searchUrl)

                str_response = response.read().decode('utf-8')
                objJSON = json.loads(str_response)

                print(str_response)

                if objJSON["numFound"] > 0:
                    movieTitle = objJSON["docs"][0]["title"]
                    movieQuote = objJSON["docs"][0]["phrase"]
                    quoteTime = objJSON["docs"][0]["time"]

                    strTime = self.getStrTime(quoteTime)

                    self.bot.sendMessage("\"%s\" - %s [%s]" % (movieQuote, movieTitle,strTime), chat["id"])

                else:
                    self.bot.sendMessage("Ne pleure pas %s, je n'ai trouvé aucun film avec %s dedans..." % (from_attr['first_name'], searchTerm), chat["id"])

            else:
                self.bot.sendMessage("Not enough argument, usage : /quote query", chat["id"])

    def getStrTime(self, quoteTime):
        quoteTimeSeconds = quoteTime // 1000 % 60
        quoteTimeMinutes = quoteTime // (1000 * 60) % 60
        quoteTimeHours = (quoteTime // (1000 * 60 * 60)) % 24

        strTime = ""
        if quoteTimeHours < 10:
            strTime += "0"
        strTime += "%s:" % quoteTimeHours
        if quoteTimeMinutes < 10:
            strTime += "0"
        strTime += "%s:" % quoteTimeMinutes
        if quoteTimeSeconds < 10:
            strTime += "0"
        strTime += "%s" % quoteTimeSeconds

        return strTime

    def get_commands(self):
        return [
            ("quote", "Fetch a movie quote on www.quodb.com"),
        ]

