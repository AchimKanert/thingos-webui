import tornado.web

import subprocess
import re

filename="/data/etc/crontabs/root"

class DisplayHandler(tornado.web.RequestHandler):
    def get(self):
        fromhour=""
        fromminute=""
        tohour=""
        tominute=""
        cronjobs=readData()
        
        for cronjob in cronjobs:
          if (cronjob["state"]=="on"):
            fromhour=cronjob["hour"]
            fromminute=cronjob["minute"]
          elif (cronjob["state"]=="off"):
            tohour=cronjob["hour"]
            tominute=cronjob["minute"]
        
        
        
        self.render("display.html", title="Display", isOn=isOn(), fromhour=fromhour, fromminute=fromminute, tohour=tohour, tominute=tominute)

    def post(self):
        self.set_header("Content-Type", "text/plain")
        if (self.get_body_argument("action")=="off"):
          setOn(False)
        elif (self.get_body_argument("action")=="on"):
          setOn(True)
        elif (self.get_body_argument("action")=="set"):
          cronjobon={}
          cronjobon["minute"]   =self.get_body_argument("fromminute")
          cronjobon["hour"]     =self.get_body_argument("fromhour")
          cronjobon["day"]      ="*"
          cronjobon["month"]    ="*"
          cronjobon["dayofweek"]="*"
          cronjobon["state"]    ="on"

          cronjoboff={}
          cronjoboff["minute"]   =self.get_body_argument("tominute")
          cronjoboff["hour"]     =self.get_body_argument("tohour")
          cronjoboff["day"]      ="*"
          cronjoboff["month"]    ="*"
          cronjoboff["dayofweek"]="*"
          cronjoboff["state"]    ="off"

          if (cronjobon["minute"]!="" and cronjobon["hour"]!="" and cronjoboff["minute"]!="" and cronjoboff["hour"]!=""):
            writeData([cronjobon, cronjoboff])

        self.redirect("/display")


def isOn():
    result=subprocess.check_output(["vcgencmd", "display_power"], encoding="utf-8")
    match=re.search('display_power=(.)', result)
    return (match.group(1)== "1")

def setOn(state):
    if (state):
      subprocess.check_output(["vcgencmd", "display_power", "1"])
    else: 
      subprocess.check_output(["vcgencmd", "display_power", "0"])


re_searchstring=' *([^ ]+) +([^ ]+) +([^ ]+) +([^ ]+) +([^ ]+) +/usr/bin/photoframe\.sh display (on|off)'


def readData():
  data=[]

  try:
    f = open(filename, "r")
  except:
    pass
  else:
    for line in f:
      match=re.search(re_searchstring, line)
      if match:
        cronjob={}
        cronjob["minute"]   =match.group(1)
        cronjob["hour"]     =match.group(2)
        cronjob["day"]      =match.group(3)
        cronjob["month"]    =match.group(4)
        cronjob["dayofweek"]=match.group(5)
        cronjob["state"]    =match.group(6)
        
        data.append(cronjob)

    f.close()
      
  return data



def filterRules(lines):
  newlines=[]
  for line in lines:
    if not (re.search(re_searchstring, line)):
      newlines.append(line)

  return newlines

def writeData(rules):
  content=[]
  
  try:
    f = open(filename, "r")
  except:
    pass
  else:
    content = f.readlines()
    content = filterRules(content) 
    f.close()
 
  for rule in rules:
    stringrule="{minute} {hour} {day} {month} {dayofweek} /usr/bin/photoframe.sh display {state}".format(minute=rule["minute"], hour=rule["hour"], day=rule["day"], month=rule["month"], dayofweek=rule["dayofweek"], state=rule["state"])
    content.append(stringrule)
 
 
  f = open(filename, "w")
  f.writelines(content)
  f.close()
  
  print(content[1])
  #subprocess.Popen(["photoframe.sh","sync"])

