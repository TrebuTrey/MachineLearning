import logging
import time

import __init__
from controller import delay
from emulator import Emulator
from helpers.log import mod_fname
logger = logging.getLogger(mod_fname(__file__))


if __name__ == "__main__":
    logger.info("running main")
    em = Emulator()
    em.run_game()
    em.fast_fwd_on()
    delay(3)
    for i in range(5):
        for j in range(3):
            em.fast_fwd_off()
            em.cont.press_a()
            em.fast_fwd_on()
            delay(0.2)
        em.cont.move_down()
        delay(2)
        em.reset()
        delay(5)
    