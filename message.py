
class Message:
    def __init__(self, json):
        #print json
        #print "\n\n"
    #    for key in json:
      #      print( "%s, %s" %(key, json[key]))
        for key in json:
            keyToSet=key
            if key == "from":
                keyToSet="fromi"
            setattr(self, keyToSet, json[key])
    
    def getChat(self):
        return self.chat
