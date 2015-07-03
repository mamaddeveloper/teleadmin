from modules.module_base import ModuleBase

class ModuleHelp(ModuleBase):
    def __init__(self, bot):
        ModuleBase.__init__(self, bot)
        self.name = "ModuleHelp"
        with open("commandlist", 'r') as f:
            self.text = "Bot help : \n" + "".join(f.readlines())

    def notify_command(self, message_id, from_attr, date, chat, commandName, commandStr):
        if commandName == "help":
            self.bot.sendMessage(self.text, chat["id"])
