# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import time, sys, json, multiprocessing

from neopixel import *


# LED strip configuration:
LED_COUNT      = 300      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)


# Define functions which animate LEDs in various ways.
def colorWipeSteps(strip, color, wait_ms=50):
	"""Wipe color across display a pixel at a time."""
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, color)   
		strip.show()
		time.sleep(wait_ms/1000.0)

def colorWipe(strip, color, wait_ms=50):
	"""Wipe color across display a pixel at a time."""
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, color)   
	strip.show()

def clear(strip):
	colorWipe(strip, Color(0,0,0))

def wait(s):
	time.sleep(s)
	

def theaterChase(strip, color, wait_ms=50, iterations=10):
	"""Movie theater light style chaser animation."""
	for j in range(iterations):
		for q in range(3):
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, color)
			strip.show()
			time.sleep(wait_ms/1000.0)
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, 0)

def wheel(pos):
	"""Generate rainbow colors across 0-255 positions."""
	if pos < 85:
		return Color(pos * 3, 255 - pos * 3, 0)
	elif pos < 170:
		pos -= 85
		return Color(255 - pos * 3, 0, pos * 3)
	else:
		pos -= 170
		return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
	"""Draw rainbow that fades across all pixels at once."""
	for j in range(256*iterations):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel((i+j) & 255))
		strip.show()
		time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
	"""Draw rainbow that uniformly distributes itself across all pixels."""
	print "lol"
	while True:
		for j in range(256*iterations):
			for i in range(strip.numPixels()):
				strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
			strip.show()
			time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
	"""Rainbow movie theater light style chaser animation."""
	for j in range(256):
		for q in range(3):
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, wheel((i+j) % 255))
			strip.show()
			time.sleep(wait_ms/1000.0)
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, 0)

def read_in():
	try:
		lines = sys.stdin.readlines()
		return json.loads(lines[0])
	except Exception as e:
		print e
		return {}

def run(strip):
	p = None
	while True:
		command = read_in()
		if not "mode" in command:
			continue
		mode = command["mode"]
		if p != None:
			p.terminate()
		if mode == "clear":
			p = multiprocessing.Process(target=clear, args=(strip,))
		elif mode == "colorWipe":
			args = command["args"]
			colorWipe(strip, Color(args["color"]["b"], args["color"]["g"], args["color"]["r"]))
		elif mode == "theaterChase":
			theaterChase(strip, Color(  0,   0, 127)) 
		elif mode == "rainbow":
			rainbow(strip)
		elif mode =="rainbowCycle":
			p = multiprocessing.Process(target=rainbowCycle, args=(strip,5,))
		elif mode == "theaterChaseRainbow":
			theaterChaseRainbow(strip)
		else:
			colorWipe(strip, Color(255, 255, 255))

		p.start()


if __name__ == '__main__':
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
	strip.begin()
	print ('Press Ctrl-C to quit.')
	run(strip)
