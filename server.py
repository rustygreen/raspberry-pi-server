import sys
import logging as log
import RPi.GPIO as GPIO
from flask import Flask, jsonify

host = '0.0.0.0'
port = 8080
debug = False
gpio_pins = (7, 11, 13, 15, 16, 18, 22, 29, 31, 32, 33, 36, 37)
app = Flask(__name__)
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

    log.info("Retieved values for all pins")
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
    log.info("Retieved value for pin '{}' (value: {})".format(
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
        GPIO.output(pin, GPIO.LOW)


if __name__ == '__main__':
    log.info('Starting app at {}:{} (debug:{})'.format(host, port, debug))
    try:
        setup_gpio()
        app.run(debug=debug, host=host, port=port)
    finally:
        log.debug('App is shutting down, cleaning up GPIO')
        GPIO.cleanup()
        log.info('GPIO has been cleaned up')
