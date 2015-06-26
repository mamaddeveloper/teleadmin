
class ModuleBase:
    def __init__(self):
        self.name = "Base Module"
    
    def setBot(self, bot):
        self.bot = bot
        
    def notify(self, update):
        try:
            if "Vincent"== update.message.fromi["first_name"] or "Vincent" == update.message.fromi["last_name"]:
                self.bot.answerToMessage("Merci pour ta franche participation, ma ptite baguette", update.message)
        except:
            pass
            
    def getName(self):
        return self.name