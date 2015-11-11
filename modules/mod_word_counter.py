from modules.module_base import ModuleBase

#Module for counting words or expression said by teacher or other speaker
class ModuleWordCounter(ModuleBase):

    def __init__(self, bot):
        ModuleBase.__init__(self, bot)
        self.name = "ModuleWordCounter"
        self.speakers = []
        self.dict = {}

    #Usage : \wc or \WordCounter action speakerName expression
    #Action can be : get, set, add, sub
    #Example : \wc Bilat get gratuit
    #  --->    Bilat said 99 times : gratuit
    def notify_command(self, message_id, from_attr, date, chat, commandName, commandStr):
        if commandName == "wordcounter" or commandName == "wc" :

            args = commandStr.split()

            speakerName = args[0].lower() # the one who said the expression to count
            action = args[1].lower() # get, set, add or sub

            expressionLength = len(commandStr) - len(args[0]) - len(args[1]) - 2
            expression = commandStr[-expressionLength:].lower() # The expression to count

            #Gets the first speaker with the given name or, if this speaker doesn't exist yet, return None
            speaker = next((s for s in self.speakers if s.name == speakerName),None)

            text = ""
            #If the speaker doesn't exist yet...
            if speaker is None :
                #....Create it
                speaker = Speaker(speakerName)
                self.speakers.append(speaker)

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
            elif action == "sub" :
                n = speaker.getExpressionCount(expression)
                speaker.setExpressionCount(expression, n-1)
                text = speaker.name + "; " + expression + " : " + str(n) + " -> " + str(n-1)
            else:
                text = "Action parameter must be get,set,add or sub"

            self.bot.sendMessage(text, chat["id"])

    def get_commands(self):
        return [
            ("wc", "Get or modify the number of times a word has been said by a speaker"),
            ("wordcounter", "Get or modify the number of times a word has been said by a speaker"),
        ]

class Speaker:
    def __init__(self, _name):
        self.name = _name
        self.expressionCounter = {}

    def getExpressionCount(self,expression):
        #Gets the value corresponding to the key in the dictionary or return the default value if the key doesn't exist
        return self.expressionCounter.setdefault(expression, 0)

    def setExpressionCount(self, expression, n):
        self.expressionCounter[expression] = n
