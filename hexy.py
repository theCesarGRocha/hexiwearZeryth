################################################################################
# Basic example of use for Hexiwear Library
#
# Created: 2017-03-30 07:55:48.081359
#
################################################################################

import streams
from nxp.hexiwear import hexiwear
import threading
import zLogo
import fatfs
import flash
import os    # import file/directory management module


streams.serial()
hexi = hexiwear.HEXIWEAR()

#variables
safe_age = False
NEGRO = 0x0000
BLANCO = 0xFFFF
EDAD = 25
PESO = 0
HRMax = 0
HRMin = 0
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
c = 0

def pressed_up():
    print("Up Button Pressed")
    hexi.vibration(100)
    hexi.enable_bt_upd_sensors()

def pressed_down():
    print("Down Button Pressed")
    hexi.vibration(100)
    hexi.disable_bt_upd_sensors()

def perfil():
    #                TEXT      x     y     w     h   
    hexi.draw_text("Perfil", x=65, y=75, w=25, h=13, color=NEGRO, background=BLANCO, encode=False) #perfil derecha

def toggle_ble():#Guardar
    try:
        hexi.fill_screen(NEGRO, encode=True)
        #SHOW_HR = True
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
        # leer_peso()
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
    print("izquierda")


def leer_peso():
    new_resource("DATA_PESO.txt")
    ff = open("resource://DATA_PESO.txt")
    line = ff.readline()
    global PESO
    PESO = int(line)
    print("LINE PESO ", PESO)
    
def guardar_peso():
    new_resource("DATA_PESO.txt")
    f = open("resource://DATA_PESO.txt","w+")
    f.write(PESO)
    #f.close() 
    print("Peso guardado")
    
def guardar_edad():
    new_resource("DATA_EDAD.txt")
    print("1")
    f = open("resource://DATA_EDAD.txt", "w+")
    print("2")
    print("EDAD ", EDAD)
    line = f.readline()
    print("LINE ", line)
    f.write(str(EDAD))
    print("3")
    print("Edad guardada")

    
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
    print('Entro - encuentraBeats')
    for i in range(len(edades)-1):
        print('Entro - encuentraBeats For  i: ' , i)
        print(hBeats[i][0], hBeats[i][1])
        if(edades[i] < EDAD and edades[i+1] >= EDAD):
            HRMax = hBeats[i+1][0]
            HRMin = hBeats[i+1][1]
            print('HRMax: ' , HRMax)
            print('HRMin: ' , HRMin)

thread(read_bt_status)
#encuentraBeats()

        
while True:
    try:
        if (SHOW_HR):
            print("SHOW_HR: ", str(SHOW_HR))
            hr = hexi.get_heart_rate()
            print("Heart Rate", hr, "bpm")
            print("------------------------------------------------------------------------------")
            if(hr > HRMax):
                print("Pulsaciones altas")
            if(hr < HRMin):
                print("pulsaciones minimas")
            hexi.draw_text(str(hr)+ " bmp", x=35, y=35, w=25, h=25, color=NEGRO, background=BLANCO, encode=False) #Heart beats
            perfil()
            c += 1
        sleep(3000)
        
    except Exception as e:
        print(e)
        sleep(3000)
        
        
        
        
        
        
