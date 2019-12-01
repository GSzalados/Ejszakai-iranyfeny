import time 	#time könyvtár importálása
import board	#board könyvtár importálása
import busio	#busio könyvtár importálása
import adafruit_tsl2591	#fényérzékelőhöz szükséges parancsok könyvtára
import pigpio	#LED-hez szükséges könyvtár

import RPi.GPIO as GPIO	#importálja és beállítja a GPIO kapcsolatot
GPIO.setmode(GPIO.BCM)

from datetime import datetime
dateTimeObj = datetime.now()
#teszt = 4 a színkeverés tesztelésére

PIR_PIN = 7	#mozgásérzékelő definiálása
GPIO.setup(PIR_PIN, GPIO.IN)	
GPIO.add_event_detect(PIR_PIN, GPIO.RISING)

i2c = busio.I2C(board.SCL, board.SDA) #inicializálja a fényérzékelőt és definiálja az i2c kapcsolatot
sensor = adafruit_tsl2591.TSL2591(i2c)

RED_PIN   = 17	#LED pin-ek definiálása
GREEN_PIN = 22
BLUE_PIN  = 24

tel = [12,1,2]
tavasz = [3,4,5]
nyar = [6,7,8]
osz = [9,10,11]

if dateTimeObj.month in tel:
	bright = 255 #RGB színkeverés kék
	r = 0.0
	g = 0.0
	b = 255.0
elif dateTimeObj.month in tavasz:
	bright = 255 #RGB színkeverés zöld
	r = 0.0
	g = 128.0
	b = 0.0
elif dateTimeObj.month in nyar:
	bright = 255 #RGB színkeverés citromsárga
	r = 255.0
	g = 0.0
	b = 0.0	
elif dateTimeObj.month in osz:
	bright = 255 #RGB színkeverés narancssárga
	r = 255.0
	g = 165.0
	b = 0.0	
else:
	nothing

pi = pigpio.pi()

def setLights(pin, brightness):
	realBrightness = int(int(brightness) * (float(bright) / 255.0))
	pi.set_PWM_dutycycle(pin, realBrightness)
	
while True:
	lux = sensor.lux
	print(lux)
	time.sleep(1.0)
	if lux < 2:
		print('Sotet van')
		if GPIO.event_detected(PIR_PIN):
			setLights(RED_PIN, r)
			setLights(GREEN_PIN, g)
			setLights(BLUE_PIN, b)
				
			try:
				time.sleep(10.5)
				setLights(RED_PIN, 0)
				setLights(GREEN_PIN, 0)
				setLights(BLUE_PIN, 0)
				
			except KeyboardInterrupt:
				setLights(RED_PIN, 0)
				setLights(GREEN_PIN, 0)
				setLights(BLUE_PIN, 0)
		else:
			print('Nincs mozgas')
