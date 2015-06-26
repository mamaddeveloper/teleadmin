
import requests
import time
from update import Update
from message import Message


class Bot:
    REQUEST_BASE="https://api.telegram.org/bot"
    def __init__(self, token):
        self.token = token
        self.last_update_id = 0
    
    def start(self):
        lines = []
        with open("updates_log", 'r') as f:
            lines.extend(f.readlines())
        for line in lines:
            if self.token in line:
                self.last_update_id = int(line.split(":")[-1])
                break
        while True:
            self.getUpdates()
            time.sleep(1)
            #break
            
    def stop(self):
        lines = []
        with open("updates_log", 'r') as f:
            lines.extend(f.readlines())
            
        lines = [line for line in lines if self.token not in line]
        lines.append(self.token + ":" +str(self.last_update_id))
        
        with open("updates_log", 'w') as f:
            for line in lines:
                f.write(line)
                f.write("\n")
                
            
    def getUpdates(self):
        r = self.getJson("getUpdates", offset=self.last_update_id)
        listUpdates = []
        for update in r["result"]:
            listUpdates.append(Update(update))
            print update
        sorted(listUpdates, key= lambda x: x.update_id)
        if len(listUpdates) > 0:
            self.last_update_id = listUpdates[-1].update_id+1
        for update in listUpdates:
            self.answerToMessage("Ta gueule, " + update.message.fromi["first_name"], update.message)
            #pass
        
    def answerToMessage(self, text, message):
        r = self.getJson("sendMessage", chat_id=message.chat["id"], text=text, disable_web_page_preview="true")
        
    def getJson(self, requestName, **parameters):
        requestString = Bot.REQUEST_BASE+self.token+"/"+requestName+"?"
        for key in parameters:
            requestString = requestString+key+"="+str(parameters[key])+"&"
        if requestString.endswith("&") or requestString.endswith("?"):
            requestString = requestString[:-1]
        print requestString
        r = requests.get(requestString)
        return r.json()
        
        
    
