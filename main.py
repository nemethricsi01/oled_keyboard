
import time
import board
import digitalio
import board, busio, displayio, os, terminalio
import adafruit_displayio_ssd1306
import adafruit_displayio_sh1106
from adafruit_display_text import label
import keypad
import supervisor
import rotaryio
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.rect import Rect
import neopixel
from rainbowio import colorwheel
import gc
pixel_pin = board.GP14
num_pixels = 24



pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=1, auto_write=False)
# pixels[5] = (255,0,0)
# pixels.show()
# Create the I2C interface.
displayio.release_displays()
sda, scl = board.GP0, board.GP1
i2c = busio.I2C(scl, sda, frequency = 400_000)
enc = rotaryio.IncrementalEncoder(board.GP16,board.GP17)
#display_bus = displayio.I2CDisplay(i2c, device_address=0x3d,reset=board.GP28)
display_bus = displayio.I2CDisplay(i2c, device_address=0x3d)
display = adafruit_displayio_sh1106.SH1106(display_bus, width=132, height=64)
#display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)
group0 = displayio.Group()
group1 = displayio.Group()
group2 = displayio.Group()
group3 = displayio.Group()

# Draw a label
#text = "Hello World!"
#text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=28, y=28)
#splash.append(text_area)
circle = Circle(128-16, 16, 6, fill=0x000000, outline=0xFFFFFF)#0
group0.append(circle)
circle = Circle(128-32, 16, 6, fill=0x000000, outline=0xFFFFFF)#1
group0.append(circle)
circle = Circle(128-48, 16, 6, fill=0x000000, outline=0xFFFFFF)#2
group0.append(circle)
circle = Circle(128-64, 16, 6, fill=0x000000, outline=0xFFFFFF)#3
group0.append(circle)
circle = Circle(128-16, 32, 6, fill=0x000000, outline=0xFFFFFF)#4
group0.append(circle)
circle = Circle(128-32, 32, 6, fill=0x000000, outline=0xFFFFFF)#5
group0.append(circle)
circle = Circle(128-48, 32, 6, fill=0x000000, outline=0xFFFFFF)#6
group0.append(circle)
circle = Circle(128-64, 32, 6, fill=0x000000, outline=0xFFFFFF)#7
group0.append(circle)
circle = Circle(12, 10, 8, fill=0x000000, outline=0xFFFFFF)#8
group0.append(circle)
circle = Circle(28, 23, 8, fill=0x000000, outline=0xFFFFFF)#9
group0.append(circle)
circle = Circle(42, 39, 8, fill=0x000000, outline=0xFFFFFF)#10
group0.append(circle)
circle = Circle(55, 55, 8, fill=0x000000, outline=0xFFFFFF)#11
group0.append(circle)




group1.append(Rect(0, 0, 128, 20, fill=0x0))
group1.append(Rect(0, 20, 128, 44, fill=0x0))
group2.append(Rect(0, 0, 128, 20, fill=0x0))
group2.append(Rect(0, 20, 128, 44, fill=0x0))
group2.append(Rect(0, 0, 128, 20, fill=0x0))
group2.append(Rect(0, 20, 128, 44, fill=0x0))

group3.append(Rect(0, 0, 128, 0, fill=0x0))
group3.append(Rect(0, 0, 128, 16, fill=0x0))
group3.append(Rect(0, 0, 128, 32, fill=0x0))
group3.append(Rect(0, 0, 128, 48, fill=0x0))
group3.append(Rect(0, 0, 128, 0, fill=0x0))
group3.append(Rect(0, 0, 128, 16, fill=0x0))
group3.append(Rect(0, 0, 128, 32, fill=0x0))
group3.append(Rect(0, 0, 128, 48, fill=0x0))
text2 = ""


last_position = None
lastevent = 0
actevent = 0
lasttime = 0
acttime = 0
presscount = 0
lastenc = 0
actenc = 0
animatetime = 0

submenu = 0
idle = 0
menu = 0
exitmenu = 0
presscount = 0
animation = 0
animselect = 0
buttontimer = [0]*12
buttoncolor = [0]*12
fade = 0




# define buttons. these can be any physical switches/buttons, but the values
KEY_PINS = (
    board.GP13,
    board.GP12,
    board.GP11,
    board.GP10,
    board.GP9,
    board.GP8,
    board.GP7,
    board.GP6,
    board.GP5,
    board.GP4,
    board.GP3,
    board.GP2,
)


keys = keypad.Keys(KEY_PINS, value_when_pressed=False, pull=True,interval=0.010,max_events=48)
encoderbutton = keypad.Keys((board.GP15,), value_when_pressed=False, pull=True)
# display.show()
# display.text("hello",0,0,1)
# display.show()
acttime = supervisor.ticks_ms()
lasttime = acttime
animatetime = supervisor.ticks_ms()
while True:
    pixels.show()
    gc.collect()
    if(supervisor.ticks_ms() > animatetime +10):
        if(menu == 0):
            if animselect == 2:
                for i in range (0,12):
                    if(buttontimer[i] > 0):
                        buttontimer[i] = buttontimer[i]-1
                        pixels[i] = colorwheel(buttoncolor[i] & 255)
                        buttoncolor[i] = buttoncolor[i] + 1
                    if(buttontimer[i] == 0):
                        buttoncolor[i] = 0
                        pixels[i] = (0,0,0)
            if animselect == 3:
                fade = fade + 0.4
                if(fade > 255):
                    fade = 0
                for i in range(0,12):
                    pixels[i] = colorwheel(int(fade) & 255)
        else:
            pixels[0] = (0,0,0)
        animatetime = supervisor.ticks_ms()
    actenc = enc.position
    encbuttstate = encoderbutton.events.get()
    if(encbuttstate):
        if(encbuttstate.pressed == True):
            if menu == 1:
                if submenu == 0:
                    menu = 2
                    exitmenu = 1
                if submenu == 1:
                    submenu = 0
                    menu = 0
                    exitmenu = 1
                    
            if (menu == 0)and (exitmenu == 0):
                menu = 1
            
            
            if (menu == 2)and(exitmenu == 0):
                animselect = 2
            if menu == 3:
                animselect = 3
            if menu == 4:
                animselect = 4
            if menu == 5:
                menu = 0
            if(exitmenu == 1):
                exitmenu = 0
            print("buttmenu:",menu)
            print("buttsubmenu:",submenu)
            print("buttanimselect:",animselect)
    if(lastenc != actenc):
        if(lastenc < actenc):
            if menu == 0:
                idle = idle+1
                if(idle > 1):
                    idle = 0
            if menu == 1:
                submenu = submenu+1
                if(submenu > 1):
                    submenu = 0
            if menu > 1:
                menu = menu+1
                if menu > 5:
                    menu = 2
        else:
            if menu == 0:
                idle = idle-1
                if(idle <0):
                    idle = 1
            if menu == 1:
                submenu = submenu-1
                if(submenu <0):
                    submenu = 1
            if menu > 1:
                menu = menu-1
                if menu < 2:
                    menu = 5
        print("encmenu:",menu)
        print("encsubmenu:",submenu)
        print("encanimselect:",animselect)
        lastenc = actenc
    if(menu == 0):
        if(idle == 0):
            display.show(group0)
            event = keys.events.get()
            if event:
                key_number = event.key_number
                key_state = event.pressed
                
                if(key_number == 0)and(key_state == True):
                    circle = Circle(128-16, 16, 6, fill=0xFFFFFF, outline=0xFFFFFF)
                    group0[0] = circle
                    if animselect == 2:
                        buttontimer[0] = 800
                if(key_number == 0)and(key_state == False):
                    circle = Circle(128-16, 16, 6, fill=0x000000, outline=0xFFFFFF)
                    group0[0] = circle
##########################################################################################
                if(key_number == 1)and(key_state == True):
                    circle = Circle(128-32, 16, 6, fill=0xFFFFFF, outline=0xFFFFFF)
                    group0[1] = circle
                    if animselect == 2:
                        buttontimer[1] = 800
                if(key_number == 1)and(key_state == False):
                    circle = Circle(128-32, 16, 6, fill=0x000000, outline=0xFFFFFF)
                    group0[1] = circle
##########################################################################################                    
                if(key_number == 2)and(key_state == True):
                    circle = Circle(128-48, 16, 6, fill=0xFFFFFF, outline=0xFFFFFF)
                    group0[2] = circle
                    if animselect == 2:
                        buttontimer[2] = 800
                if(key_number == 2)and(key_state == False):
                    circle = Circle(128-48, 16, 6, fill=0x000000, outline=0xFFFFFF)
                    group0[2] = circle
##########################################################################################                    
                if(key_number == 3)and(key_state == True):
                    circle = Circle(128-64, 16, 6, fill=0xFFFFFF, outline=0xFFFFFF)
                    group0[3] = circle
                    if animselect == 2:
                        buttontimer[3] = 800
                if(key_number == 3)and(key_state == False):
                    circle = Circle(128-64, 16, 6, fill=0x000000, outline=0xFFFFFF)
                    group0[3] = circle
##########################################################################################                   
                if(key_number == 4)and(key_state == True):
                    circle = Circle(128-16, 32, 6, fill=0xFFFFFF, outline=0xFFFFFF)
                    group0[4] = circle
                    if animselect == 2:
                        buttontimer[4] = 800
                if(key_number == 4)and(key_state == False):
                    circle = Circle(128-16, 32, 6, fill=0x000000, outline=0xFFFFFF)
                    group0[4] = circle    
##########################################################################################                    
                if(key_number == 5)and(key_state == True):
                    circle = Circle(128-32, 32, 6, fill=0xFFFFFF, outline=0xFFFFFF)
                    group0[5] = circle
                    if animselect == 2:
                        buttontimer[5] = 800
                if(key_number == 5)and(key_state == False):
                    circle = Circle(128-32, 32, 6, fill=0x000000, outline=0xFFFFFF)
                    group0[5] = circle    
##########################################################################################                
                if(key_number == 6)and(key_state == True):
                    circle = Circle(128-48, 32, 6, fill=0xFFFFFF, outline=0xFFFFFF)
                    group0[6] = circle
                    if animselect == 2:
                        buttontimer[6] = 800
                if(key_number == 6)and(key_state == False):
                    circle = Circle(128-48, 32, 6, fill=0x000000, outline=0xFFFFFF)
                    group0[6] = circle
##########################################################################################     
                if(key_number == 7)and(key_state == True):
                    circle = Circle(128-64, 32, 6, fill=0xFFFFFF, outline=0xFFFFFF)
                    group0[7] = circle
                    if animselect == 2:
                        buttontimer[7] = 800
                if(key_number == 7)and(key_state == False):
                    circle = Circle(128-64, 32, 6, fill=0x000000, outline=0xFFFFFF)
                    group0[7] = circle
##########################################################################################                                       
                if(key_number == 8)and(key_state == True):
                    circle = Circle(12, 10, 8, fill=0xFFFFFF, outline=0xFFFFFF)
                    group0[8] = circle
                    if animselect == 2:
                        buttontimer[8] = 800
                if(key_number == 8)and(key_state == False):
                    circle = Circle(12, 10, 8, fill=0x000000, outline=0xFFFFFF)
                    group0[8] = circle
##########################################################################################                    
                if(key_number == 9)and(key_state == True):
                    circle = Circle(28, 23, 8, fill=0xFFFFFF, outline=0xFFFFFF)
                    group0[9] = circle
                    if animselect == 2:
                        buttontimer[9] = 800
                if(key_number == 9)and(key_state == False):
                    circle = Circle(28, 23, 8, fill=0x000000, outline=0xFFFFFF)
                    group0[9] = circle
##########################################################################################                                        
                if(key_number == 10)and(key_state == True):
                    circle = Circle(42, 39, 8, fill=0xFFFFFF, outline=0xFFFFFF)
                    group0[10] = circle
                    if animselect == 2:
                        buttontimer[10] = 800
                if(key_number == 10)and(key_state == False):
                    circle = Circle(42, 39, 8, fill=0x000000, outline=0xFFFFFF)
                    group0[10] = circle
##########################################################################################                
                if(key_number == 11)and(key_state == True):
                    circle = Circle(55, 55, 8, fill=0xFFFFFF, outline=0xFFFFFF)
                    group0[11] = circle
                    if animselect == 2:
                        buttontimer[11] = 800
                if(key_number == 11)and(key_state == False):
                    circle = Circle(55, 55, 8, fill=0x000000, outline=0xFFFFFF)
                    group0[11] = circle
            
                    
            
        if(idle == 1):
            acttime = supervisor.ticks_ms()
            event = keys.events.get()
            if(acttime < lasttime+5000):
                if(event):
                    key_number = event.key_number
                    key_state = event.pressed
                    for i in range (0,12):
                        if(key_number == i)and(key_state == True):
                            presscount = presscount + 1
            else:
                lasttime = acttime
                text2 = ""+str(presscount*12)
                presscount = 0    
    #         keys.events.clear()
    #         keys.reset()
            text = "apm:"
            text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=4, y=8)
            text_area.scale = 2
            group1[0] = text_area
            
            text_area = label.Label(terminalio.FONT, text=text2, color=0xFFFFFF, x=35, y=40)
            text_area.scale = 4
            group1[1] = text_area
            display.show(group1)
    if(menu == 1):
        if(submenu == 0):
            group2[0]=Rect(0, 0, 128, 20, fill=0xFFFFFF)
            text = "RGB"
            text_area = label.Label(terminalio.FONT, text=text, color=0x0, x=4, y=10)
            text_area.scale = 2
            group2[1] = text_area
            
            group2[2]=Rect(0, 20, 128, 20, fill=0x0)
            text_area = label.Label(terminalio.FONT, text="IDLE", color=0xFFFFFF, x=4, y=30)
            text_area.scale = 2
            group2[3] = text_area
            
            display.show(group2)
        if(submenu == 1):
            group2[0]=Rect(0, 0, 128, 20, fill=0x0)
            text = "RGB"
            text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=4, y=10)
            text_area.scale = 2
            group2[1] = text_area
            group2[2]=Rect(0, 20, 128, 20, fill=0xFFFFFF)
            text_area = label.Label(terminalio.FONT, text="IDLE", color=0x0, x=4, y=30)
            text_area.scale = 2
            group2[3] = text_area
            display.show(group2)
        
    if(menu == 2):
        text = "animation1"
        if(animselect == 2):
            group3[0]=Rect(0, 0, 128, 16, fill=0xFFFFFF)
            text_area = label.Label(terminalio.FONT, text=text, color=0x0, x=4, y=8)
        else:
            group3[0]=Rect(2, 0, 126, 16, fill=0x0,outline = 0xFFFFFF)
            text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=4, y=8)
        
        text_area.scale = 1
        group3[1] = text_area
        
        group3[2]=Rect(0, 16, 128, 16, fill=0x0)
        text = "animation2"
        text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=4, y=24)
        text_area.scale = 1
        group3[3] = text_area
        
        group3[4]=Rect(0, 32, 128, 16, fill=0x0)
        text = "animation3"
        text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=4, y=40)
        text_area.scale = 1
        group3[5] = text_area
        
        group3[6]=Rect(0, 48, 128, 16, fill=0x0)
        text = "EXIT"
        text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=4, y=56)
        text_area.scale = 1
        group3[7] = text_area
        
        display.show(group3)
    if(menu == 3):
        group3[0]=Rect(0, 0, 128, 16, fill=0x0)
        text = "animation1"
        text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=4, y=8)
        text_area.scale = 1
        group3[1] = text_area
        
        text = "animation2"
        if(animselect == 3):
            group3[2]=Rect(0, 16, 128, 16, fill=0xFFFFFF)
            text_area = label.Label(terminalio.FONT, text=text, color=0x0, x=4, y=24)
        else:
            group3[2]=Rect(2, 16, 126, 16, fill=0x0,outline = 0xFFFFFF)
            text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=4, y=24)
        text_area.scale = 1
        group3[3] = text_area
        
        group3[4]=Rect(0, 32, 128, 16, fill=0x0)
        text = "animation3"
        text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=4, y=40)
        text_area.scale = 1
        group3[5] = text_area
        
        group3[6]=Rect(0, 48, 128, 16, fill=0x0)
        text = "EXIT"
        text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=4, y=56)
        text_area.scale = 1
        group3[7] = text_area
        
        display.show(group3)
    if(menu == 4):
        group3[0]=Rect(0, 0, 128, 16, fill=0x0)
        text = "animation1"
        text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=4, y=8)
        text_area.scale = 1
        group3[1] = text_area
        
        group3[2]=Rect(0, 16, 128, 16, fill=0x0)
        text = "animation2"
        text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=4, y=24)
        text_area.scale = 1
        group3[3] = text_area
        
        text = "animation3"
        if(animselect == 4):
            group3[4]=Rect(0, 32, 128, 16, fill=0xFFFFFF)
            text_area = label.Label(terminalio.FONT, text=text, color=0x0, x=4, y=40)
        else:
            group3[4]=Rect(2, 32, 126, 16, fill=0x0,outline = 0xFFFFFF)
            text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=4, y=40)
        text_area.scale = 1
        group3[5] = text_area
        
        group3[6]=Rect(0, 48, 128, 16, fill=0x0)
        text = "EXIT"
        text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=4, y=56)
        text_area.scale = 1
        group3[7] = text_area
        
        display.show(group3)  
    if(menu == 5):
        group3[0]=Rect(0, 0, 128, 16, fill=0x0)
        text = "animation1"
        text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=4, y=8)
        text_area.scale = 1
        group3[1] = text_area
        
        group3[2]=Rect(0, 16, 128, 16, fill=0x0)
        text = "animation2"
        text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=4, y=24)
        text_area.scale = 1
        group3[3] = text_area
        
        group3[4]=Rect(0, 32, 128, 16, fill=0x0)
        text = "animation3"
        text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=4, y=40)
        text_area.scale = 1
        group3[5] = text_area
        
        group3[6]=Rect(0, 48, 128, 16, fill=0xFFFFFF)
        text = "EXIT"
        text_area = label.Label(terminalio.FONT, text=text, color=0x0, x=4, y=56)
        text_area.scale = 1
        group3[7] = text_area
        
        display.show(group3)  
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
