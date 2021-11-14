from flask import Flask,abort, render_template, request, jsonify
from jinja2 import TemplateNotFound
from neohandler import NeoHandler
from audiohandler import AudioHandler
import board
from threading import Thread
import queue
import numpy as np

# create object of Flask
app = Flask(__name__)

# create global Queue for storing commands provided by the server
user_commands = queue.Queue()

# list of command options to display on the server
patterns = {"Rainbow", "Solid", "RGB Cycle", "Marshmello Alone", "Illenium Free Fall"}

# color to initially set the server sliders to
DEFAULT_COLOR = (0, 0, 0)


# method to collect command data from the server
@app.route("/send_rgb", methods=["POST"])
def get_color():
    # request dropdown and slider form data from server
    data = request.form
    # place form data in command Queue
    user_commands.put(data)
    # print('data:', data)
    return jsonify({"response":"OK", "data":data})


# method to reload page upon GET request
@app.route("/", methods=["GET"])
def index():
    try:
        return render_template("index.html", patterns=patterns, red=DEFAULT_COLOR[0], green=DEFAULT_COLOR[1], blue=DEFAULT_COLOR[2])
    except TemplateNotFound:
        abort(404)


def run_audio_visualizer():

    # create matrix of column heights adjusted for missing LEDs
    broken_matrix = np.array([15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 14, 15, 15, 15, 15, 15, 14])

    # create object of NeoHandler provided with the true LED count and broken matrix array to properly compensate
    led_handler = NeoHandler(pixel_pin=board.D18, num_pixels=298, pixels_per_column=broken_matrix, brightness=0.1, auto_write=False, pixel_order="GRB")

    try:
        while True:

            # check for a command in the Queue
            if user_commands.qsize() > 0:

                # get form data from the command Queue
                cmnd = user_commands.get()

                # if the drop down field contained the Solid option
                if cmnd['pattern'] == 'Solid':
                    # display the solid color selected by the sliders with no wait time
                    led_handler.solid(int(cmnd['red']), int(cmnd['green']), int(cmnd['blue']))

                # if the user selected RGB Cycle
                if cmnd['pattern'] == 'RGB Cycle':
                    # run one loop of the RGB cycle with a 1 second delay for each color
                    led_handler.rgb_cycle(1)
                
                # this is a test method used for testing missing LED compensation
                if cmnd['pattern'] == 'Diagnostic':
                    # vol_list = []
                    # for i in range(led_handler.num_pixels//led_handler.pixels_per_column):
                    #     vol_list.append(led_handler.pixels_per_column)
                    
                    # create an AudioHandler object with a set song
                    ah = AudioHandler(f'songs/{"Ice.wav"}', led_handler.num_pixels, led_handler.columns)
                    
                    # use the colors set by the server sliders
                    color = (int(cmnd['red']), int(cmnd['green']), int(cmnd['blue']))

                    # generate a volume list for a point of the song known to use the broken columns
                    vol_test = ah.generate_volume_list(10)
                    
                    # display the generated list of volumes to test the compensation
                    led_handler.display_volumes(vol_test, color)

                    # plot the fourier transform of the second of the song used for testing
                    ah.plot_fft()
                    #print(f'fourier length: {len(ah.magnitude_list)}\n', max(ah.magnitude_list[:5000]), max(ah.magnitude_list[5000:15000]), max(ah.magnitude_list[15000:]))
                
                # if the user selected Rainbow
                if cmnd['pattern'] == 'Rainbow':
                    # run one loop of the rainbow cycle
                    led_handler.rainbow_cycle(0.01)
                
                # if the user selected the song "Alone" by Marshmello
                if cmnd['pattern'] == 'Marshmello Alone':
                    # create an object of the AuidoHandler class for the song and provided display settings
                    audio_handler = AudioHandler(f'songs/{"Marshmello Alone.wav"}', led_handler.num_pixels, led_handler.columns)

                    # retrieve the set slider colors and generate a random secondary color
                    color = (int(cmnd['red']), int(cmnd['green']), int(cmnd['blue']))
                    second_color = led_handler.rand_color()

                    # for each full second of the song
                    for sec in range(int(audio_handler.length_of_song)):
                        # calculate its fourier transform and genrate a volume list
                        vol_list = audio_handler.generate_volume_list(sec)
                        # display the genrated volume list on the display and hold for 0.5 seconds
                        # this 0.5 delay causes the audio visualizer to run twice as fast as the song selceted
                        led_handler.display_volumes(vol_list, color, second_color, wait=0.5)
                    
                    # once the full song has been looped through clear the display
                    led_handler.fill((0, 0, 0))
                    led_handler.show()
                
                # if the user selected the song "Free Fall" by Illenium
                if cmnd['pattern'] == 'Illenium Free Fall':
                    # create an object of the AuidoHandler class for the song and provided display settings
                    audio_handler = AudioHandler(f'songs/{"Free Fall.wav"}', led_handler.num_pixels, led_handler.columns)

                    # retrieve the set slider colors and generate a random secondary color
                    color = (int(cmnd['red']), int(cmnd['green']), int(cmnd['blue']))
                    second_color = led_handler.rand_color()

                    # for each full second of the song
                    for sec in range(int(audio_handler.length_of_song)):
                        # calculate its fourier transform and genrate a volume list
                        vol_list = audio_handler.generate_volume_list(sec)
                        # display the genrated volume list on the display and hold for 0.5 seconds
                        # this 0.5 delay causes the audio visualizer to run twice as fast as the song selceted
                        led_handler.display_volumes(vol_list, color, second_color, wait=0.5)
                    
                    # once the full song has been looped through clear the display
                    led_handler.fill((0, 0, 0))
                    led_handler.show()
                
    # is the process is interrupted or otherwise ended clear the display
    except KeyboardInterrupt:
        pass
    finally:
        print('Turning off LEDs')
        led_handler.fill((0, 0, 0))
        led_handler.show()


if __name__ == "__main__":

    # create a thread to handle running the LED display and calculating fourier transforms
    audio_vis_thread = Thread(target=run_audio_visualizer)
    audio_vis_thread.daemon = True
    audio_vis_thread.start()

    # begin running the blocking server on the main thread
    app.run(debug=True, host="0.0.0.0")
