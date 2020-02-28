from flask import Flask, request

DEFAULT_OPEN_DOOR_PUSH_SECONDS = 5

app = Flask(__name__)


@app.route("/open_door/release", methods=["POST"])
def open_door_release():
    return "Released to open door"


@app.route("/open_door/push", methods=["POST"])
def open_door_push():
    body = request.get_json()
    if body is not None and "seconds" in body:
        seconds = int(body["seconds"])
    else:
        seconds = DEFAULT_OPEN_DOOR_PUSH_SECONDS

    return f"Pushing to open door during {seconds} seconds"


@app.route("/")
def root():
    return "Everything is working fine"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
