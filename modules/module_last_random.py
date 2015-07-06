from modules.module_base import ModuleBase
import threading

class ModuleBaseLastRandom(ModuleBase):
    def __init__(self, bot, name, cmd, provider):
        ModuleBase.__init__(self, bot)
        self.name = name
        self.cmd = cmd
        self.provider = provider

    def notify_command(self, message_id, from_attr, date, chat, commandName, commandStr):
        if commandName == self.cmd:
            threading.Thread(target=self.work, args=(commandStr, chat)).start()

    def work(self, commandStr, chat):
        if commandStr == "last":
            self.bot.sendMessage(self.provider.last(), chat["id"])
        elif commandStr == "random" or commandStr == "":
            self.bot.sendMessage(self.provider.random(), chat["id"])
        else:
            self.bot.sendMessage("command combination '/%s %s' unknown" % (self.cmd, commandStr), chat["id"])