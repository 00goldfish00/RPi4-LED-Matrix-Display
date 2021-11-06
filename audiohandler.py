from scipy.io import wavfile
from scipy.fftpack import fft
import numpy as np
import math
import matplotlib.pyplot as plt
import pyaudio

plt.close('all')

# pa = pyaudio.PyAudio()
# audio_stream = pa.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, output=True, frames_per_buffer=1024)

audio_data = wavfile.open("Broken Bone.wav")

data_points = 100000
time = np.arange(0, 0.005, 1/data_points)
freq = 5000

sine = np.sin(2*math.pi*freq*time)

n = np.size(time)
fr = (data_points/5) * np.linspace(0, 1, int(n/5))

X = fft(sine)   # Take the Fourier Transform
X_mag = abs(X[0:np.size(fr)])


plt.subplot(2, 1, 1)
plt.plot(time, sine)
plt.title('Sinusodial Signal')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')


plt.subplot(2, 1, 2)
plt.plot(fr, X_mag)
plt.title('Fast Fourier Transform of Sinusodial Signal')

plt.savefig("fourier")


# class AudioHandler():
#     ''''''

#     def __init__(self) -> None:
#         pass
