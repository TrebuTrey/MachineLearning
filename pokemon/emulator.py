from enum import Enum
import logging
import os
import platform

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from PIL import Image
import pyautogui as gui

from config import (
    EMULATOR_NAME, RETROARCH_APP_FP, RETROARCH_SCREENSHOTS_DIR
)
from controller import EmulatorController, delay, nav_to_game, press_key
from helpers.log import mod_fname
logger = logging.getLogger(mod_fname(__file__))


class ToggleState(str, Enum):
    """Enumeration for toggling on/off."""
    ON = 'on'
    OFF = 'off'


class Emulator():
    """Take actions inside an emulator."""
    def __init__(self):
        self.cont = EmulatorController()
        self.state = EmulatorState()
    
    def run_game(self):
        """Run the game inside the emulator."""
        self.launch()
        delay(2)  # make sure the system is opening up with proper time so the click can register in the focus window
        nav_to_game()
        delay(0.5)
        press_key("Enter")
    
    def launch(self):
        """Launch the emulator application."""
        logger.info(f"launching {EMULATOR_NAME} emulator")
        if platform.system() == "Darwin":
            logger.debug(f"opening {RETROARCH_APP_FP}")
            os.system(f"open {RETROARCH_APP_FP}")
        elif platform.system() == "Windows":
            gui.hotkey("ctrl", "esc")
            gui.write(EMULATOR_NAME)
            gui.press("Enter")

    def is_start_menu(self):  #make sure that screenshots folder is cleared before beginning a different ROM for parsing
        self.take_screenshot()
        currentImage = os.listdir(RETROARCH_SCREENSHOTS_DIR)[len(os.listdir(RETROARCH_SCREENSHOTS_DIR)) - 1]
        previousImage = os.listdir(RETROARCH_SCREENSHOTS_DIR)[len(os.listdir(RETROARCH_SCREENSHOTS_DIR)) - 2]

        pic1 = os.path.join(RETROARCH_SCREENSHOTS_DIR , currentImage)
        pic2 = os.path.join(RETROARCH_SCREENSHOTS_DIR , previousImage)

        img1 = mpimg.imread(pic1)
        img2 = mpimg.imread(pic2)
        plt.imshow(img1)
        plt.show()

        im = Image.open(pic1)
        width, height = im.size

        left = 4*width/7
        top = 0
        right = width
        bottom = 3*height/7

        im1 = im.crop((left, top, right, bottom))
        im1.show()

    def fast_fwd_on(self):
        """Turn fast forwad ON."""
        if self.state.is_fast_fwd_off():
            self.cont.toggle_fast_fwd()
            self.state.fast_fwd_on()
        logger.debug("fast forward is ON")
    
    def fast_fwd_off(self):
        """Turn fast forwad OFF."""
        if self.state.is_fast_fwd_on():
            self.cont.toggle_fast_fwd()
            self.state.fast_fwd_off()
        logger.debug("fast forward is OFF")
    
    def reset(self):
        """Reset the emulator."""
        self.cont.press_reset_btn()
        logger.debug("emulator reset")
    
    def take_screenshot(self):
        """Take a screenshot in the emulator."""
        self.cont.press_screenshot_btn()
        logger.debug("screenshot taken")


class EmulatorState():
    """Track state inside an emulator."""
    def __init__(self):
        self.fast_fwd = ToggleState.OFF
    
    def is_fast_fwd_on(self) -> bool:
        return self.fast_fwd == ToggleState.ON
    
    def is_fast_fwd_off(self) -> bool:
        return self.fast_fwd == ToggleState.OFF
    
    def fast_fwd_on(self):
        self.fast_fwd = ToggleState.ON
    
    def fast_fwd_off(self):
        self.fast_fwd = ToggleState.OFF


if __name__ == "__main__":
    em = Emulator()
    em.is_start_menu()