import scrollphathd as sphd
import time
import datetime
import glob
from scrollphathd.fonts import font3x5
import numpy as np

brightSet=0.5
precise=1

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    f = open(device_file, 'r') # Opens the temperature device file
    lines = f.readlines() # Returns the text
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw() # Read the temperature 'device file'

    # While the first line does not contain 'YES', wait for 0.2s
    # and then read the device file again.
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()

    # Look for the position of the '=' in the second line of the
    # device file.
    equals_pos = lines[1].find('t=')

    # If the '=' is found, convert the rest of the line after the
    # '=' into degrees Celsius, then degrees Fahrenheit
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return round(temp_c,1)

#sphd.write_string(str(read_temp()))
def printDegree(x,y):
    sphd.set_pixel(x,y,brightSet)
    sphd.set_pixel(x,y+1,brightSet)
    sphd.set_pixel(x+1,y,brightSet)
    sphd.set_pixel(x+1,y+1,brightSet)

def tinyC(x,y):
    sphd.set_pixel(x,y,brightSet)
    sphd.set_pixel(x+1,y,brightSet)
    sphd.set_pixel(x,y+1,brightSet)
    sphd.set_pixel(x,y+1,brightSet)
    sphd.set_pixel(x,y+2,brightSet)
    sphd.set_pixel(x+1,y+2,brightSet)

def pacmanOpen(xpos,ypos,reverse):
    pixels=np.asarray([[0,0,1,1,1,1,0],[0,1,1,0,1,1,1],[1,1,1,1,1,1,0],[1,1,1,1,1,0,0],[1,1,1,1,1,1,0],[0,1,1,1,1,1,1],[0,0,1,1,1,1,0]])
    for y in range(7):
        for x in range(7):
            if reverse:
                if pixels[y][x]==1:
                    sphd.set_pixel(xpos+(7-x),ypos+y,brightSet)
            else:
                if pixels[y][x]==1:
                    sphd.set_pixel(xpos+x,ypos+y,brightSet)

def pacmanClose(xpos,ypos,reverse):
    pixels=np.asarray([[0,0,1,1,1,0,0],[0,1,1,1,1,1,0],[1,1,1,1,0,1,1],[1,1,1,1,1,1,1],[1,1,1,1,1,1,1],[0,1,1,1,1,1,0],[0,0,1,1,1,0,0]])
    for y in range(7):
        for x in range(7):
            if reverse:
                if pixels[y][x]==1:
                    sphd.set_pixel(xpos+(7-x),ypos+y,brightSet)
            else:
                if pixels[y][x]==1:
                    sphd.set_pixel(xpos+x,ypos+y,brightSet)

def displayPacman(timeout):
    startTime=int(time.time())
    while startTime+timeout > time.time():
            sphd.flip(x=True,y=True)
            for x in range(0,17):
                sphd.clear()
    
                # Draw the dots
                for i in range(3,17,3):
                    if (x < i):
                        sphd.set_pixel(i,3,brightSet)
    
                # Alternate mouth open/close
                if x % 2 == 0:
                    pacmanOpen(x,0,0)
                else:
                    pacmanClose(x,0,0)
    
                sphd.show()
                time.sleep(0.3)

def displayTemp(timeout):
    startTime=int(time.time())
    while startTime+timeout > time.time():
    	sphd.flip(x=True,y=True)
        sphd.clear()
    	if precise==0:
            offset=1
            len=sphd.write_string(str(int(read_temp())),x=offset,y=1,font=font3x5,brightness=brightSet)
            printDegree(len+offset,1)
            sphd.write_string("C",x=len+offset+3,y=1,font=font3x5,brightness=brightSet)
        else:
            value=str(read_temp())
            num=value.split('.')[0]
            point=value.split('.')[1]
            len=sphd.write_string(num,x=0,y=1,font=font3x5,brightness=brightSet)
            sphd.set_pixel(len,5,brightSet)
            sphd.write_string(point,x=len+2,y=1,font=font3x5,brightness=brightSet)

            tinyC(len+7,3)
            sphd.set_pixel(len+6,1,brightSet)
    #print (str(read_temp()))
        sphd.show()
        time.sleep(1)

def displayTime(timeout):
    startTime=int(time.time())
    while startTime+timeout > time.time():
        sphd.flip(x=True,y=True)
        sphd.clear()
        currentTime=datetime.datetime.now()
    
        # Flash the colon every other second
        secs=int(currentTime.strftime("%S"))
        if (secs % 2 == 0):
            sphd.write_string(":",x=8,y=0,font=font3x5,brightness=brightSet)
    
        stringHour=currentTime.strftime("%H")
        stringMins=currentTime.strftime("%M")
    
        sphd.write_string(stringHour,x=0,y=0,font=font3x5,brightness=brightSet)
        sphd.write_string(stringMins,x=10,y=0,font=font3x5,brightness=brightSet)
    
        secPixels=int(round((float(secs)/60)*17,0))
        for s in range(secPixels):
            sphd.set_pixel(s,6,brightSet)
    
        sphd.show()
        #sphd.scroll(1)
        time.sleep(0.05)
        sphd.clear()

while True:
    displayPacman(5)
    displayTime(15)
    displayTemp(5)

