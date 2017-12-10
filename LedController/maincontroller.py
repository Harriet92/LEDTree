# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import time, sys, json, multiprocessing

from neopixel import *

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

	def argsToColor(self, args):
		color = Color(255, 255, 255)
		if "color" in args and "r" in args["color"] and "g" in args["color"] and "b" in args["color"]:
			color = Color(args["color"]["b"], args["color"]["g"], args["color"]["r"])
		return color

	# Define functions which animate LEDs in various ways.
	def colorWipeSteps(self, args):	
		wait_ms=50
		color = self.argsToColor(args) 
		while True:
			"""Wipe color across display a pixel at a time."""
			for i in range(self.strip.numPixels()):
				self.strip.setPixelColor(i, color)   
				self.strip.show()
				self.time.sleep(wait_ms/1000.0)

	def colorWipe(self, args):
		wait_ms=50
		color = self.argsToColor(args) 
		"""Wipe color across display a pixel at a time."""
		while True:
			for i in range(self.strip.numPixels()):
				self.strip.setPixelColor(i, color)   
			self.strip.show()	

	def theaterChase(self, args):
		wait_ms=50
		iterations=10
		color = Color(  0,   0, 127) #self.argsToColor(args) 
		"""Movie theater light style chaser animation."""
		while True:
			for j in range(iterations):
				for q in range(3):
					for i in range(0, self.strip.numPixels(), 3):
						self.strip.setPixelColor(i+q, color)
					self.strip.show()
					time.sleep(wait_ms/1000.0)
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
		wait_ms=20
		iterations=1
		"""Draw rainbow that fades across all pixels at once."""
		while True:
			for j in range(256*iterations):
				for i in range(self.strip.numPixels()):
					self.strip.setPixelColor(i, self.wheel((i+j) & 255))
				self.strip.show()
				time.sleep(wait_ms/1000.0)

	def rainbowCycle(self, args):
		wait_ms = 1 
		"""Draw rainbow that uniformly distributes itself across all pixels."""
		while True:
			for j in range(256):
				for i in range(self.strip.numPixels()):
					self.strip.setPixelColor(i, self.wheel((int(i * 256 / self.strip.numPixels()) + j) & 255))
				self.strip.show()
				time.sleep(wait_ms/1000.0)

	def theaterChaseRainbow(self):
		wait_ms=50
		"""Rainbow movie theater light style chaser animation."""
		while True:
			for j in range(256):
				for q in range(3):
					for i in range(0, self.strip.numPixels(), 3):
						self.strip.setPixelColor(i+q, self.wheel((i+j) % 255))
					self.strip.show()
					time.sleep(wait_ms/1000.0)
					for i in range(0, self.strip.numPixels(), 3):
						self.strip.setPixelColor(i+q, 0)

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
		args = command["args"] if "args" in command else {}
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
		else:
			targetFunction = self.colorWipe

		self.animationProcess = multiprocessing.Process(target=targetFunction, args=(args,))
		self.animationProcess.start()

	def run(self):
		p = None
		while True:
			command = self.read_in()
			self.changeMode(command)


if __name__ == '__main__':
	controller = MainController()
	print ('Press Ctrl-C to quit.')
	controller.run()
