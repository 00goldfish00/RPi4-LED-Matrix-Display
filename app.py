import time
from flask import Flask,abort, render_template, request, jsonify
from jinja2 import TemplateNotFound
from neohandler import NeoHandler
from audiohandler import AudioHandler
import board
from threading import Thread

app = Flask(__name__)

patterns = {"rainbow", "solid", "blink", "fade", "matrix"}
DEFAULT_COLOR = (0, 0, 0)

@app.route("/send_rgb", methods=["POST"])
def get_color():
    data = request.form
    print(f"Form data: {data}")
    # collect color and pattern data here
    return jsonify({"response":"OK", "data":data})


@app.route("/", methods=["GET"])
def index():
    try:
        return render_template("index.html", patterns=patterns, red=DEFAULT_COLOR[0], green=DEFAULT_COLOR[1], blue=DEFAULT_COLOR[2])
    except TemplateNotFound:
        abort(404)


def run_audio_visualizer():

    led_handler = NeoHandler(pixel_pin=board.D18, num_pixels=40, pixels_per_column=10, brightness=0.1, auto_write=False, pixel_order="GRB")
    audio_handler = AudioHandler('Free Fall.wav', led_handler.num_pixels, led_handler.pixels_per_column)

    for sec in range(int(audio_handler.length_of_song)):
        vol_list = audio_handler.generate_volume_list(sec)
        led_handler.display_volumes(vol_list, wait=0.1)
    
    led_handler.fill((0, 0, 0))
    led_handler.show()


if __name__ == "__main__":

    audio_vis_thread = Thread(target=run_audio_visualizer)
    audio_vis_thread.daemon = True
    audio_vis_thread.start()

    try:
        while True:
            # app.run(debug=True, host="0.0.0.0")
            continue
    except KeyboardInterrupt:
        print(' accepted\nEnding program')
