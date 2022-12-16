import time
import logging as log
from enum import Enum
import RPi.GPIO as GPIO


SENSOR_SETTLE_DELAY = 0.1
PULSE_TIME = 0.00001


class OutputUnit(Enum):
    CENTIMETERS = 'cm'
    MILLIMETERS = 'mm'
    INCHES = 'in'
    FOOT = 'ft'


class HCSR04:
    'HC-SR04 sensor reader class for Raspberry'

    def __init__(self, **kwargs):
        self.trigger_pin = None
        self.echo_pin = None
        self.sensor_settle_delay = 2
        self.pulse_time = PULSE_TIME
        self.timeout_seconds = 2
        self.output_unit = OutputUnit.CENTIMETERS.value
        self.__read_start_time = None
        self.__read_end_time = None

        allowed_keys = list(self.__dict__.keys())
        self.__dict__.update((key, value) for key, value in kwargs.items()
                             if key in allowed_keys)

    def read(self):
        'Reads the distance'
        if self.trigger_pin == None or self.echo_pin == None:
            raise RuntimeError('Invalid GPIO pin(s) supplied')

        log.info('Reading HC-SR04 sensor')
        self.__setup_pins()
        self.__wait_for_settle()
        distance_cm = self.__read_distance_cm()

        return {'distance': distance_cm}

    def __wait_for_settle(self):
        log.debug('Waiting for sensor to settle')
        time.sleep(self.sensor_settle_delay)

    def __setup_pins(self):
        log.debug('Setting up pins for sensing distance')
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)
        GPIO.output(self.trigger_pin, GPIO.LOW)

    def __read_distance_cm(self):
        self.__pulse()
        self.__read_start_time = time.monotonic()
        pulse_duration = self.__read_echo_pin_response()
        return self.__pulse_duration_to_distance(pulse_duration)

    def __pulse(self):
        log.info('Pulsing trigger pin #{}'.format(self.trigger_pin))
        GPIO.output(self.trigger_pin, GPIO.HIGH)
        time.sleep(self.pulse_time)
        GPIO.output(self.trigger_pin, GPIO.LOW)

    def __read_echo_pin_response(self):
        log.debug('Waiting for echo pin response')
        while GPIO.input(self.echo_pin) == 0:
            self.__check_elapsed_time()
            pulse_start = time.time()

        while GPIO.input(self.echo_pin) == 1:
            self.__check_elapsed_time()
            pulse_end = time.time()

        return pulse_end - pulse_start

    def __pulse_duration_to_distance(self, pulse_duration):
        # TODO: Remove magic number - @russell.green
        distance = pulse_duration * 17150
        return round(distance, 2)

    def __check_elapsed_time(self):
        elapsed_time = time.monotonic() - self.__read_start_time

        if elapsed_time > self.timeout_seconds:
            raise RuntimeError('Sensor failed to read in specified time')
