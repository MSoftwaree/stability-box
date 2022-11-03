from core.sfar_device import SfarModules
import time

sfar = SfarModules()

while True:
    sfar.set_all_leds(65535)
    time.sleep(1)
    sfar.set_all_leds(0)
    time.sleep(0.5)
    for loop in range(16):
        sfar.set_do_sfar_green(loop, True)
        time.sleep(0.1)
        sfar.set_do_sfar_green(loop, False)
        time.sleep(0.1)
        sfar.set_do_sfar_red(loop, True)
        time.sleep(0.1)
        sfar.set_do_sfar_red(loop, False)
        time.sleep(0.1)

