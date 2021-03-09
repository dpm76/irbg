#!/usr/bin/python
from utime import sleep_us, sleep
from machine import Pin
from micropython import const

# Zuordnung der GPIO Pins (ggf. anpassen)
HIGH = const(1)
LOW  = const(0)

LCD_RS = Pin(Pin.board.D2, Pin.OUT)
LCD_E  = Pin(Pin.board.D3, Pin.OUT)
LCD_DATA4 = Pin(Pin.board.D4, Pin.OUT)
LCD_DATA5 = Pin(Pin.board.D5, Pin.OUT)
LCD_DATA6 = Pin(Pin.board.D6, Pin.OUT)
LCD_DATA7 = Pin(Pin.board.D7, Pin.OUT)

LCD_WIDTH = 16 		# Zeichen je Zeile
LCD_LINE_1 = 0x80 	# Adresse der ersten Display Zeile
LCD_LINE_2 = 0xC0 	# Adresse der zweiten Display Zeile
LCD_CHR = HIGH
LCD_CMD = LOW
E_PULSE = const(500) # us
E_DELAY = const(500) # us

def lcd_send_byte(bits, mode):
	# Pins auf LOW setzen
	LCD_RS.value(mode)
	LCD_DATA4.value(LOW)
	LCD_DATA5.value(LOW)
	LCD_DATA6.value(LOW)
	LCD_DATA7.value(LOW)
	if bits & 0x10 == 0x10:
	  LCD_DATA4.value(HIGH)
	if bits & 0x20 == 0x20:
	  LCD_DATA5.value(HIGH)
	if bits & 0x40 == 0x40:
	  LCD_DATA6.value(HIGH)
	if bits & 0x80 == 0x80:
	  LCD_DATA7.value(HIGH)
	sleep_us(E_DELAY)    
	LCD_E.value(HIGH)  
	sleep_us(E_PULSE)
	LCD_E.value(LOW)  
	sleep_us(E_DELAY)      
	LCD_DATA4.value(LOW)
	LCD_DATA5.value(LOW)
	LCD_DATA6.value(LOW)
	LCD_DATA7.value(LOW)
	if bits&0x01==0x01:
	  LCD_DATA4.value(HIGH)
	if bits&0x02==0x02:
	  LCD_DATA5.value(HIGH)
	if bits&0x04==0x04:
	  LCD_DATA6.value(HIGH)
	if bits&0x08==0x08:
	  LCD_DATA7.value(HIGH)
	sleep_us(E_DELAY)    
	LCD_E.value(HIGH)  
	sleep_us(E_PULSE)
	LCD_E.value(LOW)  
	sleep_us(E_DELAY)  

def display_init():
	lcd_send_byte(0x33, LCD_CMD)
	lcd_send_byte(0x32, LCD_CMD)
	lcd_send_byte(0x28, LCD_CMD)
	lcd_send_byte(0x0C, LCD_CMD)  
	lcd_send_byte(0x06, LCD_CMD)
	lcd_send_byte(0x01, LCD_CMD)  

def lcd_message(message):
	for i in range(LCD_WIDTH):
	  if i < len(message):
	    lcd_send_byte(ord(message[i]),LCD_CHR)
	  else:
	    lcd_send_byte(ord(" "), LCD_CHR)
	
if __name__ == '__main__':
	
	display_init()

	
	lcd_send_byte(LCD_LINE_1, LCD_CMD)
	lcd_message("Es scheint zu")
	lcd_send_byte(LCD_LINE_2, LCD_CMD)
	lcd_message("funktionieren :)")
	
	sleep(4)
	
	msg1 = "Dies ist ein"
	msg2 = "kleiner Test"
	for i in range(len(msg1)):
		lcd_send_byte(LCD_LINE_1, LCD_CMD)
		lcd_message(msg1[:i+1])
		lcd_send_byte(LCD_LINE_2, LCD_CMD)
		lcd_message("")
		sleep(0.1)	
	for i in range(len(msg2)):
		lcd_send_byte(LCD_LINE_1, LCD_CMD)
		lcd_message(msg1)
		lcd_send_byte(LCD_LINE_2, LCD_CMD)
		lcd_message(msg2[:i+1])
		sleep(0.1)
	
	sleep(4)
	
