"""
command: sudo PYTHONPATH=".:build/lib.linux-armv7l-2.7" python main_2.py

"""
from led_first import show_light_first, show_light_first_inverse
from led_second import show_light_second, turnoff_light_second

import time
import RPi.GPIO as gpio 

# Setup PIN NUMBER =====================

# PWM: GPIO 12, 13, 18, 19
# SPI(MOSI): GPIO 10
TRIG1 = 23   # UW1_TRIG
ECHO1 = 26   # UW1_ECHO original=19
TRIG2 = 12  # UW12_TRIG=18  => pin number
# LED_second => 18(PWM)
ECHO2 = 17  # UW2_ECHOq

SUB_MOT = 19
# ======================================

# Hyper parameter ======================
INTERVAL_DISTANCE = 30  
END_DISTANCE = 5    
MARGIN_ERROR = 0.1  
MID_TERM = 0.1      

FAST = 5           
SLOW = 3           

# ======================================

# GPIO SETUP ===========================
gpio.setmode(gpio.BCM)
gpio.setup(TRIG1, gpio.OUT)
gpio.setup(TRIG2, gpio.OUT)

# gpio.setup(SUB_MOT, gpio.OUT)
# motor = gpio.PWM(SUB_MOT, 50)
# motor.start(0)
# ======================================

# define function ======================
def light_LED(state, wait_time):

    if state == 'RED':
        show_light_first_inverse(wait_time, 'RED')
    elif state == "YELLOW":
        show_light_first_inverse(wait_time, 'YELLOW')
    elif state == "GREEN":
        show_light_first_inverse(wait_time, 'GREEN')
    else:
        # Need to modify
        print ("Input another value.")

def measure_distance(trig, echo):

    gpio.output(trig, False)
    time.sleep(0.01)

    gpio.output(trig, True)
    time.sleep(0.001)
    gpio.output(trig, False)
    
    gpio.setup(echo, gpio.IN)
    while gpio.input(echo) == 0:
        pulse_start = time.time()

    while gpio.input(echo) == 1:
        pulse_end = time.time()
    
    pulse_duration = pulse_end - pulse_start
    return round(pulse_duration * 17000, 4)


def get_measure_avg_dist(trig, echo):
    test_UW = []
    for _ in range(11):
        distance = measure_distance(trig, echo)
        test_UW.append(distance)
    test_UW.sort()
    return test_UW[8]  # return value of 3 Quarter position


def get_interval_time(speed):
    return 0.8 / speed     

def activate_submotor(state):
    gpio.setup(SUB_MOT, gpio.OUT)
    motor = gpio.PWM(SUB_MOT, 50)
    motor.start(0)
    motor.ChangeDutyCycle(state)
    time.sleep(2)
    motor.stop()
    del motor

# ================================================

# Main function ==================================
if __name__ == "__main__":

    time.sleep(3)
    print ("Waiting for ready")
    print ("STEP1: ============ \n <LED TEST>")
    light_LED('GREEN', 0.1)
    light_LED('YELLOW', 0.2)
    light_LED('RED', 0.3)
    print ("STEP2: ============= \n <MOTRO TEST>")
    show_light_second()
    activate_submotor(7.5)
    activate_submotor(12.5)
    turnoff_light_second()
    time.sleep(3)
    show_light_second()
    activate_submotor(7.5)
    activate_submotor(12.5)
    turnoff_light_second()
    print ("STEP2: ============= \n <MEASURE DISTANCE>")
    print("MEASURE_DISTANCE1")
    MEASURE_DISTANCE1 = get_measure_avg_dist(TRIG1, ECHO1)
    print("MEASURE_DISTANCE1 completed\n MEASURE_DISTANCE2")
    MEASURE_DISTANCE2 = get_measure_avg_dist(TRIG2, ECHO2)
    print("MEASURE_DISTANCE2 completed")
    print("result of measure_distance: %f %f \n" % 
                    (MEASURE_DISTANCE1, MEASURE_DISTANCE2) )
    print("Test Completed!!")
    time.sleep(3)
    print ("\nStarting main =======================")
    is_pass = False     
    is_red = False      
    sub_state = 0       # sub_state = Sub mortor status -> 0 : init / 1 : active

    try:
        while True:
            gpio.output(TRIG1, False)
            gpio.output(TRIG2, False)
            time.sleep(0.2)

            if not is_pass: 
                # measure distance in UW1
                distance1 = measure_distance(TRIG1, ECHO1)
                loss = abs(distance1 - MEASURE_DISTANCE1)

                if loss > MEASURE_DISTANCE1 * MARGIN_ERROR:
                    start_time = time.time()
                    is_pass = True
            else:
                # measure distance in UW2
                time.sleep(MID_TERM)

                distance2 = measure_distance(TRIG2, ECHO2)
                loss = abs(distance2 - MEASURE_DISTANCE2)

                if loss > MEASURE_DISTANCE2 * MARGIN_ERROR and not is_red:
                    
                    print ("State: Object goal in")
                    fin_time = time.time()
                    speed = INTERVAL_DISTANCE/(fin_time-start_time)
                    print ("time: %.4f, speed: %.4f" % (fin_time-start_time, speed) )
                    
                    wait_time = get_interval_time(speed)

                    if speed >= FAST:
                        state = 'GREEN'
                    elif SLOW <= speed and speed < FAST:
                        state = 'YELLOW'
                    else:
                        state = 'RED'
                        print("STATUS: RED")
                        show_light_second()
                        activate_submotor(7.5)
                        if sub_state == 0:
                            sub_state = 1
                        light_LED(state, wait_time)
                        is_red = True

                        continue

                    print ("Now, let's show status bia LED")
                    
                    time.sleep( round(END_DISTANCE/speed, 3) )
                    # show_light_second(state, wait_time)
                    light_LED(state, wait_time)
                    is_pass = False
                else:
                    if is_red:
                        while True:
                            time.sleep(0.5)
                            gpio.output(TRIG1, False)
                            gpio.output(TRIG2, False)
                            show_light_second()
                            distance3 = measure_distance(TRIG2, ECHO2)
                            loss = abs(distance3 - MEASURE_DISTANCE2)
                            print("Still RED status")
                            print(loss, MEASURE_DISTANCE2 * MARGIN_ERROR)
                            if not loss > MEASURE_DISTANCE2 * MARGIN_ERROR:
                                break
                        print("RED disappeared")
                        turnoff_light_second()
                        if sub_state == 1:
                            sub_state = 0
                            activate_submotor(12.5)
                        is_red = False
                        is_pass = False
                    else:
                        pass
                        # print("Object didnt' goal in UW2 yet.. continue keep watching only UW2")

                gpio.setup(ECHO2, gpio.OUT)
            gpio.setup(ECHO1, gpio.OUT)
    
    except KeyboardInterrupt:
        gpio.cleanup()
        print ("Program exits.")