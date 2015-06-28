from bot import Bot
from modules.module_base import ModuleBase

class ModuleMysql(ModuleBase):

    def __init__(self, bot):
        ModuleBase.__init__(self, bot)
        self.name = "Mysql"
        
 # def notify(self, update):
 #     try:
 #         if "test" in update.message.text:
 #             self.bot.sendMessage("Message de test", update.message.chat["id"])
 #             keyboard = array3=[["test1", "test2"],["test3", "test4"]]
 #             self.bot.setReplyKeyboardMarkup(keyboard)
 #     except:
 #         pass
 #         
 # def notifyCommand(self, command, commandArgText):
 #     pass