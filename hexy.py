# heartbeats
# Created at 2019-12-09 06:49:10.719102
# rmFowuD_TB6wLMqKU92xXQ
# Chip id retrieved f1005005501354e4ffffffffffff9300
# (Docking Station) registered with uid: j2ojeUDnSxyquUhTCPTlyg


import streams
from nxp.hexiwear import hexiwear
import threading
import fatfs
import flash
import os    # import file/directory management module


streams.serial()
hexi = hexiwear.HEXIWEAR()
storageHR = []
#variables
NEGRO = 0x0000
BLANCO = 0xFFFF
EDAD = 25
PESO = 0
HRMax = 0
HRMin = 0
STEPS = 5
medicionesHR = 8
SHOW_HR = True
edades = [10,20,30,35,40,45,50,55,60,65,70]
hBeats = (  [100,200],
            [95,190],
            [93,185],
            [90,180],
            [88,175],
            [85,170],
            [83,160],
            [80,160],
            [78,155],
            [75,150])

def perfil():
    #                TEXT      x     y     w     h   
    hexi.draw_text("Perfil", x=65, y=75, w=25, h=13, color=NEGRO, background=BLANCO, encode=False) #perfil derecha

def toggle_ble():#Guardar
    try:
        hexi.fill_screen(NEGRO, encode=True)
        print("Left Button Pressed")
        hexi.vibration(100)
        hexi.bt_driver.toggle_adv_mode()
    except Exception as e:
        print("error on left_pressed", e)

    
def print_paircode():
    print("Your Pair Code:",hexi.bt_driver.passkey)

def increment_age():
    print("function increment age")
    EDAD += 1;
    hexi.draw_text(str(EDAD), x=35, y=35, w=25,  h=25, color=NEGRO, background=BLANCO, encode=False) #EDAD
    encuentraBeats()

def decrement_age():
    print("function decrement age")
    EDAD -= 1;
    hexi.draw_text(str(EDAD), x=35, y=35, w=25,  h=25, color=NEGRO, background=BLANCO, encode=False) #EDAD
    encuentraBeats()

def increment_weight():
    PESO += 1;
    hexi.draw_text(str(PESO), x=35, y=35, w=25,  h=25, color=NEGRO, background=BLANCO, encode=False) #PESO

def decrement_weight():
    PESO -= 1;
    hexi.draw_text(str(PESO), x=35, y=35, w=25,  h=25, color=NEGRO, background=BLANCO, encode=False) #PESO
    
def screen_peso():
    try:
        print("Right Button Pressed")
        global SHOW_HR
        SHOW_HR = False
        hexi.draw_text("       ", x=35, y=55, w=25, h=25, color=NEGRO, background=NEGRO,  encode=False) #borrar Heart beats
        hexi.draw_text("Peso",    x=35, y=5,  w=25, h=13, color=NEGRO, background=BLANCO, encode=False) #arriba
        hexi.draw_text("Guardar", x=5,  y=75, w=25, h=13, color=NEGRO, background=BLANCO, encode=False) #izquierda
        
        hexi.draw_text(" ",       x=65, y=75, w=25, h=13, color=NEGRO, background=NEGRO,  encode=False) # borrar texto Perfil
        hexi.draw_text("+",       x=80, y=5,  w=5,  h=5,  color=NEGRO, background=BLANCO, encode=False)
        hexi.draw_text("--",      x=80, y=55, w=5,  h=2,  color=NEGRO, background=BLANCO, encode=False)
        hexi.draw_text("Edad",    x=55, y=75, w=35, h=13, color=NEGRO, background=BLANCO, encode=False) #Derecha
        hexi.draw_text(str(PESO), x=35, y=35, w=25, h=25, color=NEGRO, background=BLANCO, encode=False) #EDAD
        
        hexi.attach_button_up(increment_weight)
        hexi.attach_button_down(decrement_weight)
        hexi.attach_button_right(toggle_touch)
        hexi.attach_button_left(izquierda)
        
    except Exception as e:
        print("error on right_pressed", e)
        
def izquierda():
    hexi.draw_text("    ",    x=35, y=5,  w=25, h=13, color=NEGRO, background=NEGRO, encode=False) #arriba
    hexi.draw_text("      ", x=5,  y=75, w=25, h=13, color=NEGRO, background=NEGRO, encode=False) #izquierda
    hexi.draw_text("    ",       x=80, y=5,  w=5,  h=5,  color=NEGRO, background=NEGRO, encode=False)
    hexi.draw_text("  ",      x=80, y=55, w=5,  h=2,  color=NEGRO, background=NEGRO, encode=False)
    hexi.draw_text("    ",    x=55, y=75, w=35, h=13, color=NEGRO, background=NEGRO, encode=False) #Derecha
    hexi.draw_text("      ", x=35, y=35, w=25, h=25, color=NEGRO, background=NEGRO, encode=False) #EDAD
    global SHOW_HR
    SHOW_HR = True
    hexi.draw_text(str(hr)+ " bmp", x=35, y=35, w=25, h=25, color=NEGRO, background=BLANCO, encode=False) #Heart beats
    perfil()

def toggle_touch(): # - Al seleccionar perfil - mostramos a edad
    try:
        print("Right Button Pressed")
        global SHOW_HR
        SHOW_HR = False
        
        hexi.draw_text("     ",   x=40, y=35, w=25, h=25, color=NEGRO, background=NEGRO,  encode=False) #borrar Heart beats
        hexi.draw_text("Edad",    x=35, y=5,  w=25, h=13, color=NEGRO, background=BLANCO, encode=False) #arriba
        hexi.draw_text("Guardar", x=5,  y=75, w=25, h=13, color=NEGRO, background=BLANCO, encode=False) #izquierda
        
        hexi.draw_text(" ",       x=65, y=75, w=25, h=13, color=NEGRO, background=NEGRO,  encode=False) # borrar texto Perfil
        hexi.draw_text("+",       x=80, y=5,  w=5,  h=5,  color=NEGRO, background=BLANCO, encode=False)
        hexi.draw_text("--",      x=80, y=55, w=5,  h=2,  color=NEGRO, background=BLANCO, encode=False)
        hexi.draw_text("Peso",    x=55, y=75, w=35, h=13, color=NEGRO, background=BLANCO, encode=False) #Derecha
        hexi.draw_text(str(EDAD), x=35, y=35, w=25, h=25, color=NEGRO, background=BLANCO, encode=False) #EDAD
        
        hexi.attach_button_up(increment_age)
        hexi.attach_button_down(decrement_age)
        hexi.attach_button_right(screen_peso)
        hexi.attach_button_left(izquierda)
        
    except Exception as e:
        print("error on right_pressed", e)


# used to check the bluetooth status
pinMode(LED2, OUTPUT)

try:
    hexi.fill_screen(NEGRO, False)
    hexi.attach_button_right(toggle_touch)
    hexi.attach_passkey(print_paircode)
except Exception as e:
    print(e)
    
    
def read_bt_status():
    while True:
        bt_on, bt_touch, bt_link = hexi.bluetooth_info()
        digitalWrite(LED2, 0 if bt_on == 1 else 1)
        sleep(1000)

def encuentraBeats():
    for i in range(len(edades)-1):
        if(edades[i] < EDAD and edades[i+1] >= EDAD):
            HRMax = hBeats[i+1][0]
            HRMin = hBeats[i+1][1]

pinMode(LED0,OUTPUT)


def alertHightHR(hr):
    print("Entro 8")
    if(hr > HRMax):
        print("Pulsaciones altas")
        for i in range(5):
            digitalWrite(LED0, HIGH)  # turn the LED ON by setting the voltage HIGH
            # sleep(800)                # wait for a second is 1000
            # digitalWrite(LED0, LOW)   # turn the LED OFF by setting the voltage LOW
            # sleep(800)

def alertLowHR(hr):
    print("Entro 6")
    if(hr < HRMin):
        print("pulsaciones minimas")
        for i in range(10):
            hexi.vibration(200)  # turn vibration
            # sleep(800)                # wait for a second is 1000
        
def almacenaHR(hr):
    print("Entro 3")
    storageHR.append(hr)
    print("longitud: "+ str(len(storageHR)))
    # sleep(3000) #wait for three seconds to storage the heart rate
    if(len(storageHR) == 20): # Each 20 seconds you should save this array in a place to do analysis about that
        print(storageHR)        #but in this moment just empty the beats
        storageHR = []
        
def monitoreaHR(hr):
    almacenaHR(hr)
    print("Entro 4")
    alertLowHR(hr)
    print("Entro 7")
    alertHightHR(hr)
    print("Entro 9")
        
    
# almacena = threading.Thread(target = almacenaHR)
# almacena.start()

# lowHR = threading.Thread(target = alertLowHR)
# lowHR.start()

# HightHR = threading.Thread(target = alertHightHR)
# HightHR.start()

thread(read_bt_status)
#encuentraBeats()

        
while True:
    try:
        if (SHOW_HR):
            hr = hexi.get_heart_rate()
            print("Heart Rate", hr, "bpm")
            print("-------------------------------------------------------------------")
            if(medicionesHR >= STEPS):
                monitoreaHR(hr)
                medicionesHR = 0
            else:
                print("Entro 0")
                medicionesHR += 1
                print("Mediciones: " + str(medicionesHR))
            hexi.draw_text(str(hr)+ " bmp", x=35, y=35, w=25, h=25, color=NEGRO, background=BLANCO, encode=False) #Heart beats
            perfil()

    except Exception as e:
        print(e)
        sleep(3000)

