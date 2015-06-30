import re
import collections

from bot import Bot
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
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [a + b[1:] for a, b in splits if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b) > 1]
    replaces = [a + c + b[1:] for a, b in splits for c in ModuleSpelling.alphabet if b]
    inserts = [a + c + b for a, b in splits for c in ModuleSpelling.alphabet]
    return set(deletes + transposes + replaces + inserts)


def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in ModuleSpelling.NWORDS)


def known(words): return set(w for w in words if w in ModuleSpelling.NWORDS)


# SpellChecker method, return best correction and a list of suggestions words
def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    return max(candidates, key=ModuleSpelling.NWORDS.get), candidates


class ModuleSpelling(ModuleBase):
    NWORDS = train(words('modules/resources/FrenchDictionnary.txt'))
    alphabet = 'abcdefghijklmnopqrstuvwxyzàâæçéèêîïëôœùûüÿ'
    people = {'Deruaz','Pierre', 'Jules', 'Eddy'}

    def __init__(self, bot):
        ModuleBase.__init__(self, bot)
        self.name = "Spelling"

    # Spelling correction
    def notify_text(self, message_id, from_attr, date, chat, text):

        # Only words bigger than 4 letters
        words = re.findall("\w{4,}", text.lower(), re.UNICODE)

        if from_attr['first_name'] in ModuleSpelling.people:
            wordList = {}
            for word in words:

                # Call spelling checker
                bestSolution, candidates = correct(word)
                if bestSolution != word:
                    wordList[word] = candidates


            if len(wordList.keys()) > 0:
                message = "Nombre de mots mal orthographiés : " + str(len(wordList)) + "\nVoici leurs corrections:\n\n"

                for word in wordList.keys():
                    message += word + " --> " + " ou ".join(list(wordList[word])[:3]) + "\n"

                # Congratulaiton message
                if ((len(wordList.keys()) / len(words))  >= 0.6) and (len(wordList.keys()) > 3):
                    Congrats = "\n\n Beau score! Tu as fais " + str(len(wordList.keys())) + " fautes sur " + str(len(words)) + " mots! Es-tu dyslexique?"
                    message += Congrats

                self.bot.sendMessage(message, chat["id"], reply_to_message_id = message_id)