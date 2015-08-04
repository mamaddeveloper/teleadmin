from modules.module_base import ModuleBase
from tools.admin import Admin, NotAdminException
import logging

class ModuleAdmin(ModuleBase):
    LOGS = (
        "errors",
        "info",
    )
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
                self.logger.warning("%s added by %s", commandStr, from_attr)
                self.bot.sendMessage("Admin added", chat["id"])
            elif commandName == "noop":
                self.admin.remove(from_attr, commandStr)
                self.logger.warning("%s removed by %s", commandStr, from_attr)
                self.bot.sendMessage("Admin removed", chat["id"])
            elif commandName == "level":
                level = "admin" if self.admin.is_admin(from_attr) else "user"
                self.bot.sendMessage("You are '%s'" % level, chat["id"])
            elif commandName == "log":
                if not self.admin.is_admin(from_attr):
                    raise NotAdminException
                if commandStr in self.LOGS:
                    try:
                        [h().flush() for h in logging._handlerList]
                    except:
                        self.logger.exception("Fail to flush handlers", exc_info=True)
                    self.bot.sendDocument(chat["id"], "logs/%s.log" % commandStr)
                else:
                    self.bot.sendMessage("Log %s unknown" % commandStr, chat["id"])

        except NotAdminException:
            self.logger.warning("%s Not admin /%s %s", from_attr, commandName, commandStr)
            self.bot.sendMessage("Your are not admin !", chat["id"])
