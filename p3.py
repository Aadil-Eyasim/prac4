import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import threading
import datetime
import RPi.GPIO as GPIO

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)
# create the mcp object
mcp = MCP.MCP3008(spi, cs)
# create an analog input channel on pin 1 for temp reading and pin 2 for
light reading
chan = AnalogIn(mcp, MCP.P1)
chan1= AnalogIn(mcp, MCP.P2)
GPIO.setmode(GPIO.BCM)
oldTime=datetime.datetime.now()
pButton=23 #gpio 17 is used for push button
global sampTime #10s is the default sample time
sampTime=10

def setup() :
#button setup and interrupt
    GPIO.setup(pButton,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(pButton,GPIO.RISING,callback=pushTime,bouncetime=200)
    
def getTemp():
    thread=threading.Timer(sampTime,getTemp)
    thread.daemon=True
    thread.start()
    diffTime=datetime.datetime.now() - oldTime
    temp=round((chan.voltage-0.5)/0.01)
    print("{0:.0f}".format(RT.total_seconds())+"s",'\t',chan.value,'\t ',Temp,'C','\t ', chan1.value)
    
def pushTime(chanNum):
    #this function changes the value of the sample time whenever the button interrupt is triggered
    global sampTime
    if GPIO.event_detected(chanNum):
        if sampTime>5:
            sampTime=5
        elif sampTime==5:
            sampTime=1
        else:
            sampTime=10
    return sampTime



if __name__=="__main__":
print("Runtime",'\t',"Temp Reading",'\t',"Temp",'\t',"Light
reading")
setup()
getTemp()
while True:
pass
