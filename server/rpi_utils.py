import io


def is_raspberry_pi(raise_on_errors=False):
    """Checks if Raspberry PI.

    :return: Whether the current machine is a Raspberry PI or not.
    """
    try:
        with io.open("/proc/cpuinfo", "r") as cpuinfo:
            found = False
            for line in cpuinfo:
                if line.startswith("Hardware"):
                    found = True
                    label, value = line.strip().split(":", 1)
                    value = value.strip()
                    if value not in ("BCM2708", "BCM2709", "BCM2835", "BCM2836"):
                        if raise_on_errors:
                            raise ValueError(
                                "This system does not appear to be a Raspberry Pi."
                            )
                        else:
                            return False
            if not found:
                if raise_on_errors:
                    raise ValueError(
                        "Unable to determine if this system is a Raspberry Pi."
                    )
                else:
                    return False
    except IOError:
        if raise_on_errors:
            raise ValueError("Unable to open `/proc/cpuinfo`.")
        else:
            return False

    return True


if not is_raspberry_pi():
    import sys
    import fake_rpi

    sys.modules["RPi"] = fake_rpi.RPi  # Fake RPi
    sys.modules['RPi.GPIO'] = fake_rpi.RPi.GPIO # Fake GPIO
    sys.modules["smbus"] = fake_rpi.smbus  # Fake smbus (I2C)

import RPi.GPIO as gpio

DEFAULT_OPEN_DOOR_PIN = 23


class PiDoorBellGPIOHelper:
    def __init__(self, open_door_pin=DEFAULT_OPEN_DOOR_PIN):
        self.__open_door_pin = open_door_pin
        gpio.setmode(gpio.BCM)
        gpio.setup(self.__open_door_pin, gpio.OUT)
        gpio.output(self.__open_door_pin, gpio.LOW)

    def push(self):
        gpio.output(self.__open_door_pin, gpio.HIGH)

    def release(self):
        gpio.output(self.__open_door_pin, gpio.LOW)
