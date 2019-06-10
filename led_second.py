import time
from neopixel import *
import argparse

# LED strip configuration:
LED_COUNT      = 8      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 128    # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

global strip
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

def set_color(color):
    
    dict_color = {
        'GREEN': (255,0,0),
        'YELLOW': (255,255,0),
        'RED': (0,255,0),
        'None': (0,0,0)
    }

    return dict_color[color]


# Define functions which animate LEDs in various ways.
# def colorWipe_basic(strip, color, wait_time):
#     """Wipe color across display a pixel at a time."""
#     for i in range(strip.numPixels()):
#         strip.setPixelColor(i, color)
#         strip.show()
#         time.sleep(wait_time)
#         strip.setPixelColor(i, Color(0,0,0))
#         strip.show()
#         time.sleep(0.01)

def colorWipe(strip, color, wait_time=0.1):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_time)

def show_light_second():
    colorWipe(strip, Color(0,255,0), 0.1 )  # Red wipe

def turnoff_light_second():
    colorWipe(strip, Color(0,0,0), 0.01 )


# def show_light_second(state, wait_time):
#     color_type = set_color(state)
#     Color_class = Color(color_type[0], color_type[1], color_type[2])
#     colorWipe_basic(strip, Color_class, wait_time)
#     turnoff_light_second()
