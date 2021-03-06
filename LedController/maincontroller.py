# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import time, sys, json, multiprocessing
from neopixel import *
from random import randint

class MainController(object):

	# LED strip configuration:
	LED_COUNT      = 300      # Number of LED pixels.
	LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
	LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
	LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
	LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
	LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

	strip = None
	animationProcess = None

	def __init__(self):
		self.strip = Adafruit_NeoPixel(self.LED_COUNT, self.LED_PIN, self.LED_FREQ_HZ, self.LED_DMA, self.LED_INVERT, self.LED_BRIGHTNESS)
		self.strip.begin()

	def clear(self, args):
		self.colorWipe({"color": {"r": 0, "g": 0, "b": 0}})

	def wait(self, s):
		time.sleep(s)

	def argsToDic(self, args):
		dic = {}
		for arg in args:
			if arg["name"] == "speed":
				dic["speed"] = self.argsToSpeed(arg["value"])
			elif arg["name"] == "color":
				dic["color"] = self.argsToColor(arg["value"])
		return dic

	def argsToColor(self, hcolor):
		h= hcolor.lstrip('#')
		color = Color(int(h[0:2], 16), int(h[4:6], 16), int(h[2:4], 16) )
		return color

	def argsToSpeed(self, arg):
		speed = 800 / float(1000)
		argSpeed = float(arg) 
		if argSpeed == 0:
			speed = 1000
		else:
			speed = speed / argSpeed
		return speed

	# Define functions which animate LEDs in various ways.
	def colorWipeSteps(self, args):	
		wait_s= args["speed"]
		color = args["color"]
		while True:
			"""Wipe color across display a pixel at a time."""
			for i in range(self.strip.numPixels()):
				self.strip.setPixelColor(i, Color(0,0,0))
			for i in range(self.strip.numPixels()):
				self.strip.setPixelColor(i, color)   
				self.strip.show()
				self.time.sleep(wait_s)

	def colorWipe(self, args):
		color = args["color"]
		"""Wipe color across display a pixel at a time."""
		while True:
			for i in range(self.strip.numPixels()):
				self.strip.setPixelColor(i, color)   
			self.strip.show()	

	def theaterChase(self, args):
		wait_s= args["speed"]
		color = args["color"]
		"""Movie theater light style chaser animation."""
		while True:
			for q in range(3):
				for i in range(0, self.strip.numPixels(), 3):
					self.strip.setPixelColor(i+q, color)
				self.strip.show()
				time.sleep(wait_s)
				for i in range(0, self.strip.numPixels(), 3):
					self.strip.setPixelColor(i+q, 0)

	def wheel(self, pos):
		"""Generate rainbow colors across 0-255 positions."""
		if pos < 85:
			return Color(pos * 3, 255 - pos * 3, 0)
		elif pos < 170:
			pos -= 85
			return Color(255 - pos * 3, 0, pos * 3)
		else:
			pos -= 170
			return Color(0, pos * 3, 255 - pos * 3)

	def rainbow(self, args):
		wait_s= args["speed"]
		"""Draw rainbow that fades across all pixels at once."""
		while True:
			for j in range(256):
				for i in range(self.strip.numPixels()):
					self.strip.setPixelColor(i, self.wheel((i+j) & 255))
				self.strip.show()
				time.sleep(wait_s)

	def rainbowCycle(self, args):
		wait_s= args["speed"]
		"""Draw rainbow that uniformly distributes itself across all pixels."""
		while True:
			for j in range(256):
				for i in range(self.strip.numPixels()):
					self.strip.setPixelColor(i, self.wheel((int(i * 256 / self.strip.numPixels()) + j) & 255))
				self.strip.show()
				time.sleep(wait_s)

	def theaterChaseRainbow(self, args):
		wait_s= args["speed"]
		"""Rainbow movie theater light style chaser animation."""
		while True:
			for j in range(256):
				for q in range(3):
					for i in range(0, self.strip.numPixels(), 3):
						self.strip.setPixelColor(i+q, self.wheel((i+j) % 255))
					self.strip.show()
					time.sleep(wait_s)
					for i in range(0, self.strip.numPixels(), 3):
						self.strip.setPixelColor(i+q, 0)

	def moveArray(self, ledArr):
		if sum(ledArr) == 0 or sum(ledArr) == self.LED_COUNT:
			ledArr[0] = 1
			return ledArr
		lastIndex = 0
		for i,val in enumerate(ledArr):
			if val == 1:
				lastIndex = i
		if ledArr[lastIndex - 1] == 1 or lastIndex == 0:
			ledArr[self.LED_COUNT-1]=1
		else:
			ledArr[lastIndex] = 0
			ledArr[lastIndex - 1] = 1
		return ledArr


	def counter(self, args):
		color = args["color"]
		wait_s= args["speed"]
		"""One by one countdown to the bottom."""
		LEDarray = [0] * self.LED_COUNT
		while True:
			for ind,led in enumerate(LEDarray):
				if led == 1:
					self.strip.setPixelColor(ind, color)
				else:
					self.strip.setPixelColor(ind, 0)
			self.strip.show()
			time.sleep(wait_s)
			LEDarray = self.moveArray(LEDarray)

	def moveRandom(self, ledArr):
		if sum(ledArr) > 0.75 * self.LED_COUNT:
			ledArr = [0] * self.LED_COUNT
		ledArr[randint(0, self.LED_COUNT-1)]=1
		return ledArr


	def random(self, args):
		color = args["color"]
		wait_s= args["speed"]
		"""Random."""
		LEDarray = [0] * self.LED_COUNT
		while True:
			for ind,led in enumerate(LEDarray):
				if led == 1:
					self.strip.setPixelColor(ind, color)
				else:
					self.strip.setPixelColor(ind, 0)
			self.strip.show()
			time.sleep(wait_s)
			LEDarray = self.moveRandom(LEDarray)

	def read_in(self):
		try:
			lines = sys.stdin.readlines()
			return json.loads(lines[0])
		except Exception as e:
			print e
			return {}
	
	def changeMode(self, command):
		if not "mode" in command:
			return
		mode = command["mode"]
		
		if "args" in command:
			args = command["args"] 
			args=self.argsToDic(args)
			#print str(args["color"])

		print "Staring mode: " + mode
		if self.animationProcess != None:
			self.animationProcess.terminate()
		targetFunction = None
		if mode == "clear":
			targetFunction = self.clear
		elif mode == "colorWipe":
			targetFunction = self.colorWipe
		elif mode == "theaterChase":
			targetFunction = self.theaterChase
		elif mode == "rainbow":
			targetFunction = self.rainbow
		elif mode =="rainbowCycle":
			targetFunction = self.rainbowCycle
		elif mode == "theaterChaseRainbow":
			targetFunction = self.theaterChaseRainbow
		elif mode == "counter":
			targetFunction = self.counter
		elif mode == "random":
			targetFunction = self.random
		else:
			targetFunction = self.colorWipe

		self.animationProcess = multiprocessing.Process(target=targetFunction, args=(args,))
		self.animationProcess.start()


	def terminate(self):
		self.animationProcess.terminate()

	def run(self):
		p = None
		while True:
			command = self.read_in()
			self.changeMode(command)


if __name__ == '__main__':
	controller = MainController()
	print ('Press Ctrl-C to quit.')
	controller.run()
