from modules.module_base import ModuleBase

class ModuleWordCounter(ModuleBase):

    def __init__(self, bot):
        ModuleBase__init__(self, bot)
        self.name = "ModuleWordCounter"
        self.speakers = []
        self.dict = {}

    #Usage : \wc or \WordCounter action speakerName expression
    #Action can be : get, set, add, sub
    #Example : \wc get Bilat gratuit
    #  --->    Bilat said 99 times : gratuit
    def notify_command(self, message_id, from_attr, date, chat, commandName, commandStr):
        if commandName == "WordCounter" or commandName == "wc" :

            args = commandStr.split()

            speakerName = args[0] # the one who said the expression to count
            action = args[1] # get, set, add or sub

            expressionLength = len(commandStr) - len(args[0]) - len(args[1]) - 2
            expression = commandStr[-expressionLength:] # The expression to count

            speaker = next((s for s in self.speakers if s.name == speakerName),None)

            text = ""
            if speaker is None :

                speaker = Speaker(speakerName)
                self.speakers.append(speaker)

            if action == "get" :
                n = speaker.getExpressionCount(expression)
                text = speaker.name + " said " + n + " times : " + expression
            elif action == "set" :
                #TODO
                text = "Not implemented yet, sorry :-)"
            elif action == "add" :
                n = speaker.getExpressionCount(expression)
                speaker.setExpressionCount(expression, n+1)
                text = speaker.name + "; " + expression + " : " + n + " -> " + n+1
            elif action == "sub" :
                n = speaker.getExpressionCount(expression)
                speaker.setExpressionCount(expression, n-1)
                text = speaker.name + "; " + expression + " : " + n + " -> " + n-1
            else:
                text = "Action parameter must be get,set,add or sub"

            self.bot.sendMessage(text, chat["id"])

    def get_commands(self):
        return [
        ("wc", "Count words"),
        ("WordCounter", "Count words"),
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