from flask import Flask, request
from rpi_utils import PiDoorBellGPIOHelper

DEFAULT_OPEN_DOOR_PUSH_SECONDS = 5

app = Flask(__name__)
gpioHelper = PiDoorBellGPIOHelper()


@app.route("/open_door/release", methods=["POST"])
def open_door_release():
    gpioHelper.release()
    return "Released to open door"


@app.route("/open_door/push", methods=["POST"])
def open_door_push():
    gpioHelper.push()
    return f"Pushing to open door"


@app.route("/")
def root():
    return "Everything is working fine"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
