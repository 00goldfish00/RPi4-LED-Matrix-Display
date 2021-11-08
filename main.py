from neohandler import NeoHandler
from audiohandler import AudioHandler
import board


if __name__ == '__main__':
    led_handler = NeoHandler(pixel_pin=board.D18, num_pixels=300, brightness=0.1, auto_write=False, pixel_order="GRB")
    audio_handler = AudioHandler('Free Fall.wav')

    for sec in range(10):
        vol_list = audio_handler.generate_volume_list(sec)
        led_handler.display_volumes(vol_list, wait=0.25)
    
    led_handler.fill((0, 0, 0))
    led_handler.show()
