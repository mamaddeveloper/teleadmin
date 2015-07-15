from modules.module_base import ModuleBase
from tools.admin import Admin, NotAdminException

class ModuleAdmin(ModuleBase):
    def __init__(self, bot):
        ModuleBase.__init__(self, bot)
        self.name = "ModuleAdmin"
        self.admin = Admin()
        self.bot.admin = self.admin


    def notify_command(self, message_id, from_attr, date, chat, commandName, commandStr):
        try:
            if commandName == "id":
                self.bot.sendMessage("Your id is %s" % from_attr["id"], chat["id"])
            elif commandName == "op":
                self.admin.add(from_attr, commandStr)
                self.bot.sendMessage("Admin added", chat["id"])
            elif commandName == "noop":
                self.admin.remove(from_attr, commandStr)
                self.bot.sendMessage("Admin removed", chat["id"])
            elif commandName == "level":
                level = "admin" if self.admin.is_admin(from_attr) else "user"
                self.bot.sendMessage("You are '%s'" % level, chat["id"])
        except NotAdminException:
            self.bot.sendMessage("Your are not admin !", chat["id"])
