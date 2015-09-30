from modules.module_base import ModuleBase

class ModuleHelp(ModuleBase):
    def __init__(self, bot):
        ModuleBase.__init__(self, bot)
        self.name = "ModuleHelp"


    def notify_command(self, message_id, from_attr, date, chat, commandName, commandStr):
        if commandName == "help":
            self.bot.sendMessage("\r\n".join(["/%s - %s" % (t[0], t[1]) for t in self.bot.listCommandsWithDesc]), chat["id"])

    def get_commands(self):
        return [
            ("help", "Show help"),
        ]
