from scipy.fft import fft, fftfreq
import numpy as np
from scipy.io import wavfile

# y axis

samplerate, data = wavfile.read("Broken Bones.wav", mmap=False)
y = np.array(data[0:4500000])

# Number of sample points

N = 1024

# sample spacing

T = 1.0 / 44100

# x axis

x = np.linspace(0.0, N*T, N, endpoint=False)

yf = fft(y)

xf = fftfreq(N, T)[:N//2]

import matplotlib.pyplot as plt

plt.plot(x, y)

plt.grid()

plt.savefig("THISONE")

plt.plot(xf, 2.0/N * np.abs(yf[0:N//2]))

plt.savefig("THATONE")

print("DONE!")