import sys
from enum import Enum
import logging as log
import RPi.GPIO as GPIO
from flask import Flask, jsonify
from flask_cors import CORS
from sensors.dht11 import DHT11


class InitialPinBehavior(Enum):
    # Sets the initial pin state to LOW (0).
    LOW = 0
    # Sets the initial pin state to HIGH (1).
    HIGH = 1
    # Sets the pin state to the default state of the Raspberry Pi (as
    # if the it was restarted and untouched). Pins 1-8 are defaulted
    # to HIGH (1) while 9 and above default to LOW (0).
    # See: https://roboticsbackend.com/raspberry-pi-gpios-default-state/
    DEFAULT = 2
    # Do not change the pin states - leaving them exactly how they are.
    UNMODIFIED = 3


host = '0.0.0.0'
port = 8080
debug = False
gpio_pins = (7, 11, 12, 13, 15, 16, 18, 22, 29, 31, 32, 33, 36, 37)
initial_pin_state = InitialPinBehavior.DEFAULT
app = Flask(__name__)
CORS(app)
app.url_map.strict_slashes = False

log.basicConfig(
    level=log.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        log.StreamHandler(sys.stdout)
    ]
)


@app.route('/pins')
def get_all_pins():
    result = []
    for pin in gpio_pins:
        pin_result = {'pin': pin, 'value': get_pin_value(pin)}
        result.append(pin_result)

    log.info("Retrieved values for all pins")
    return jsonify(result)


@app.route('/pins/all/<int:value>')
def set_all_pins(value):
    result = []
    for pin in gpio_pins:
        new_value = set_get_pin_value(pin, value)
        changed = value != new_value
        pin_result = {'pin': pin, 'value': get_pin_value(
            pin), 'changed': changed}
        result.append(pin_result)

    log.info("Set value of all pins to {}".format(value))
    return jsonify(result)


@app.route('/pins/<int:pin>')
def get_pin(pin):
    pin_value = get_pin_value(pin)
    log.info("Retrieved value for pin '{}' (value: {})".format(
        str(pin), str(pin_value)))
    return str(pin_value)


@app.route('/pins/<int:pin>/<int:value>')
def set_pin(pin, value):
    pin_value = set_get_pin_value(pin, value)

    if (value != pin_value):
        msg = "Failed to set pin '{}'. Expected {} to be {}".format(
            pin, pin_value, value)
        log.exception(msg)
        raise Exception(msg)

    log.info("Set value for pin '{}' (value: {})".format(pin, pin_value))
    return str(pin_value)


@app.route('/sensors/dht11/<int:pin>')
def get_sensor_dht11(pin):
    instance = DHT11(pin=pin)
    result = instance.read_with_retry()
    log.info("Retrieved DHT11 sensor reading for pin '{}'".format(pin))
    return jsonify(result.to_dict())


def get_pin_value(pin):
    return GPIO.input(pin)


def set_pin_value(pin, value):
    GPIO.output(pin, value)


def set_get_pin_value(pin, value):
    set_pin_value(pin, value)
    return get_pin_value(pin)


def setup_gpio():
    GPIO.setmode(GPIO.BOARD)

    for pin in gpio_pins:
        GPIO.setup(pin, GPIO.OUT)
        set_initial_state(pin)


def set_initial_state(pin):
    if initial_pin_state == InitialPinBehavior.UNMODIFIED:
        return
    if initial_pin_state == InitialPinBehavior.LOW:
        state = GPIO.LOW
    elif initial_pin_state == InitialPinBehavior.HIGH:
        state = GPIO.HIGH
    elif initial_pin_state == InitialPinBehavior.DEFAULT:
        state = GPIO.HIGH if pin < 9 else GPIO.LOW

    log.debug("Setting pin '{}' to state '{}'".format(pin, state))
    GPIO.output(pin, state)


if __name__ == '__main__':
    log.info('Starting app at {}:{} (debug:{})'.format(host, port, debug))
    try:
        setup_gpio()
        app.run(debug=debug, host=host, port=port)
    except Exception as e:
        log.error('Fatal application error occurred: {}'.format(e))
    finally:
        log.debug('App is shutting down, cleaning up GPIO')
        GPIO.cleanup()
        log.info('GPIO has been cleaned up')
