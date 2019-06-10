import time
from ws2812 import write2812
from spidev import SpiDev

# WS2812 Setting
spi = SpiDev()
spi.open(0,0)

def set_color(color):

    dict_color = {
        'WHITE': [10,10,10],
        'GREEN': [10,0,0],
        'YELLOW': [10,10,0],
        'RED': [0,10,0],
        'None': [0,0,0]
    }

    return dict_color[color]

def show_light_first(wait_time, color='None'):

    signal_list = [[0,0,0]] * 8

    on_color = set_color(color)
    try:
        for i in range(8):
            signal_list[i] = on_color
            write2812(spi, signal_list)
            time.sleep(wait_time)
            signal_list[i] = set_color('None')
            write2812(spi, signal_list)
    
    except:
        print ("ERROR ouccurs in first led")

def show_light_first_inverse(wait_time, color='None'):
    
    signal_list = [[0,0,0]] * 8

    on_color = set_color(color)
    try:
        for i in range(7,-1,-1):
            signal_list[i] = on_color
            write2812(spi, signal_list)
            time.sleep(wait_time)
            signal_list[i] = set_color('None')
            write2812(spi, signal_list)
    
    except:
        print ("ERROR ouccurs in first led")