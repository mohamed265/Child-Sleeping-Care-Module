import RPi.GPIO as GPIO
from Room import Room
from SoundSession import SoundSession
from RabbitMQMqttClient import RabbitMQMqttClient
import time
import json

childRoom = Room("Child Room", 18)
parentRoom = Room("Parent Room", 15)
soundSession = SoundSession()

def on_message(client, userdata, message):
    '''
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
    '''
    global soundSession
    #print (message.topic is 'arduino/sensors/A4', message.topic == 'arduino/sensors/A4')
    #print(message.topic.equals( 'arduino/sensors/A4'))
    if message.topic == 'arduino/sensors/A4':
        #print ("kdhjkehk")
        mess = message.payload.decode()
        #print("message")
        #print("mess rtpe", type (mess))
        
        #print("proximity value: ", mess.proximity)
        msg = json.loads(mess)
        
        #print("msg rtpe", type (msg))
        print("proximity value: ", msg["proximity"])
        soundSession.updateProximity(msg["proximity"])
        #print("after")
        '''
        if msg.proximity > 100:
            if soundSession.thereIsSoundSession:
                soundSession.closeSession()
        '''    


def on_connect(client, a, b, c):
    global rabbitMQMqttClient
    rabbitMQMqttClient.subscribe("arduino/sensors/A4")
    print("on_connect method called")
    

rabbitMQMqttClient = RabbitMQMqttClient("cs616", "cs616", "192.168.0.103", 1883, on_message, on_connect)   

def soundSensorDtect(channel):
    global soundSession
    global rabbitMQMqttClient
        
    if GPIO.input(channel):
        print("sound detected")
        if soundSession.isProximityCloseValue():
            parentRoom.turnOffLight()
            print("sound due to a movement")
        else:
            if not(soundSession.thereIsSoundSession) or soundSession.isOutdatedSession():
                    print("will start a new sound session")
                    soundSession.startNewSession()
            else:
                print("there is an active sound session")
                soundSession.updateSoundDetectionTime()
                if soundSession.isTurningParentRoomLightOn():
                    parentRoom.turnOnLight() #ForPeriodNonBlocking(5)
                elif soundSession.isTurningChildRoomLightOn():
                    childRoom.turnOnLight() #ForPeriodNonBlocking(3)
            msg = {
                "counter": 0,
                "micros": 0,
                #"sessionId": soundSession.sessionId,
                "acoustic": round(soundSession.getSessionDuration(), 2),
                #"startTime": soundSession.startTime
            }
            rabbitMQMqttClient.publish("arduino/sensors/A5", json.dumps(msg))
    else:
        if soundSession.thereIsSoundSession and soundSession.isOutdatedSession():
            print("sound session outdated, close light")
            soundSession.closeSession()
            parentRoom.turnOffLight()
            childRoom.turnOffLight()
        print("no detection")
        
channel = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)
GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)
GPIO.add_event_callback(channel, soundSensorDtect)

while True:
    time.sleep(1)
    if soundSession.thereIsSoundSession and soundSession.isOutdatedSession():
            print("sound session outdated, close light")
            parentRoom.turnOffLight()
            childRoom.turnOffLight()
            soundSession.closeSession()
    if not(rabbitMQMqttClient.isConnected):
        rabbitMQMqttClient.connect()
