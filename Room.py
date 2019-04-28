from gpiozero import LED
import time
import thread

class Room:
    name = ""
    gpiPin = 0
    led = None
    isTurnedOn = False
        
    def __init__(self, name, gpiPin):
        self.name = name
        self.gpiPin = gpiPin
        self.led = LED(gpiPin)

    def turnOnLightForPeriodNonBlocking(self, timeout):
        self.turnOnLight()
        thread.start_new_thread( self.awaitTimeThenClose, (timeout,) )
        
    def turnOnLightForPeriodBlocking(self, timeout):
        self.turnOnLight()
        self.awaitTimeThenClose(timeout) 
        
    def awaitTimeThenClose(self, timeout):
        time.sleep(timeout)
        self.turnOffLight()

    def turnOnLight(self):
        if not(self.isTurnedOn):
            self.led.on()
            self.isTurnedOn = True
            print(self.name + " light turned on")

    def turnOffLight(self):
        if self.isTurnedOn:
            self.led.off()
            self.isTurnedOn = False
            print(self.name + " light turned off")


