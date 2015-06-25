
class Message:
    def __init__(self, json):
        #print json
        #print "\n\n"
    #    for key in json:
      #      print( "%s, %s" %(key, json[key]))
        for key in json:
            setattr(self, key, json[key])
    
    def getChat(self):
        return self.chat