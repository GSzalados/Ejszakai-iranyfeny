import time
import board
import busio
import adafruit_tsl2591
import pigpio

RED_PIN   = 17
GREEN_PIN = 22
BLUE_PIN  = 24

bright = 255
r = 0.0
g = 255.0
b = 0.0

pi = pigpio.pi()

def setLights(pin, brightness):
	realBrightness = int(int(brightness) * (float(bright) / 255.0))
	pi.set_PWM_dutycycle(pin, realBrightness)

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_tsl2591.TSL2591(i2c)

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
PIR_PIN = 7
LED_PIN = 11
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.add_event_detect(PIR_PIN, GPIO.RISING)
			
while True:
	lux = sensor.lux
	print(lux)
	time.sleep(1.0)
	if lux < 1:
		print('Sotet van')
		if GPIO.event_detected(PIR_PIN):
			print('Felkapcsolom a LED-et')
			setLights(RED_PIN, r)
			setLights(GREEN_PIN, g)
			setLights(BLUE_PIN, b)
			time.sleep(10.5)

			setLights(RED_PIN, 0)
			setLights(GREEN_PIN, 0)
			setLights(BLUE_PIN, 0)
		else:
			print('Nincs mozgas')
