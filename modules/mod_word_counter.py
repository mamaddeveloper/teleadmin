from modules.module_base import ModuleBase
import json
import os.path
import codecs

#Module for counting words or expression said by teacher or other speaker
class ModuleWordCounter(ModuleBase):
    FILE = os.path.join(os.path.dirname(__file__), "../botTest/WordCounter.txt")
    def __init__(self, bot):
        ModuleBase.__init__(self, bot)
        self.name = "ModuleWordCounter"
        self.speakers = []
        self.load()

    #Usage : /wc or /WordCounter action speakerName expression
    #Action can be : get, set, add, sub, list
    #Example : /wc Bilat get gratuit
    #  --->    bilat said 99 times : gratuit
    def notify_command(self, message_id, from_attr, date, chat, commandName, commandStr):
        if commandName == "wordcounter" or commandName == "wc" :

            args = commandStr.split()

            text = ""
            if len(args) >= 2 :

                speakerName = args[0].lower() # the one who said the expression to count
                action = args[1].lower() # get, set, add, sub or list

                #Gets the first speaker with the given name or, if this speaker doesn't exist yet, return None
                speaker = next((s for s in self.speakers if s.name == speakerName),None)


                #If the speaker doesn't exist yet...
                if speaker is None :
                    #....Create it
                    speaker = Speaker(speakerName)
                    self.speakers.append(speaker)

                if action == "list":

                    text = speaker.name + " said : \n"
                    if len(speaker.expressionCounter) > 0:
                        for expres, count in speaker.expressionCounter.items():
                            text += "   " + expres + " -> " + str(count) + "\n"
                    else:
                        text = "No expression saved for this speaker"

                else :
                    expressionLength = len(commandStr) - len(args[0]) - len(args[1]) - 2
                    expression = commandStr[-expressionLength:].lower() # The expression to count

                    if action == "get" :
                        n = speaker.getExpressionCount(expression)
                        text = speaker.name + " said " + str(n) + " times : " + expression
                    elif action == "set" :
                        #TODO
                        text = "Not implemented yet, sorry :-)"
                    elif action == "add" :
                        n = speaker.getExpressionCount(expression)
                        speaker.setExpressionCount(expression, n+1)
                        text = speaker.name + "; " + expression + " : " + str(n) + " -> " + str(n+1)
                        self.save()
                    elif action == "sub" :
                        n = speaker.getExpressionCount(expression)
                        speaker.setExpressionCount(expression, n-1)
                        text = speaker.name + "; " + expression + " : " + str(n) + " -> " + str(n-1)
                        self.save()
                    else:
                        text = "Action parameter must be get,set,add, sub or list"

            elif commandStr.lower() == "clear" and self.bot.admin.is_admin(from_attr):
                self.speakers = []
                self.save()
                text = "Cleared !"
                pass
            else:
                text = "Not enough argument, usage : /wc action speakerName [expression]"

            self.bot.sendMessage(text, chat["id"])

    def get_commands(self):
        return [
            ("wc", "Get or modify the number of times a word has been said by a speaker"),
            ("wordcounter", "Get or modify the number of times a word has been said by a speaker"),
        ]

    def save(self):
        with codecs.open(self.FILE, "w") as f:
            f.write(json.dumps([{"name": s.name, "expressionCounter" : s.expressionCounter} for s in self.speakers]))

    def load(self):
        if not os.path.exists(self.FILE):
            return
        with codecs.open(self.FILE, "r") as f:
            js = json.loads("".join(f.readlines()))
        for s in js:
            speaker = Speaker(s["name"])
            speaker.expressionCounter = s["expressionCounter"]
            self.speakers.append(speaker)

class Speaker:
    def __init__(self, _name):
        self.name = _name
        self.expressionCounter = {}

    def getExpressionCount(self,expression):
        #Gets the value corresponding to the key in the dictionary or return the default value if the key doesn't exist
        return self.expressionCounter.setdefault(expression, 0)

    def setExpressionCount(self, expression, n):
        self.expressionCounter[expression] = n
