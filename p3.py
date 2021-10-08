import busio
import digitalio
import board 
import threading
import time 
import RPi.GPIO as GPIO
import adafruit_mcp3xxx.mcp3008 as MCP 
from adafruit_mcp3xxx.analog_in import AnalogIn 
import math


# some global variables that need to change as we run the program
sampling_time = 1
presses = 0

#define pins
sampling_btn = 23
  
#setup 
def setup():
    #setup button
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(sampling_btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(sampling_btn, GPIO.FALLING, callback=sampling_btn_pressed, bouncetime=400) #add rising edge detection on a channel
    
    pass
    
#create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)
# create the mcp object
mcp = MCP.MCP3008(spi, cs)
# create an analog input channel on pin 1
chan = AnalogIn(mcp, MCP.P1)

#print heading
print('{:<12s} {:<15s} {:<15s}'.format('Runtime','Temp Reading', 'Temp'))

start = time.time() #get the starting time of the thread
def print_temp_thread():
    #This function prints the temp to the screen every 10 seconds
    thread = threading.Timer(sampling_time, print_temp_thread)
    thread.daemon = True  # Daemon threads exit when the program does
    thread.start()

    end = time.time() #get the end time 
    runtime = math.trunc(end-start) #calculate the runtime 
    
    adc_value = chan.value #adc opcode
    temp_voltage = chan.voltage #voltage from the adc
    temp = (temp_voltage - 0.5)/0.01 #convert voltage into temp using equation from MCP9700 datasheet 
    
    print('{:<12s} {:<15d} {:<4.1f} C'.format(str(runtime)+'s', adc_value, temp))
    pass 

# sampling period button
def sampling_btn_pressed(sampling_btn):
#this function increases the sampling period if the button is pressed
    global sampling_time
    global presses
    
    presses+=1

    if (presses==1):
        sampling_time = 1
    elif (presses==2):
        sampling_time = 5
    elif (presses==3):
        sampling_time = 10
        presses=0 #loop back to 0 presses once the button has been pressed 3 times
    
    return sampling_time
    return presses

pass

if __name__ == "__main__":
    setup() #call setup
    print_temp_thread() # call it once to start the thread
    
    # Tell our program to run indefinitely
    while True:
        pass
