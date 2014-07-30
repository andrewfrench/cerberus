import RPi.GPIO as GPIO
import time

GPIO.setup(18, GPIO.OUT)

while(1):
	print("Voltage HIGH")
	GPIO.output(18, True)
	time.sleep(5)
	print("Voltage LOW")
	GPIO.output(18, False)
	time.sleep(5)