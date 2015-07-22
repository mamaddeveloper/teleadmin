import gspread
import json
import os.path
import oauth2client.client
import random

class BestSentences:
    FILE = os.path.join(os.path.dirname(__file__), "../botTest/drive.json")

    def __init__(self):
        self.sentences = ()

    def load(self):
        settings = json.load(open(self.FILE))
        json_key = settings["key"]
        scope = ['https://spreadsheets.google.com/feeds']

        credentials = oauth2client.client.SignedJwtAssertionCredentials(json_key['client_email'],bytes(json_key['private_key'], 'UTF-8'), scope)

        gc = gspread.authorize(credentials)
        wks = gc.open_by_key(settings["sheet"]).sheet1

        i = 2
        self.sentences = []
        while True:
            who = wks.cell(i, 1).value
            text = wks.cell(i, 2).value
            date = wks.cell(i, 3).value
            if not who or not text:
                break
            self.sentences.append(
                {
                    "who": who,
                    "text": text,
                    "date": date,
                }
            )
            i += 1

    def get(self, key=None):
        if len(self.sentences) == 0:
            raise BestSentencesNotLoadedException()
        if key:
            key = key.lower()
            source = list([s for s in self.sentences if s["who"].lower() == key])
            if len(source) == 0:
                raise BestSentencesNotFoundException()
        else:
            source = self.sentences
        return random.choice(source)

class BestSentencesException(Exception): pass
class BestSentencesNotLoadedException(Exception): pass
class BestSentencesNotFoundException(Exception): pass


if __name__ == '__main__':
    b = BestSentences()
    b.load()
    b.get()
    b.get("piconche")
    b.get("piconche")
    b.get("pocket")
    b.get("pocket")
    b.get("pocket")
    b.get("pocket")
    print("ok")
