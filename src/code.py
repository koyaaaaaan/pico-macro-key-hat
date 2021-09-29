import board
import busio
import time
import usb_hid
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_jp import KeyboardLayoutJP
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
import board
import digitalio
import config
import displayio
from adafruit_st7789 import ST7789
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
import supervisor

# Circuit Configlation
PIN_UP = board.GP2
PIN_DOWN = board.GP18
PIN_LEFT = board.GP16
PIN_RIGHT = board.GP20
PIN_CENTER = board.GP3
PIN_A = board.GP15
PIN_B = board.GP17
PIN_X = board.GP19
PIN_Y = board.GP21
PIN_SCK_DISPLAY = board.GP10
PIN_SDA_DISPLAY = board.GP11
PIN_CHIPSELECT_DISPLAY = board.GP9
PIN_DATACOMMAND_DISPLAY = board.GP8
PIN_RESET_DISPLAY = board.GP12
DISPLAY_WIDTH = 240
DISPLAY_HEIGHT = 240
LOOP_WAIT = 0.05
LOCK_TIME = 2 / LOOP_WAIT

# COLOR CONFIG
TITLE_COLOR = 0xFFFFFF
TEXT_COLOR = 0xEEEEEE

BG_LOGO = 0x0000CD
BG_LOCK = 0x696969
BG_UNLOCK = 0x0000CD
BG_CENTER = 0x2F4F4F
BG_UP = 0x8B0000
BG_DOWN = 0x4B0082
BG_LEFT = 0xC71585
BG_RIGHT = 0x6A5ACD

# Auto Reload OFF.
# Avoiding unreleased gpip10 when AutoReload
supervisor.disable_autoreload()

# ready keyboard
keyboard = Keyboard(usb_hid.devices)
layout = None

# ready buttons
J_UP = digitalio.DigitalInOut(PIN_UP)
J_UP.direction = digitalio.Direction.INPUT
J_UP.pull = digitalio.Pull.UP
J_DOWN = digitalio.DigitalInOut(PIN_DOWN)
J_DOWN.direction = digitalio.Direction.INPUT
J_DOWN.pull = digitalio.Pull.UP
J_LEFT = digitalio.DigitalInOut(PIN_LEFT)
J_LEFT.direction = digitalio.Direction.INPUT
J_LEFT.pull = digitalio.Pull.UP
J_RIGHT = digitalio.DigitalInOut(PIN_RIGHT)
J_RIGHT.direction = digitalio.Direction.INPUT
J_RIGHT.pull = digitalio.Pull.UP
J_CENTER = digitalio.DigitalInOut(PIN_CENTER)
J_CENTER.direction = digitalio.Direction.INPUT
J_CENTER.pull = digitalio.Pull.UP

btnA = digitalio.DigitalInOut(PIN_A)
btnA.direction = digitalio.Direction.INPUT
btnA.pull = digitalio.Pull.UP
btnB = digitalio.DigitalInOut(PIN_B)
btnB.direction = digitalio.Direction.INPUT
btnB.pull = digitalio.Pull.UP
btnX = digitalio.DigitalInOut(PIN_X)
btnX.direction = digitalio.Direction.INPUT
btnX.pull = digitalio.Pull.UP
btnY = digitalio.DigitalInOut(PIN_Y)
btnY.direction = digitalio.Direction.INPUT
btnY.pull = digitalio.Pull.UP

# ready display
spi = busio.SPI(clock=PIN_SCK_DISPLAY, MOSI=PIN_SDA_DISPLAY)
while not spi.try_lock():
    pass
spi.configure(baudrate=24000000) # Configure SPI for 24MHz
spi.unlock()

displayio.release_displays()
display_bus = displayio.FourWire(spi, command=PIN_DATACOMMAND_DISPLAY, chip_select=PIN_CHIPSELECT_DISPLAY, reset=PIN_RESET_DISPLAY)
display = ST7789(display_bus, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, rowstart=80, rotation=270)

# Make the display context
passSplash = None # use for lock screen

# load font
font_file = "Junction-regular-24.pcf"
font = bitmap_font.load_font(font_file)

def bgFill(color):
    color_bitmap = displayio.Bitmap(DISPLAY_WIDTH, DISPLAY_HEIGHT, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = color
    bg_sprite = displayio.TileGrid(color_bitmap,pixel_shader=color_palette,x=0, y=0)
    return bg_sprite

def textGrp(_scale, _x, _y, _text, _color):
    text_group = displayio.Group(scale=_scale, x=_x, y=_y)
    text_group.append(label.Label(font, text=_text, color=_color))
    return text_group

def logo():
    splash = displayio.Group()
    display.show(splash)
    splash.append(bgFill(BG_LOGO))
    splash.append(textGrp(1,5,70,"Welcome to",TITLE_COLOR))
    splash.append(textGrp(1,5,120,"Custom Key",TITLE_COLOR))
    splash.append(textGrp(1,5,170,"Version 3",TITLE_COLOR))
    time.sleep(3)

def textShow(title,text1,text2,text3,text4,bgColor, titlecolor,color):
    splash = displayio.Group()
    display.show(splash)
    splash.append(bgFill(bgColor))
    splash.append(textGrp(1,5,30,title,titlecolor))
    splash.append(textGrp(1,5,80,text1,color))
    splash.append(textGrp(1,5,120,text2,color))
    splash.append(textGrp(1,5,160,text3,color))
    splash.append(textGrp(1,5,200,text4,color))
    
def isPressed(currentVal, preVal):
    if preVal == True and currentVal == False:
        return True
    else:
        return False

def lockLoop():
    if config.uselock == False or len(config.lockpin) == 0:
      setLayout()
      return

    pin = []
    passText()
    time.sleep(0.1)
    preBtnValCENTER = J_CENTER.value
    preBtnValA = btnA.value
    preBtnValB = btnB.value
    preBtnValX = btnX.value
    preBtnValY = btnY.value

    while True:
        stateCENTER = isPressed(J_CENTER.value, preBtnValCENTER)
        stateA = isPressed(btnA.value, preBtnValA)
        stateB = isPressed(btnB.value, preBtnValB)
        stateX = isPressed(btnX.value, preBtnValX)
        stateY = isPressed(btnY.value, preBtnValY)
        preBtnValCENTER = J_CENTER.value
        preBtnValA = btnA.value
        preBtnValB = btnB.value
        preBtnValX = btnX.value
        preBtnValY = btnY.value

        if stateCENTER:
            if checkPin(pin):
              setLayout()
              return
            pin = []
            passText()
        elif stateA:
            pin.append("A")
            passTextAdd(len(pin), "*")
        elif stateB:
            pin.append("B")
            passTextAdd(len(pin), "*")
        elif stateX:
            pin.append("X")
            passTextAdd(len(pin), "*")
        elif stateY:
            pin.append("Y")
            passTextAdd(len(pin), "*")
        else:
            pass

        time.sleep(0.05)  


def passText():
    global passSplash
    passSplash = displayio.Group()
    display.show(passSplash)
    passSplash.append(bgFill(BG_LOCK))
    passSplash.append(textGrp(1,5,30,"Locked",TITLE_COLOR))
    passSplash.append(textGrp(1,5,80,"Enter the Pin.",TEXT_COLOR))
    passSplash.append(textGrp(1,5,140,">> ",TEXT_COLOR))

def passTextAdd(times, subtext):
    passSplash.append(textGrp(1, 40 + (20 * times) ,140 ,subtext,TEXT_COLOR))

def checkPin(pin):
    if len(pin) != len(config.lockpin):
      return False
    for i in range(len(config.lockpin)): 
      if pin[i] != config.lockpin[i]:
        return False
    return True

def setLayout():
    global layout
    if config.layoutType == "jp":
      layout = KeyboardLayoutJP(keyboard)
    else:
      layout = KeyboardLayoutUS(keyboard)
    textShow("Unlocked!", "You got it.","Welcome to",
             "Custom Key 3",
             "           ( ^_^)b", BG_UNLOCK , TITLE_COLOR, TEXT_COLOR)
    time.sleep(2.5)

def getKeyCodes(idx, btnIdx):
    return config.keymap[idx]["data"][btnIdx]["value"]
        
def keysend(strVal):
    global layout
    layout.write(strVal)
    time.sleep(0.1)

def titleShow(sidx):
    sidxStr = str(sidx)
    title = "[UNKNOWN]"
    bgC = 0x000000
    if sidx == 0:
        title = "[CENTER]"
        bgC = BG_CENTER
    elif sidx == 1:
        title = "[UP]"
        bgC = BG_UP
    elif sidx == 2:
        title = "[DOWN]"
        bgC = BG_DOWN
    elif sidx == 3:
        title = "[LEFT]"
        bgC = BG_LEFT
    elif sidx == 4:
        title = "[RIGHT]"
        bgC = BG_RIGHT
    textShow(title
            ,"1. " + config.keymap[sidx]["data"][0]["label"]
            ,"2. " + config.keymap[sidx]["data"][1]["label"]
            ,"3. " + config.keymap[sidx]["data"][2]["label"]
            ,"4. " + config.keymap[sidx]["data"][3]["label"]
            , bgC ,TITLE_COLOR, TEXT_COLOR)

def mainLoop():
    lockLoop()
    lockTimeCount = 0
    macroIdx = 0
    titleShow(macroIdx)
    
    preBtnValUP = J_UP.value
    preBtnValDOWN = J_DOWN.value
    preBtnValLEFT = J_LEFT.value
    preBtnValRIGHT = J_RIGHT.value
    preBtnValCENTER = J_CENTER.value
    preBtnValA = btnA.value
    preBtnValB = btnB.value
    preBtnValX = btnX.value
    preBtnValY = btnY.value
    
    while True:
        stateUP = isPressed(J_UP.value, preBtnValUP)
        stateDOWN = isPressed(J_DOWN.value, preBtnValDOWN)
        stateLEFT = isPressed(J_LEFT.value, preBtnValLEFT)
        stateRIGHT = isPressed(J_RIGHT.value, preBtnValRIGHT)
        stateCENTER = isPressed(J_CENTER.value, preBtnValCENTER)
        stateA = isPressed(btnA.value, preBtnValA)
        stateB = isPressed(btnB.value, preBtnValB)
        stateX = isPressed(btnX.value, preBtnValX)
        stateY = isPressed(btnY.value, preBtnValY)
        
        preBtnValUP = J_UP.value
        preBtnValDOWN = J_DOWN.value
        preBtnValLEFT = J_LEFT.value
        preBtnValRIGHT = J_RIGHT.value
        preBtnValCENTER = J_CENTER.value
        preBtnValA = btnA.value
        preBtnValB = btnB.value
        preBtnValX = btnX.value
        preBtnValY = btnY.value

        if J_CENTER.value == False:
          lockTimeCount = lockTimeCount + 1
          if lockTimeCount > LOCK_TIME:
            lockTimeCount = 0
            lockLoop()
            macroIdx = 0
            titleShow(macroIdx)

        if stateCENTER:
          macroIdx = 0
          titleShow(macroIdx)
          lockTimeCount = 0
        elif stateUP:
          macroIdx = 1
          titleShow(macroIdx)
        elif stateDOWN:
          macroIdx = 2
          titleShow(macroIdx)
        elif stateLEFT:
          macroIdx = 3
          titleShow(macroIdx)
        elif stateRIGHT:
          macroIdx = 4
          titleShow(macroIdx)
        elif stateA:
          keysend(getKeyCodes(macroIdx, 0))
        elif stateB:
          keysend(getKeyCodes(macroIdx, 1))
        elif stateX:
          keysend(getKeyCodes(macroIdx, 2))
        elif stateY:
          keysend(getKeyCodes(macroIdx, 3))
        
        time.sleep(LOOP_WAIT)
        

logo()
mainLoop()



