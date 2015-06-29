from bot import Bot
import re, collections

from modules.module_base import ModuleBase

def words(filename):
    with open(filename) as file:
        return re.findall("\w+", file.read(), re.UNICODE)

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

def edits1(word):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in ModuleSpelling.alphabet if b]
   inserts    = [a + c + b     for a, b in splits for c in ModuleSpelling.alphabet]
   return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in ModuleSpelling.NWORDS)

def known(words): return set(w for w in words if w in ModuleSpelling.NWORDS)

def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    print(candidates)
    return max(candidates, key=ModuleSpelling.NWORDS.get)

class ModuleSpelling(ModuleBase):

    NWORDS = train(words('modules/ressources/FrenchDictionnary.txt'))
    alphabet = 'abcdefghijklmnopqrstuvwxyzàâæçéèêîïëôœùûüÿ'

    def __init__(self, bot):
        ModuleBase.__init__(self, bot)
        self.name = "Spelling"

    # Spelling correction
    def notify_text(self, message_id, from_attr, date, chat, text):
        words = re.findall("\w+", text, re.UNICODE)

        if from_attr['first_name'] == "Michael":
            for word in words:
                if correct(word) != word.lower():
                    message = "Le mot " + word + " n'est pas orthographié correctment. Vouliez-vous dire : " + correct(word) + " ?"
                    print(message)
                    self.bot.sendMessage(message, chat["id"])

