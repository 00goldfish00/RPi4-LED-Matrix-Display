from flask import Flask,abort, render_template, request, jsonify
from jinja2 import TemplateNotFound
from neohandler import NeoHandler
from audiohandler import AudioHandler
import board
from threading import Thread
import queue
import numpy as np

app = Flask(__name__)

user_commands = queue.Queue()

patterns = {"Rainbow", "Solid", "RGB Cycle", "Marshmello Alone", "Illenium Free Fall"}
DEFAULT_COLOR = (0, 0, 0)


@app.route("/send_rgb", methods=["POST"])
def get_color():
    data = request.form
    user_commands.put(data)
    # print('data:', data)
    return jsonify({"response":"OK", "data":data})


@app.route("/", methods=["GET"])
def index():
    try:
        return render_template("index.html", patterns=patterns, red=DEFAULT_COLOR[0], green=DEFAULT_COLOR[1], blue=DEFAULT_COLOR[2])
    except TemplateNotFound:
        abort(404)


def run_audio_visualizer():
    broken_matrix = np.array([15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 14, 15, 15, 15, 15, 15, 14])
    led_handler = NeoHandler(pixel_pin=board.D18, num_pixels=298, pixels_per_column=broken_matrix, brightness=0.1, auto_write=False, pixel_order="GRB")
    try:
        while True:
            if user_commands.qsize() > 0:
                cmnd = user_commands.get()

                if cmnd['pattern'] == 'Solid':
                    led_handler.solid(int(cmnd['red']), int(cmnd['green']), int(cmnd['blue']))

                if cmnd['pattern'] == 'RGB Cycle':
                    led_handler.rgb_cycle(1)
                
                if cmnd['pattern'] == 'Diagnostic':
                    # vol_list = []
                    # for i in range(led_handler.num_pixels//led_handler.pixels_per_column):
                    #     vol_list.append(led_handler.pixels_per_column)
                    
                    ah = AudioHandler(f'songs/{"Ice.wav"}', led_handler.num_pixels, led_handler.columns)
                    
                    color = (int(cmnd['red']), int(cmnd['green']), int(cmnd['blue']))

                    vol_test = ah.generate_volume_list(10)
                    
                    led_handler.display_volumes(vol_test, color)

                    ah.plot_fft()
                    #print(f'fourier length: {len(ah.magnitude_list)}\n', max(ah.magnitude_list[:5000]), max(ah.magnitude_list[5000:15000]), max(ah.magnitude_list[15000:]))
                
                if cmnd['pattern'] == 'Rainbow':
                    led_handler.rainbow_cycle(0.01)
                
                if cmnd['pattern'] == 'Marshmello Alone':
                    audio_handler = AudioHandler(f'songs/{"Marshmello Alone.wav"}', led_handler.num_pixels, led_handler.columns)

                    color = (int(cmnd['red']), int(cmnd['green']), int(cmnd['blue']))
                    second_color = led_handler.rand_color()

                    for sec in range(int(audio_handler.length_of_song)):
                        vol_list = audio_handler.generate_volume_list(sec)
                        led_handler.display_volumes(vol_list, color, second_color, wait=0.5)
                    
                    led_handler.fill((0, 0, 0))
                    led_handler.show()
                
                if cmnd['pattern'] == 'Illenium Free Fall':
                    audio_handler = AudioHandler(f'songs/{"Free Fall.wav"}', led_handler.num_pixels, led_handler.columns)

                    color = (int(cmnd['red']), int(cmnd['green']), int(cmnd['blue']))
                    second_color = led_handler.rand_color()

                    for sec in range(int(audio_handler.length_of_song)):
                        vol_list = audio_handler.generate_volume_list(sec)
                        led_handler.display_volumes(vol_list, color, second_color, wait=0.5)
                    
                    led_handler.fill((0, 0, 0))
                    led_handler.show()
                
    except KeyboardInterrupt:
        pass
    finally:
        print('Turning off LEDs')
        led_handler.fill((0, 0, 0))
        led_handler.show()


if __name__ == "__main__":

    audio_vis_thread = Thread(target=run_audio_visualizer)
    audio_vis_thread.daemon = True
    audio_vis_thread.start()

    app.run(debug=True, host="0.0.0.0")
