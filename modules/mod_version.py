from modules.module_base import ModuleBase
import os.path
import subprocess

class ModuleVersion(ModuleBase):
    PATH = os.path.dirname(os.path.dirname(__file__))

    def __init__(self, bot):
        ModuleBase.__init__(self, bot)
        self.name = "ModuleVersion"

    def notify_command(self, message_id, from_attr, date, chat, commandName, commandStr):
        if commandName == "version":
            try:
                text = "https://github.com/nichuguen/TelegramBot/\n"
                text += subprocess.check_output(["git","log", "-1"], cwd=self.PATH).decode("utf-8")
                print(type(text))
                self.bot.sendMessage(text, chat["id"])
            except:
                self.bot.sendMessage("Error getting version", chat["id"])
