"""Raspberry Pi Server

`raspberry-pi-server` is a server component designed to be ran on a Raspberry Pi
which provides RESTful services to control the GPIO pins of the Raspberry Pi.
This project was created in an effort to eliminate the need to create custom
python scripts and constantly maintain, update, and schedule them on a Raspberry Pi.
Rather, you can deploy one single service on the Pi (raspberry-pi-server), and
never have to logon to the Pi again. Interaction to the Pi can be done through
RESTful services using whatever client/technology you'd like. For example, check
out the [raspberry-pi-client project](https://github.com/rustygreen/raspberry-pi-client)
"""
__author__ = "Russell Green"
__license__ = "MIT"
__version__ = "1.0.2"
__maintainer__ = "Russell.Green"
__email__ = "me@rusty.green"
__status__ = "Production"

import sys
import os
import datetime
from enum import Enum
import logging as log
import RPi.GPIO as GPIO
from flask import Flask, jsonify, request
from flask_cors import CORS
from sensors.dht11 import DHT11
from sensors.hcsr04 import HCSR04


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


host = os.getenv("SERVER_HOST") or "0.0.0.0"
port = os.getenv("SERVER_PORT") or 5000
log_level = os.getenv("SERVER_LOG_LEVEL") or log.WARN
debug = False
gpio_pins = (7, 11, 12, 13, 15, 16, 18, 22, 29, 31, 32, 33, 35, 36, 37, 38, 40)
gpio_pin_history = {}
initial_pin_state = InitialPinBehavior.DEFAULT
app = Flask(__name__)
CORS(app)
app.url_map.strict_slashes = False
start_time = datetime.datetime.now()


log.basicConfig(
    level=log_level,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[log.StreamHandler(sys.stdout)],
)


@app.route("/healthz")
def health_check():
    """Health check

    Returns a value to ensure the service is up.
    """
    return "healthy"


@app.route("/version")
def version():
    """Version

    Returns the module version.
    """
    return __version__


@app.route("/info")
def info():
    """Info

    Returns the deployment info.
    """
    info = {
        "version": __version__,
        "host": host,
        "port": port,
        "logLevel": log_level,
        "isDebug": debug,
        "startTime": start_time,
    }

    return jsonify(info)


@app.route("/pins")
def get_all_pins():
    """Get pins

    Retries a list of all GPIO pins and their current values.
    """
    result = []
    for pin in gpio_pins:
        pin_result = {"pin": pin, "value": get_pin_value(pin)}
        history = get_pin_history(pin)
        pin_result.update(history)
        result.append(pin_result)

    log.info("Retrieved values for all pins")
    return jsonify(result)


@app.route("/pins/all/<int:value>")
def set_all_pins(value):
    """Set pins to value

    Set all GPIO pins to a specified value.
    """
    result = []
    for pin in gpio_pins:
        new_value = set_get_pin_value(pin, value)
        changed = value != new_value
        pin_result = {"pin": pin, "value": get_pin_value(pin), "changed": changed}

        history = get_pin_history(pin)
        pin_result.update(history)
        result.append(pin_result)

    log.info("Set value of all pins to {}".format(value))
    return jsonify(result)


@app.route("/pins/<int:pin>")
def get_pin(pin):
    """Get pin value

    Gets the current value for a given GPIO pin.
    """
    pin_value = get_pin_value(pin)
    log.info(
        "Retrieved value for pin '{}' (value: {})".format(str(pin), str(pin_value))
    )

    return str(pin_value)


@app.route("/pins/<int:pin>/<int:value>")
def set_pin(pin, value):
    """Set pin value

    Sets a GPIO pin to a specified value.
    """
    pin_value = set_get_pin_value(pin, value)

    if value != pin_value:
        msg = "Failed to set pin '{}'. Expected {} to be {}".format(
            pin, pin_value, value
        )
        log.exception(msg)
        raise Exception(msg)

    log.info("Set value for pin '{}' (value: {})".format(pin, pin_value))
    return str(pin_value)


@app.route("/sensors/dht11/<int:pin>")
def get_sensor_dht11(pin):
    """Get DHT11 sensor reading

    Gets a reading for a DHT11 sensor.
    """
    sensor = DHT11(pin=pin)
    log.info("Reading DHT11 sensor for pin '{}'".format(pin))
    result = sensor.read_with_retry()
    log.info("Retrieved DHT11 sensor reading for pin '{}'".format(pin))
    return jsonify(result.to_dict())


@app.route("/sensors/hcsr04/<int:trigger_pin>/<int:echo_pin>")
def get_sensor_hcsr04(trigger_pin, echo_pin):
    """Get HC-SR04 sensor reading
    Gets a reading for a HC-SR04 ultrasonic sonar distance sensor.
    See: https://adafru.it/3942
    """
    log.info(
        "Reading HC-SR04 sensor for pin 'trigger: {}, echo: {}'".format(
            trigger_pin, echo_pin
        )
    )
    args = {"trigger_pin": trigger_pin, "echo_pin": echo_pin}
    args.update(request.args)

    sensor = HCSR04(**args)
    result = sensor.read()
    log.info(
        "Retrieved HC-SR04 sensor reading for pin 'trigger: {}, echo: {}'".format(
            trigger_pin, echo_pin
        )
    )
    return jsonify(result)


def temperature_of_raspberry_pi():
    """Get Pi temperature

    Gets the temperature of the Raspberry Pi.
    """
    cpu_temp = os.popen("vcgencmd measure_temp").readline()
    return cpu_temp.replace("temp=", "")


def get_pin_value(pin):
    """Gets a pin value by GPIO pin number

    Gets the value of a GPIO pin.
    """
    return GPIO.input(pin)


def set_pin_value(pin, value):
    """Sets pin value

    Sets a GPIO pin value.
    """
    GPIO.output(pin, value)
    set_pin_history(pin)


def set_get_pin_value(pin, value):
    """Sets pin value and then returns the value

    Sets and gets a GPIO pin value.
    """
    set_pin_value(pin, value)
    return get_pin_value(pin)


def get_pin_history(pin):
    if pin in gpio_pin_history:
        return gpio_pin_history[pin]
    else:
        return {"lastValue": None}


def set_pin_history(pin):
    history = {"lastChange": datetime.datetime.now()}
    record = get_pin_history(pin)
    record.update(history)


def setup_gpio():
    """Sets up the GPIO pins

    Sets up the Raspberry Pi and GPIO pins for initial use.
    """
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)

    for pin in gpio_pins:
        GPIO.setup(pin, GPIO.OUT)
        set_initial_state(pin)


def set_initial_state(pin):
    """Sets the initial state for a given pin

    Sets up a pin's initial state based on the configured behavior.
    """
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


if __name__ == "__main__":
    log.info(
        "Starting app at {}:{} (debug:{}). Version {}".format(
            host, port, debug, __version__
        )
    )
    try:
        setup_gpio()
        app.run(debug=debug, host=host, port=port)
    except Exception as e:
        log.error("Fatal application error occurred: {}".format(e))
    finally:
        log.debug("App is shutting down, cleaning up GPIO")
        GPIO.cleanup()
        log.info("GPIO has been cleaned up")
