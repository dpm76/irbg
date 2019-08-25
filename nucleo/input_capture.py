from pyb import Timer
from stm import mem32, TIM1, TIM2, TIM_SMCR, TIM_CCER

configset = {
    "F767_16bit": { 
        "timer": 1, 
        "timer-period": 0xffff,
        "timer-addr": TIM1,
        "pin-capture": pyb.Pin.board.D6,
        "led-timer": 8,
        "led-freq": 8,
        "led-id": 1
    },
    "F767_32bit": { 
        "timer": 2, 
        "timer-period": 0x3fffffff,
        "timer-addr": TIM2,
        "pin-capture": pyb.Pin.board.D13,
        "led-timer": 8,
        "led-freq": 8,
        "led-id": 1
    }
}

config = configset["F767_32bit"]


def capturePwm(ch):

    cap = ch.capture()

    while True:
        
        tmp = ch.capture()
        if tmp < 2000 and tmp != cap:
            throttle = (tmp-1000)/10
            print("{0}%".format(throttle))
            
            
def capture(ch):

    cap = ch.capture()
    while True:
            
        tmp = ch.capture()
        if tmp != cap:    
            print(tmp)
            cap = tmp
                
            
def main():
    # Configure timer2 as a microsecond counter.
    tim = Timer(config["timer"], prescaler=(machine.freq()[0]//1000000)-1, period=config["timer-period"])
    tim2 = Timer(config["led-timer"], freq=config["led-freq"])
    tim2.callback(lambda t: pyb.LED(config["led-id"]).toggle())

    # Configure channel for timer IC.
    ch = tim.channel(1, Timer.IC, pin=config["pin-capture"], polarity=Timer.FALLING)

    # Slave mode disabled in order to configure
    mem32[config["timer-addr"] + TIM_SMCR] = 0

    # Reset on rising edge (or falling in case of inverted detection). Ref: 25.4.3 of STM32F76xxx_reference_manual.pdf
    mem32[config["timer-addr"] + TIM_SMCR] = (mem32[config["timer-addr"] + TIM_SMCR] & 0xfffe0000) | 0x54

    # Capture sensitive to rising edge. Ref: 25.4.9 of STM32F76xxx_reference_manual.pdf
    mem32[config["timer-addr"] + TIM_CCER] = 0b1011

    print("capturing")
    capture(ch)
    

if __name__ == "__main__":
    main()
