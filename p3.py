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
chan = AnalogIn(mcp, MCP.P1)
chan1 = AnalogIn(mcp, MCP.P2)

#print(’Raw ADC Value: ’, chan.value)
#print(’ADC Voltage: ’ + str(chan.voltage) + ’V’)

toggle_btn = 23   
def setup():
    #setup button
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(toggle_btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(toggle_btn, GPIO.FALLING, callback=toggle_btn_pressed, bouncetime=300) 
    pass
    

t = 1
print('{:<12s} {:<15s} {:<15s} {:<15s}'.format('Runtime','Temp Reading', 'Temp', 'Light Reading'))

 
start = time.time()
def print_runtime_temp_thread():

    thread = threading.Timer(t, print_runtime_temp_thread)
    thread.daemon = True  # Daemon threads exit when the program does
    thread.start()

    
    end = time.time() #get the end time 
    runtime = math.trunc(end-start) 
 
    temp = (chan1.voltage - 0.5)/0.01  
    
    print('{:<12s} {:<15d} {:<4.1f} C {:<15d}'.format(str(runtime)+'s', chan1.value, temp, chan.value))
    pass 

# sampling period button

def toggle_btn_pressed(toggle_btn):
#this function increases the sampling period if the button is pressed
    global t
    global presses
    
    presses+=1

    if (presses==1):
        sampling_time = 1
    elif (presses==2):
        sampling_time = 5
    elif (presses==3):
        sampling_time = 10
        presses=0 #loop back to 0 presses once the button has been pressed 3 times
    
    return t
    return presses

pass

if __name__ == "__main__":
    setup() #call setup
    print_runtime_temp_thread() # call it once to start the thread
    
    # Tell our program to run indefinitely
    while True:
        pass
