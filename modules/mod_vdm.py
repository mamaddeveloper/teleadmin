from modules.module_base import ModuleBase
from tools.vdm import Vdm
import threading

class ModuleVdm(ModuleBase):

    def __init__(self, bot):
        ModuleBase.__init__(self, bot)
        self.name = "ModuleTroll"
        self.vdm = Vdm()

    def notify_command(self, message_id, from_attr, date, chat, commandName, commandStr):
        if commandName == "vdm":
            threading.Thread(target=self.work, args=(commandStr, chat)).start()

    def work(self, commandStr, chat):
        if commandStr == "last":
            self.bot.sendMessage(self.vdm.last(), chat["id"])
        elif commandStr == "random" or commandStr == "":
            self.bot.sendMessage(self.vdm.random(), chat["id"])