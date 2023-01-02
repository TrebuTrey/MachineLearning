import os
import platform

import pyautogui as gui

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

            outfile.write("a = " + aButton)
            outfile.write("b = " + bButton)
            outfile.write("start = " + startButton)
            outfile.write("select = " + selectButton)
            outfile.write("up = " + upButton)
            outfile.write("down = " + downButton)
            outfile.write("left = " + leftButton)
            outfile.write("right = " + rightButton)

        
    

def openEmulator():
    compOS = platform.system()

    if compOS == 'Windows':
        gui.hotkey('ctrl', 'esc')
        gui.write('RetroArch')
        gui.press('Enter')
        # gui.press('right-arrow-key')


cont = Controller()
# openEmulator()


# pyautogui.press('e')