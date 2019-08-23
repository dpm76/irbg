from pyb import Timer
from stm import mem32, TIM1, TIM_SMCR, TIM_CCER

# Configure timer2 as a microsecond counter.
tim = Timer(1, prescaler=(machine.freq()[0]//1000000)-1, period=0xffff)
tim2 = Timer(8, freq=8)
tim2.callback(lambda t: pyb.LED(1).toggle())

# Configure channel1 on PA0 for timer IC.
ch = tim.channel(1, Timer.IC, pin=pyb.Pin.board.D6, polarity=Timer.FALLING)

# Slave mode disabled in order to configure
mem32[TIM1 + TIM_SMCR] = 0

# Reset on rising edge (or falling in case of inverted detection). Ref: 25.4.3 of STM32F76xxx_reference_manual.pdf
mem32[TIM1 + TIM_SMCR] = (mem32[TIM1 + TIM_SMCR] & 0xfffe0000) | 0x54

# Capture sensitive to rising edge. Ref: 25.4.9 of STM32F76xxx_reference_manual.pdf
mem32[TIM1 + TIM_CCER] = 0b1011

print("capturing")
cap = ch.capture()
while True:
    
    tmp = ch.capture()
    #while tmp == 0:
    #    tmp = ch.capture()
        
    if tmp < 2000 and tmp != cap:
        throttle = (tmp-1000)/10
        print("{0}%".format(throttle))
        freq = (throttle / 4) + 1 if throttle > 0 else 1
        tim2.init(freq=int(freq))
        cap = tmp
