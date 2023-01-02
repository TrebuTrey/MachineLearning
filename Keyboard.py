import os
import platform
import sys
import time

import pyautogui as gui         #pyautogui is great for hotkeys and utilizing special characters on the system level, but it cannot register output in the applications
import pydirectinput as inp     #pydirect input is perfect for controlling common button presses with the emulator development

class Controller():
    FILEPATH = os.path.join('D:', 'Emulator', 'RetroArch', 'retroarch.cfg') #make sure you use '/' and not '\' when designating your directory
    FILEPATH

    KEYBIND = "input_player1_"
    aButton = 'a = '
    bButton = 'b = '
    startButton = 'start = '
    selectButton = 'select = '
    upButton = 'up = '
    downButton = 'down = '
    leftButton = 'left = '
    rightButton = 'right = '
    fastForward = 'input_toggle_fast_forward = '
    with open(FILEPATH, 'r') as infile, open('input1_1.txt', 'w') as outfile:
            for line in infile:
                if KEYBIND in line:
                    # outfile.write(line.replace(KEYBIND, ""))
                    line = line.replace(KEYBIND, "")
                    line = line.replace('"', "")
                    if aButton == line[0:len(aButton)]:
                        aButton = line.replace(aButton, "")
                    if bButton == line[0:len(bButton)]:
                        bButton = line.replace(bButton, "")
                    if startButton == line[0:len(startButton)]:
                        startButton = line.replace(startButton, "")
                    if selectButton == line[0:len(selectButton)]:
                        selectButton = line.replace(selectButton, "")
                    if upButton == line[0:len(upButton)]:
                        upButton = line.replace(upButton, "")
                    if downButton == line[0:len(downButton)]:
                        downButton = line.replace(downButton, "")
                    if leftButton == line[0:len(leftButton)]:
                        leftButton = line.replace(leftButton, "")
                    if rightButton == line[0:len(rightButton)]:
                        rightButton = line.replace(rightButton, "")
                if fastForward in line:
                    line = line.replace(fastForward, "")
                    line = line.replace('"', "")
                    fastForward = line

            outfile.write("a = " + aButton)
            outfile.write("b = " + bButton)
            outfile.write("start = " + startButton)
            outfile.write("select = " + selectButton)
            outfile.write("up = " + upButton)
            outfile.write("down = " + downButton)
            outfile.write("left = " + leftButton)
            outfile.write("right = " + rightButton)
            outfile.write("ff = " + fastForward)
    

def mouseControl(): #establish where your X and Y position of the emulator will be on your screen so the mouse click in OpenEmulator will be set properly
    try:
        while True:
            x, y = gui.position()
            positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
            print(positionStr, end='')
            print('\b' * len(positionStr), end='', flush=True)
    except KeyboardInterrupt:
        print('\n')        
    

def openEmulator():
    compOS = platform.system()
    
    if compOS == 'Windows':
        gui.hotkey('ctrl', 'esc')
        gui.write('RetroArch')
        gui.press('Enter')
        time.sleep(3)                   # make sure the system is opening up with proper time so the click can register in the focus window
        gui.leftClick(x= 300, y= 300)
        time.sleep(3)
        inp.press('backspace')
        inp.press('right' ,presses=3)
        inp.press('down')
        inp.press('Enter', presses=2)
        


cont = Controller()
a = cont.aButton
b = cont.bButton
st = cont.startButton
se = cont.selectButton
u = cont.upButton
d = cont.downButton
l = cont.leftButton
r = cont.rightButton
ff = cont.fastForward
openEmulator()
time.sleep(5)
inp.typewrite(a*100)
# mouseControl()

