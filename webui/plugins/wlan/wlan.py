import tornado.web
import subprocess


filename="/data/etc/wpa_supplicant.conf"

class WlanHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("wlan.html", title="WLAN", wlan=readData())

    def post(self):
        data={}
        data["ssid"]=self.get_body_argument("ssid")
        data["password"]=self.get_body_argument("password")
        
        writeData(data)
        
        self.render("wlan_response.html", title="WLAN")
        


def readData():
  print("Test")
  data={}
  data["ssid"]=""
  data["password"]=""

  try:
    f = open(filename, "r")
  except:
    pass
  else:
    lines = f.readlines()
    for line in lines:
       parts=line.split("=")
       if (len(parts)==2):
         print(parts)
         if parts[0].strip() == "ssid":
            data["ssid"]=parts[1][1:-2]
         # Password is ignored as not needed

    f.close()
      
  return data


def writeData(data):
  try:
    f = open(filename, "r")
  except:
    pass
  else:
    lines = f.readlines()
    f.close()
    f = open(filename, "w")
    for line in lines:
       parts=line.split("=")
       if (len(parts)==2):
         print(parts)
         if parts[0].strip() == "ssid":
            f.write("ssid=\"{ssid}\"\n".format(ssid=data["ssid"]))
         elif parts[0].strip() == "psk":
            f.write("psk=\"{psk}\"\n".format(psk=data["password"]))
         else:
            f.write(line)
       else:
            f.write(line) 
    f.close()

  subprocess.Popen(["reboot"])

