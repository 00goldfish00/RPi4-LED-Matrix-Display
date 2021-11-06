from scipy.fftpack import fft
import numpy as np
import math
import matplotlib.pyplot as plt
import pyaudio


t = np.arange(0, 1, 1/1000)

sine = np.sin(2*math.pi*20*t)

plt.subplot(2, 1, 1)
plt.plot(t, sine)
plt.title('Sinusodial Signal')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')

X = fft(sine)   # Take the Fourier Transform

plt.subplot(2, 1, 2)
plt.plot(X)
plt.title('Fast Fourier Transform of Sinusodial Signal')


class AudioHandler():
    ''''''

    def __init__(self) -> None:
        pass
