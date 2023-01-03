import os
import platform
import time

import pyautogui as gui           #pyautogui is great for hotkeys and utilizing special characters on the system level, but it cannot register output in the applications
if platform.system() == "Windows":
    import pydirectinput as inp   #pydirect input is perfect for controlling common button presses with the emulator development

from config import (
    EMULATOR_NAME, RETROARCH_APP_FP,
    RETROARCH_DIR, RETROARCH_CFG_FP, RETROARCH_SCREENSHOTS_DIR
)


class EmulatorController():

    def __init__(self, player_num: int = 1):
        self.player_num = player_num
        
        # parse the config file
        keybind = f"input_player{player_num}_"
        a_btn_str = f"{keybind}a = "
        b_btn_str = f"{keybind}b = "
        start_btn_str = f"{keybind}start = "
        select_btn_str = f"{keybind}select = "
        up_btn_str = f"{keybind}up = "
        down_btn_str = f"{keybind}down = "
        left_btn_str = f"{keybind}left = "
        right_btn_str = f"{keybind}right = "
        fast_fwd_btn_str = "input_toggle_fast_forward = "
        reset_btn_str = "input_reset = "
        screenshot_btn_str = "input_screenshot = "

        def _clean_line(line: str, sub_str: str) -> str:
            return line.replace(sub_str, "").replace("\"", "").replace("\n", "")

        with open(RETROARCH_CFG_FP, "r") as infile:
            for line in infile:
                if a_btn_str in line:
                    self.a_btn = _clean_line(line, a_btn_str)
                elif b_btn_str in line:
                    self.b_btn = _clean_line(line, b_btn_str)
                elif start_btn_str in line:
                    self.start_btn = _clean_line(line, start_btn_str)
                elif select_btn_str in line:
                    self.select_btn = _clean_line(line, select_btn_str)
                elif up_btn_str in line:
                    self.up_btn = _clean_line(line, up_btn_str)
                elif down_btn_str in line:
                    self.down_btn = _clean_line(line, down_btn_str)
                elif left_btn_str in line:
                    self.left_btn = _clean_line(line, left_btn_str)
                elif right_btn_str in line:
                    self.right_btn = _clean_line(line, right_btn_str)
                elif fast_fwd_btn_str in line:
                    self.fast_fwd_btn = _clean_line(line, fast_fwd_btn_str)
                elif reset_btn_str in line:
                    self.reset_btn = _clean_line(line, reset_btn_str)
                elif screenshot_btn_str in line:
                    self.screenshot_btn = _clean_line(line, screenshot_btn_str)
                else:
                    pass
    
    def press_a(self):
        self._press_btn_emulator(self.a_btn)
    
    def press_b(self):
        self._press_btn_emulator(self.b_btn)
    
    def press_start(self):
        self._press_btn_emulator(self.start_btn)
    
    def press_select(self):
        self._press_btn_emulator(self.select_btn)
    
    def move_up(self):
        self._press_btn_emulator(self.up_btn)
    
    def move_down(self):
        self._press_btn_emulator(self.down_btn)
    
    def move_left(self):
        self._press_btn_emulator(self.left_btn)
    
    def move_right(self):
        self._press_btn_emulator(self.right_btn)
    
    def fast_fwd(self):
        self._press_btn_emulator(self.fast_fwd_btn)

    def reset(self):
        self._press_btn_emulator(self.reset_btn)
    
    def take_screenshot(self):
        self._press_btn_emulator(self.screenshot_btn)
    
    def _press_btn_emulator(self, btn: str):
        if platform.system() == "Darwin":
            press_mac_key(btn)
        elif platform.system() == "Windows":
            inp.typewrite(btn)


def press_mac_key(key: str):
    print(f"pressing key: {key}")
    gui.keyDown(key)
    gui.keyUp(key)


def open_emulator():
    if platform.system() == "Darwin":
        os.system(f"open {RETROARCH_APP_FP}")
        time.sleep(5)
        press_mac_key('left')
        time.sleep(0.5)
        press_mac_key('down')
        press_mac_key('down')
        time.sleep(1)
        press_mac_key('right')
        time.sleep(0.5)
        press_mac_key('enter')
        time.sleep(0.5)
        press_mac_key('enter')
    elif platform.system() == "Windows":
        gui.hotkey("ctrl", "esc")
        gui.write(EMULATOR_NAME)
        gui.press("Enter")
        time.sleep(1)                   # make sure the system is opening up with proper time so the click can register in the focus window
        inp.press("right" ,presses=3)
        inp.press("Enter", presses=2)


def control_mouse(): #establish where your X and Y position of the emulator will be on your screen so the mouse click in OpenEmulator will be set properly
    try:
        while True:
            x, y = gui.position()
            positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
            print(positionStr, end='')
            print('\b' * len(positionStr), end='', flush=True)
    except KeyboardInterrupt:
        print('\n')        
