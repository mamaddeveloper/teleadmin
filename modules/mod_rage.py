from modules.module_base import ModuleBase
import random
from tools.fileList import FileList

class ModuleRage(ModuleBase):

    def __init__(self, bot):
        ModuleBase.__init__(self, bot)
        self.name = "ModuleRage"
        self.ragelist = FileList("botTest/ragelist")

    def notify_command(self, message_id, from_attr, date, chat, commandName, commandStr):
        if commandName == "rage":

            args = commandStr.split(" ");

            if args[0] != '':
                if len(args) > 1:
                    if args[0] == "add":
                        template = " ".join(args[1:])
                        if "$" in template:
                            template = template[:1].upper() + template[1:]
                            self.ragelist.add(template)
                            self.bot.sendMessage("/rage : template \"%s\" added."%template, chat['id'])
                        else:
                            self.bot.sendMessage("/rage : Your rage phrase template must contains at least one '$' ", chat['id'])
                        return 

                if len(self.ragelist) > 0:
                    try:
                        self.bot.sendMessage(random.choice(self.ragelist.list).replace("$", " ".join(args)), chat['id'])
                    except:
                        self.bot.sendMessage("/rage : YOU TRIED TO RAGE BUT THIS IS THE MOTHERFUCKING MODULE THAT RAGE BECAUSE IT'S FUCKED UP", chat['id'])
                else:
                    self.bot.sendMessage("/rage : First add a rage template please.", chat['id'])
            else:
                self.bot.sendMessage("/rage : Arguments missing", chat['id'])


    def get_commands(self):
        return [
            ("rage", "Eh bah, ça rage du cul ? Keyword: add <rage template with '$' placeholder> | <thing against you rage>"),
        ]