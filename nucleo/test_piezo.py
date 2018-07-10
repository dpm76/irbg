from time import sleep

def buzz(pin, timer, channel, freq, time):

	t = pyb.Timer(timer, freq=freq)
	#t.callback(lambda t: p.value( 0 if p.value() == 1 else 1))
	t.channel(channel, pyb.Timer.PWM, pin=p, pulse_width_percent=50.0)
	sleep(time)
	t.deinit()

# Notes durations
W = 1.0  # Whole
H = 0.5  # Half
Q = 0.25 # Quarter
E = 0.125 # Eighth
S = 0.0625 # Sixteenth

p = pyb.Pin.board.D10
p.init(pyb.Pin.AF_PP,af=pyb.Pin.AF2_TIM4)

pyb.Pin.board.LED1.off()
pyb.Pin.board.LED2.off()
pyb.Pin.board.LED3.off()

pyb.Pin.board.LED1.on()
pyb.Pin.board.LED2.on()
pyb.Pin.board.LED3.on()

sleep(0.2)

pyb.Pin.board.LED1.off()
pyb.Pin.board.LED2.off()
pyb.Pin.board.LED3.off()

sleep(0.2)

pyb.Pin.board.LED1.on()
pyb.Pin.board.LED2.on()
pyb.Pin.board.LED3.on()

sleep(0.2)

pyb.Pin.board.LED1.off()
pyb.Pin.board.LED2.off()
pyb.Pin.board.LED3.off()

sleep(0.2)

pyb.Pin.board.LED1.on()
pyb.Pin.board.LED2.on()
pyb.Pin.board.LED3.on()

sleep(0.2)

pyb.Pin.board.LED1.off()
pyb.Pin.board.LED2.off()
pyb.Pin.board.LED3.off()

sleep(0.2)

buzz(p, 4, 3, 110.0, E-S)
sleep(S)
buzz(p, 4, 3, 110.0, E-S)
sleep(S)
buzz(p, 4, 3, 880.0, Q-S)
sleep(H+S)

pyb.Pin.board.LED2.on()
buzz(p, 4, 3, 440.0, E)
pyb.Pin.board.LED2.off()

pyb.Pin.board.LED1.on()
buzz(p, 4, 3, 220.0, E)
pyb.Pin.board.LED1.off()

buzz(p, 4, 3, 110.0, E+S)

sleep(S)

pyb.Pin.board.LED3.on()
buzz(p, 4, 3, 880.0, E)
pyb.Pin.board.LED3.off()

pyb.Pin.board.LED1.on()
buzz(p, 4, 3, 220.0, E)
pyb.Pin.board.LED1.off()

pyb.Pin.board.LED2.on()
buzz(p, 4, 3, 440.0, E+S)
pyb.Pin.board.LED2.off()

sleep(S)

pyb.Pin.board.LED3.on()
buzz(p, 4, 3, 880.0, Q)
pyb.Pin.board.LED3.off()

pyb.Pin.board.LED2.on()
buzz(p, 4, 3, 440.0, H+Q)
pyb.Pin.board.LED2.off()

p.init(0,af=-1)
