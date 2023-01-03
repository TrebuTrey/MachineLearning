from configparser import ConfigParser
import os

CFG_FN = "config.ini"
SECTION = "DEFAULT"

print(f"parsing: {CFG_FN}")
if not os.path.isfile(CFG_FN):
    raise FileNotFoundError(f"Unable to locate {CFG_FN}. Create {CFG_FN} according to https://docs.python.org/3.9/library/configparser.html#quick-start with {SECTION} section.")

config = ConfigParser()
config.read(CFG_FN)

RETROARCH_DIR = config.get(SECTION, "RETROARCH_DIR")
RETROARCH_CFG_FP = config.get(SECTION, "RETROARCH_CFG_FP")
RETROARCH_SCREENSHOTS_DIR = config.get(SECTION, "RETROARCH_SCREENSHOTS_DIR")

print(f"RETROARCH_DIR: {RETROARCH_DIR}")
print(f"RETROARCH_CFG_FP: {RETROARCH_CFG_FP}")
print(f"RETROARCH_SCREENSHOTS_DIR: {RETROARCH_SCREENSHOTS_DIR}")