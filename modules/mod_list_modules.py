from modules.module_base import ModuleBase
import inspect
import os

class ModuleListModule(ModuleBase):
    def __init__(self, bot):
        ModuleBase.__init__(self, bot)
        self.name = "ModuleListModule"


    def notify_command(self, message_id, from_attr, date, chat, commandName, commandStr):
        if commandName == "modules":
            if (self.bot.admin.is_admin(from_attr)):
                print("\r\n".join(["%s : %s" % (m.name, type(m)) for m in self.bot.listModules]))
                self.bot.sendMessage("\r\n".join(["%s in %s" % (m.name, os.path.basename(inspect.getfile(m.__class__))) for m in self.bot.listModules]), chat["id"])
            else:
                self.bot.sendMessage("Admins only", chat["id"])

    def get_commands(self):
        return [
            ("modules", "List loaded modules (admin only)"),
        ]
