import busio
import digitalio
import board 
import adafruit_mcp3xxx.mcp3008 as MCP 
from adafruit_mcp3xxx.analog_in import AnalogIn 
import RPi.GPIO as GPIO
import threading
import time 
import math

#create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)
# create the mcp object
mcp = MCP.MCP3008(spi, cs)
# create an analog input channel on pin 1
chan1 = AnalogIn(mcp, MCP.P1) #for Temp sensor
chan2 = AnalogIn(mcp, MCP.P2) #for LDR

#print(’Raw ADC Value: ’, chan.value)
#print(’ADC Voltage: ’ + str(chan.voltage) + ’V’)

toggle_btn = 23   
def setup():

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(toggle_btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(toggle_btn, GPIO.FALLING, callback=toggle_btn_pressed, bouncetime=300) 
    pass
    

t = 10 
start = time.time()
def print_runtime_temp_thread():

    thread = threading.Timer(t, print_runtime_temp_thread)
    thread.daemon = True  
    thread.start()
 
    end = time.time() #get the end time 
    runtime = math.trunc(end-start) 
 
    temp = round(((chan1.voltage - 0.5)*100), 2)
    
    print('{:<12s} {:<15d} {:<5.2f} {:<6s} {:<13d}'.format(str(runtime)+'s', chan1.value, temp, 'C', chan2.value))
    pass 


def toggle_btn_pressed(toggle_btn):

    global t
    if GPIO.event_detected(toggle_btn):
        if t==1:
            t=5
        elif t==1:
            t=5
        elif t==10:
            t=1
        else:
            t=10
        return t
pass

if __name__ == "__main__":
    setup() 
    print('{:<12s} {:<15s} {:<12s} {:<15s}'.format('Runtime','Temp Reading', 'Temp', 'Light Reading'))
    print_runtime_temp_thread() 
    
    # Tell our program to run indefinitely
    while True:
        pass
