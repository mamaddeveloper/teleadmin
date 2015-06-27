from bot import Bot


class ModuleChangeGroupName():
    def __init__(self):
        self.bot = None
        self.name = "ChangeGroupName"

    def getName(self):
        return self.name

    def setBot(self, bot):
        self.bot = bot
        print("Bot set" + str(self.bot))

    def notify(self, update):
        try:
            if update.message.new_chat_title:
                self.bot.sendMessage("Quel nom de merde.", update.message.chat["id"])
        except:
            pass
