import logging
import time

import __init__
from controller import EmulatorController, open_emulator
from helpers.log import mod_fname
logger = logging.getLogger(mod_fname(__file__))


if __name__ == "__main__":
    logger.info("running main")
    controller = EmulatorController()
    open_emulator()
    controller.fast_fwd()
    time.sleep(1)
    controller.fast_fwd()
    for i in range(5):
        for i in range(10):
            controller.move_up()
            controller.take_screenshot()
        time.sleep(1)
        controller.reset()
        time.sleep(15)