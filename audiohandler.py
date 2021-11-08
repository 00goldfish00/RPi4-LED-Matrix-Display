from scipy.io import wavfile
from scipy.fftpack import fft, fftfreq
import numpy as np
import matplotlib.pyplot as plt
import math
from neohandler import NeoHandler
import board



# data sample step
second_to_transform = 100

# 
start_point = second_to_transform
print('start point:', start_point, type(start_point))

# time length of collected data
stop_point = second_to_transform+1
print('stop point:', stop_point, type(stop_point))

# x-axis is frequency
x = np.linspace(start_point, stop_point, N, endpoint=False)
# fft of frequency range
xf = fftfreq(N, T)[:N//22]

# y-axis input sinewaves
y = song_data[start_point*N:stop_point*N]
# fft of input signal
yf = fft(y)
#y-axis of the fourier tranform graph 
magnitude = 2.0/N * np.abs(yf[0:N//22])

class AudioHandler:
    ''''''

    def __init__(self, song_title) -> None:
        # read in song waveform data
        samplerate, data = wavfile.read(song_title, mmap=False)

        # convert to numpy array
        song_data = np.array(data[:])
        print('number of data points in song:', len(song_data))

        # length of song in seconds
        length_of_song = np.size(song_data) / samplerate
        print('length of song in seconds:', length_of_song)

        # Number of data points to sample for transform
        N = samplerate
        
        # spacing between data points (song sample rate in denominator)
        T = 1.0 / samplerate
    

    # plot
    def plot_fft(self, xf, yf, xt = [], yt = [], name = 'Fourier Plot'):
        if xt.any() == True and yt.any() == True:
            plt.subplot(2, 1, 1)
            plt.plot(xt, yt)
            plt.title('sine input over time')

            plt.subplot(2, 1, 2)
            plt.plot(xf, magnitude)
            plt.title('fft of sine over frequency range')
        else:
            plt.plot(xf, magnitude)
            plt.grid()
            plt.title('fft of sine over frequency range')

        plt.savefig(name)

# ah = AudioHandler()
# ah.plot_fft(xf, yf, x, y, 'FFT of Song Data')

channel = list()
channel_volume = list()
for i in range(10):
    channel.append(max(magnitude[i*50:(i+1)*50])) 
    #print("Channel ",(i+1)," max (", i*50, ":", (i+1)*50, ") is: ", channel[i])
    channel_volume.append(int(max(magnitude[i*50:(i+1)*50])/400))
    print("channel vol: ", channel_volume[i])
for x in range(5):
    channel.append(max(magnitude[500+x*100:500+(x+1)*100])) 
    #print("Channel ",(x+11)," max (", 500+x*100, ":", 500+(x+1)*100, ") is: ", channel[x])
    channel_volume.append(int(max(magnitude[500+x*100:500+(x+1)*100])/400))
    print("channel vol: ", channel_volume[x])
for n in range(5):
    channel.append(max(magnitude[1000+n*200:1000+(n+1)*200])) 
    #print("Channel ",(n+16)," max (", 1000+n*200, ":", 1000+(n+1)*200, ") is: ", channel[n])
    channel_volume.append(int(max(magnitude[1000+n*200:1000+(n+1)*200])/400))
    #rint("channel vol: ", channel_volume[n])

ph = NeoHandler(pixel_pin=board.D18, num_pixels=300, brightness=0.1, auto_write=False, pixel_order="GRB")
ph.display_volumes(freq_vols=channel_volume, keep=True)
