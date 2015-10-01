from modules.module_base import ModuleBase
from tools.vote import *

class ModuleVote(ModuleBase):
    def __init__(self, bot):
        ModuleBase.__init__(self, bot)
        self.name = "ModuleVote"
        self.manager = VoteManager()

    def notify_command(self, message_id, from_attr, date, chat, commandName, commandStr):
        if commandName == "vote":
            try:
                commandStr = str(commandStr)
                if commandStr == "close":
                    vote = self.manager.close(from_attr)
                    text = self.vote_tostring(vote)
                    self.bot.sendMessage(text, chat["id"])
                elif commandStr == "state":
                    vote = self.manager.state()
                    text = self.vote_tostring(vote)
                    self.bot.sendMessage(text, chat["id"])
                elif commandStr == "yes" or commandStr == "oui":
                    self.manager.vote(from_attr, True)
                    self.bot.sendMessage("Vote enregistré", chat["id"])
                elif commandStr == "no" or commandStr == "non":
                    self.manager.vote(from_attr, False)
                    self.bot.sendMessage("Vote enregistré", chat["id"])
                elif commandStr == "":
                    self.bot.sendMessage("Veuillez spécifier un argument", chat["id"])
                else:
                    self.manager.start(from_attr, commandStr)
                    self.bot.sendMessage("Vote crée, vous pouvez commencer de voter !", chat["id"])

            except NoVoteException:
                self.bot.sendMessage("Impossible de voter, pas de vote en cours", chat["id"])
            except OngoingVoteException:
                self.bot.sendMessage("Impossible de créer un nouveau vote, il y a un vote en cours", chat["id"])
            except AlreadyVoteException:
                self.bot.sendMessage("Tu pensais pouvoir voter plusieurs fois, petit malin...", chat["id"])
            except Exception as e:
                self.bot.sendMessage("Unknown vote exception : %s" % e, chat["id"])
    def vote_tostring(self, vote):
        if vote.votesFor == vote.votesAgainst:
            resultat = "égalité"
        elif vote.votesFor >= vote.votesAgainst:
            resultat = "accepté"
        else:
            resultat = "refusé"
        return "Résultat du vote '%s' : \nVotes pour : %d\nVotes contre : %d\nNombre votant : %d\nRésultat (%s) : %s (%.2f%%)" \
               % (vote.name, vote.votesFor, vote.votesAgainst, vote.voteCount, "définitif" if vote.end else "provisoir",  resultat, vote.rate * 100)

    def get_commands(self):
        return [
            ("vote", "vote"),
        ]
