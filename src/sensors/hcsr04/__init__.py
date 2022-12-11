import RPi.GPIO as GPIO
import time


SENSOR_SETTLE_DELAY=0.5
PULSE_TIME = 0.00001


class HCSR04:
    'HC-SR04 sensor reader class for Raspberry'

    __trigger_pin = 0
    __echo_pin = 0
    __sensor_settle_delay = 2
    __pulse_time = PULSE_TIME

    def __init__(self, trigger_pin, echo_pin, sensor_settle_delay=SENSOR_SETTLE_DELAY, pulse_time=PULSE_TIME):
        self.__trigger_pin = trigger_pin
        self.__echo_pin = echo_pin
        self.__sensor_settle_delay = sensor_settle_delay
        self.__pulse_time = pulse_time

    def read(self):
        'Reads the distance'
        self.__setup_for_distance_measurement()
        time.sleep(self.__sensor_settle_delay)
        distance_cm = self.__read_distance_cm()

        return { 'distance': distance_cm }

    def __setup_for_distance_measurement(self):
        GPIO.setup(self.__trigger_pin, GPIO.OUT)
        GPIO.setup(self.__echo_pin, GPIO.IN)

    def __read_distance_cm(self):
        self.__pulse()
        pulse_duration = self.__read_pulse_duration()
        return self.__pulse_duration_to_distance(pulse_duration)

    def __pulse(self):
        GPIO.output(self.__trigger_pin, True)
        time.sleep(self.__pulse_time)
        GPIO.output(self.__trigger_pin, False)

    def __read_pulse_duration(self):
        while GPIO.input(self.__echo_pin) == 0:
            pulse_start = time.time()

        while GPIO.input(self.__echo_pin) == 1:
            pulse_end = time.time()

        return pulse_end - pulse_start

    def __pulse_duration_to_distance(self, pulse_duration):
        # TODO: Remove magic number - @russell.green
        distance = pulse_duration * 17150
        return round(distance, 2)
