from scipy.io import wavfile    
from scipy.fftpack import fft, fftfreq
import numpy as np
import math
import matplotlib.pyplot as plt
import pyaudio

plt.close('all')

# pa = pyaudio.PyAudio()
# audio_stream = pa.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, output=True, frames_per_buffer=1024)

samplerate, data = wavfile.read("Marshmello Alone.wav", mmap=False)
song_data = np.array(data[:4500000])
print("number of data points = ", len(song_data))
print("song_data shape:", song_data.shape)
print("samplerate = ", samplerate)
length_of_song = np.size(song_data) / samplerate
print (f"length of song = {length_of_song} seconds")

time_axis = np.linspace(0, length_of_song, len(song_data))
print("time_axis shape:", time_axis.shape)


freq_range = np.linspace(0.0, len(song_data)/44100, len(song_data))
freq_range_fft = fftfreq(len(song_data), 1/44100)[:len(song_data)//2]
print("freq_range shape:", freq_range.shape)

song_data_fft = fft(song_data)
print("song_data_fft shape:", song_data_fft.shape)
# data_snip_mag = abs(song_data_fft[0:np.size(freq_range)])
# print("data_snip_mag shape:", data_snip_mag.shape)

plt.subplot(2, 1, 1)
plt.plot(time_axis, song_data)
# plt.xlabel("Time [s]")
# plt.ylabel("Amplitude")
plt.title('Song Data')

plt.subplot(2, 1, 2)
plt.plot(freq_range_fft, (2/len(song_data) * np.abs(song_data_fft[0:len(song_data)//2])))
plt.title('Fast Fourier Transform of Song Snippet')

plt.savefig("Song Fourier")

# Code to generate a sine wave
# data_points = 100000
# time = np.arange(0, 0.005, 1/data_points)
# freq = 5000

# sine = np.sin(2*math.pi*freq*time)

# n = np.size(time)
# fr = (data_points/5) * np.linspace(0, 1, int(n/5))

# X = fft(sine)   # Take the Fourier Transform
# X_mag = abs(X[0:np.size(fr)])

# plt.subplot(2, 1, 1)
# plt.plot(time, sine)
# plt.title('Sinusodial Signal')
# plt.xlabel('Time (s)')
# plt.ylabel('Amplitude')


# class AudioHandler():
#     ''''''

#     def __init__(self) -> None:
#         pass
