#!/bin/bash

python -c "from mygpio import mygpio; from config import config as c; gpio = mygpio(c.LED_RED, c.LED_GREEN, c.LED_BLUE, c.BUZZER); gpio.clean()"

