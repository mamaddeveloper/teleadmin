from modules.module_base import ModuleBase
from tools.bestSentences import *
import threading

class ModuleDtc(ModuleBase):

    def __init__(self, bot):
        ModuleBase.__init__(self, bot)
        self.name = "BestSentences"
        self.best_sentences = BestSentences()
        threading.Thread(target=self.best_sentences.load).start()

    def notify_command(self, message_id, from_attr, date, chat, commandName, commandStr):
        if commandName == "bs":
            if commandStr == "load":
                if self.bot.admin.is_admin(from_attr):
                    try:
                        self.best_sentences.load()
                        self.bot.sendMessage("Reloaded !", chat["id"])
                    except BestSentencesLoadException:
                        self.bot.sendMessage("Fail to load sentences.", chat["id"])
                else:
                    self.bot.sendMessage("Access denied !", chat["id"])
            else:
                try:
                    s = self.best_sentences.get(commandStr)
                    text = "%s\n\n%s, %s" % (s["text"], s["who"], s["date"])
                    self.bot.sendMessage(text, chat["id"])
                except BestSentencesNotFoundException:
                    self.bot.sendMessage("User %s not found !" % commandStr, chat["id"])

                except BestSentencesNotLoadedException:
                    self.bot.sendMessage("Module not loaded !", chat["id"])
    def get_commands(self):
        return [
            ("bs", "Best sentences."),
        ]

