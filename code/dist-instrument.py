from ultrasonic import Ultrasonic
from buzzer import Buzzer

import time

def main():

    GPIO_TRIGGER = 66 #P8.7
    GPIO_ECHO    = 67 #P8.8
    PWM_PORT     = 6  #P8.13

    LPF_A = 0.5

    MIN_DIST = 50.0
    MAX_DIST = 150.0
    DIST_RANGE = MAX_DIST - MIN_DIST

    MIN_FREQ = 220
    MAX_FREQ = 880
    FREQ_RANGE = MAX_FREQ - MIN_FREQ

    try:
        print("Press Ctrl+C to finish")
        meter = Ultrasonic(GPIO_TRIGGER, GPIO_ECHO)
        buzz = Buzzer(6)

        dist = meter.read()
        time.sleep(0.5)
        while True:

            distRead = meter.read()

            if distRead != Ultrasonic.OUT_OF_RANGE:
                
                dist += (distRead - dist) * LPF_A
                print("~ {0:.3f} cm".format(dist))
                
                if dist > MIN_DIST and dist < MAX_DIST:
                    freq = (((dist - MIN_DIST) / DIST_RANGE) * FREQ_RANGE) + MIN_FREQ
                    buzz.playNote(freq, 0.5)

                else:
                    time.sleep(0.5)
                
            else:
                print("Out of range!")
                time.sleep(0.5)

    except KeyboardInterrupt:
        print("\nCtrl+C pressed.")

    finally:
        print("Bye!")
        meter.cleanup()
        buzz.cleanup()


if __name__ == '__main__':

    main()
