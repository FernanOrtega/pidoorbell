import io, atexit
from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler


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
    sys.modules["RPi.GPIO"] = fake_rpi.RPi.GPIO  # Fake GPIO
    sys.modules["smbus"] = fake_rpi.smbus  # Fake smbus (I2C)

import RPi.GPIO as gpio

DEFAULT_OPEN_DOOR_PIN = 23
DEFAULT_RELEASE_SECONDS = 5
RELEASE_JOB_ID = "release_job"


class PiDoorBellGPIOHelper:
    def __init__(self, open_door_pin=DEFAULT_OPEN_DOOR_PIN):
        self.__open_door_pin = open_door_pin
        self.__scheduler = BackgroundScheduler()
        gpio.setmode(gpio.BCM)
        gpio.setup(self.__open_door_pin, gpio.OUT)
        gpio.output(self.__open_door_pin, gpio.LOW)

        self.__scheduler.start()
        atexit.register(lambda: self.clean_app())

    # Shut down the scheduler when exiting the app
    def clean_app(self):
        self.__scheduler.shutdown()
        gpio.cleanup()

    def push(self):
        gpio.output(self.__open_door_pin, gpio.HIGH)
        self.__delayed_release()

    def release(self):
        gpio.output(self.__open_door_pin, gpio.LOW)
        if self.__scheduler.get_job(job_id=RELEASE_JOB_ID) is not None:
            self.__scheduler.remove_job(job_id=RELEASE_JOB_ID)

    def __delayed_release(self):
        print("Added new job to release")
        self.__scheduler.add_job(
            id=RELEASE_JOB_ID,
            max_instances=1,
            func=self.release,
            trigger="date",
            run_date=datetime.now() + timedelta(seconds=DEFAULT_RELEASE_SECONDS),
            replace_existing=True,
        )
