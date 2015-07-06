from modules.module_base import ModuleBase
from tools.vote import *

class ModuleVote(ModuleBase):
    def __init__(self, bot):
        ModuleBase.__init__(self, bot)
        self.manager = VoteManager()

    def notify_command(self, message_id, from_attr, date, chat, commandName, commandStr):
        if commandName == "vote":
            try:
                commandStr = str(commandStr)
                if commandStr == "close":
                    vote = self.manager.close(from_attr)
                    nbVotes = len(vote.votes)
                    rate = 0
                    if nbVotes > 0:
                        rate = vote.votesFor / nbVotes
                    if vote.votesFor == vote.votesAgainst:
                        resultat = "égalité"
                    elif vote.votesFor >= vote.votesAgainst:
                        resultat = "accepté"
                    else:
                        resultat = "refusé"
                    text = "Résultat du vote '%s' : \nVotes pour : %d\nVotes contre : %d\nNombre votant : %d\nRésultat : %s (%.2f%%)" \
                           % (vote.name, vote.votesFor, vote.votesAgainst, nbVotes, resultat, rate * 100)
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
