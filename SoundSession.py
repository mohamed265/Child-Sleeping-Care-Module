import time
import timeit
import datetime

class SoundSession:

    sessionId = 0
    startTime = None
    t_startTime = None
    t_lastSoundDetectionTime = None
    thereIsSoundSession = False
    proximity = 0
        
    def __init__(self):
        self.startTime = datetime.datetime.now()
        self.t_startTime = self.t_lastSoundDetectionTime = timeit.default_timer()
    
    def startNewSession(self):
        self.thereIsSoundSession = True
        self.sessionId = self.sessionId + 1
        self.startTime = datetime.datetime.now()
        self.t_startTime = self.t_lastSoundDetectionTime = timeit.default_timer()
        self.proximity = 0
        
    def closeSession(self):
        self.thereIsSoundSession = False

    def isOutdatedSession(self):
        if self.isTimeExceeds(self.t_lastSoundDetectionTime, 5): # greaterthan 5 seconds
            return True
        return False
    
    def getSessionDuration(self):
        return timeit.default_timer() - self.t_startTime

    def isTimeExceeds(self, t_time, msAmount):
        #print(t_time, msAmount,timeit.default_timer() , timeit.default_timer() - t_time > msAmount)
        return timeit.default_timer() - t_time > msAmount
    
    def updateProximity(self, proximity):
        self.proximity = proximity
        
    def isProximityCloseValue(self):
        return self.proximity > 0 and self.proximity < 40
        
    def updateSoundDetectionTime(self):
        self.t_lastSoundDetectionTime = timeit.default_timer()
    
    def isTurningChildRoomLightOn(self):
        return self.isTimeExceeds(self.t_startTime, 5)

    def isTurningParentRoomLightOn(self):
        return self.isTimeExceeds(self.t_startTime, 10)
