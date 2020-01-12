#-----------------------------------------------------------------------------------------------
#
#
#
#-----------------------------------------------------------------------------------------------
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO! This is probably because you need superuser privileges. You can achieve this by using 'sudo' to run your script")
#
# Global variables

#-----------------------------------------------------------------------------------------------
class relayGPIO:
    nbRelays = 8
    maxRelays = 8
    #----------1--2--3--4--5--6--7--8--
    relayLabels = ["Relay-1","Relay-2","Relay-3","Relay-4","Relay-5","Relay-6","Relay-7","Relay-8"]
    relayState = [0,0,0,0,0,0,0,0]
    relayPins = [29,31,33,35,37,32,38,40]
    boardrev = 3
    gpiover = 1
    previousMode = "None"

    #
    # 
    #
    def initGpio(self):
        # Set GPIO mode to Pin's number, channel list
        self.boardrev=GPIO.RPI_INFO['P1_REVISION']
        self.gpiover=GPIO.VERSION
        self.previousMode = GPIO.getmode()
        GPIO.setwarnings(False)
        self.nbRelays = 6

    #
    #
    # Configure GPIO pins to output
    #
    def configPins(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.relayPins, GPIO.OUT)
        #
        # Set all pins to LOW
        #
        GPIO.output(self.relayPins, GPIO.LOW)
        #pinfunc = GPIO.gpio_function(pin)

    #
    # Load settings                     
    #
    def loadSettings(self):
        pass

    #
    # Save settings                     
    #
    def saveSettings(self):
        pass

    #
    # Clean exit                    
    #
    def cleanExit(self):
        pass
        #try:
            #GPIO.cleanup()
        #finally:
            #pass

    #
    # Set pin id for a relay 
    #
    def setRelayPin(self,relayId,pinId):
        self.relayPins[relayId - 1] = pinId
        print("New Pin ID=" + str(pinId))

    #
    # Get pin id for a relay 
    #
    def getRelayPin(self,relayId):
        pinId = self.relayPins[relayId - 1]
        print("Get Pin ID=" + str(pinId))

    #
    # Get relay status 
    #
    def getRelayStatus(self,relayId):
        print("Relay " + relayId + " = " + str(self.relayState[relayId - 1]))


    #
    # Relay On
    #
    def relayOn(self, relayId):
        pinId = self.relayPins[relayId - 1]
        print("ON Pin ID=" + str(pinId))
        GPIO.output(pinId, GPIO.HIGH)
        self.relayState[relayId - 1] = 1

    #
    # Relay Off
    #
    def relayOff(self, relayId):
        pinId = self.relayPins[relayId - 1]
        print("OFF Pin ID=" + str(pinId))
        GPIO.output(pinId, GPIO.LOW)
        self.relayState[relayId - 1] = 0

    #
    # Show settings
    #
    def showSettings(self):
        print("Nb relays :" + str(self.nbRelays))


