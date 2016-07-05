# External module imports
import RPi.GPIO as GPIO
import time


class mygpio():

	INFINITY = 0

	def __init__(self, red, green, blue, buzzer):
		self.red = red
		self.green = green
		self.blue = blue
		self.buzzer = buzzer


		self.LEDS = [self.red, self.green, self.blue]
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BOARD) # Broadcom pin-numbering scheme
		self.ledInit()
		self.buzzerInit()


	def ledInit(self):
		for led in self.LEDS:
			GPIO.setup(led, GPIO.OUT) # LED pin set as output
			GPIO.output(led, GPIO.LOW) 
	 
	def buzzerInit(self):
		GPIO.setup(self.buzzer, GPIO.OUT) # LED pin set as output
		GPIO.output(self.buzzer, GPIO.LOW)  

	def ledAllOff(self):
		for led in self.LEDS:
			GPIO.output(led, GPIO.LOW)

	def ledForTime(self, led, interval):
		self.ledAllOff()
		GPIO.output(led, GPIO.HIGH)
		time.sleep(interval)
		if interval > 0:
			GPIO.output(led, GPIO.LOW)

	def ledBlink(self, led, interval):
		self.ledAllOff()
		while True:
			GPIO.output(led, GPIO.HIGH)
			time.sleep(interval)
			GPIO.output(led, GPIO.LOW)
			time.sleep(interval)

	def ledFail(self, led, interval):
		self.ledAllOff()
		for i in xrange(0, 15):
			GPIO.output(led, GPIO.HIGH)
                        time.sleep(interval)
                        GPIO.output(led, GPIO.LOW)
                        time.sleep(interval)
		
	def buzzerForTime(self, interval):
                GPIO.output(self.buzzer, GPIO.HIGH)
                time.sleep(interval)
		GPIO.output(self.buzzer, GPIO.LOW)
	
	def beepSuccess(self):
		self.buzzerForTime(0.2)

	def beepFail(self):
		for i in xrange(0, 3):
			self.buzzerForTime(0.1)
			time.sleep(0.1)

	def beepStart(self):
		self.buzzerForTime(0.1)
                time.sleep(0.3)
		self.buzzerForTime(0.1)
                time.sleep(0.3)
		self.buzzerForTime(0.5)

	def successSeq(self):
		self.ledAllOff()
		GPIO.output(self.blue, GPIO.HIGH)
		self.beepSuccess()
                time.sleep(0.5)
		GPIO.output(self.blue, GPIO.LOW)
		GPIO.output(self.green, GPIO.HIGH)
	
	def failSeq(self):
		self.ledAllOff()
		GPIO.output(self.red, GPIO.HIGH)
		self.beepFail()
                time.sleep(0.5)
		GPIO.output(self.red, GPIO.LOW)
		GPIO.output(self.green, GPIO.HIGH)
	
	def clean(self):
		GPIO.cleanup() # cleanup all GPIO

	def startSeq(self):
		self.ledAllOff()
	        self.ledForTime(self.red, 0.5)
                self.ledForTime(self.green, 0.5)
                self.ledForTime(self.blue, 0.5)

		self.beepStart()

	def test(self):
		self.ledAllOff()
		self.ledForTime(self.red, 2)
		self.ledForTime(self.green, 2)
		self.ledForTime(self.blue, 2)

		self.beepSuccess()
		time.sleep(2)
		self.beepFail()


