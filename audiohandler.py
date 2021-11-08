from scipy.io import wavfile
from scipy.fftpack import fft, fftfreq
import numpy as np
import matplotlib.pyplot as plt


class AudioHandler:
    ''''''

    def __init__(self, song_title) -> None:
        # read in song waveform data
        # samplerate - Number of data points to sample for transform
        # data - audio waveform data array
        self.samplerate, self.data = wavfile.read(song_title, mmap=False)

        # convert to numpy array
        self.song_data = np.array(self.data[:])

        # length of song in seconds
        self.length_of_song = np.size(self.song_data) / self.samplerate

        # spacing between data points (song sample rate in denominator)
        self.T = 1.0 / self.samplerate
    

    def fft_at_time(self, second_to_transform):
        # data sample step
        second_to_transform = second_to_transform

        # 
        start_point = second_to_transform
        print('start point:', start_point, type(start_point))

        # time length of collected data
        stop_point = second_to_transform+1
        print('stop point:', stop_point, type(stop_point))

        # x-axis is frequency
        x = np.linspace(start_point, stop_point, self.samplerate, endpoint=False)
        # fft of frequency range
        xf = fftfreq(self.samplerate, self.T)[:self.samplerate//22]

        # y-axis input sinewaves
        y = self.song_data[start_point*self.samplerate:stop_point*self.samplerate]
        # fft of input signal
        yf = fft(y)
        #y-axis of the fourier tranform graph 
        self.magnitude_list = 2.0/self.samplerate * np.abs(yf[0:self.samplerate//22])


    # plot
    def plot_fft(self, xf, yf, xt = [], yt = [], name = 'Fourier Plot'):
        if xt.any() == True and yt.any() == True:
            plt.subplot(2, 1, 1)
            plt.plot(xt, yt)
            plt.title('sine input over time')

            plt.subplot(2, 1, 2)
            plt.plot(xf, self.magnitude_list)
            plt.title('fft of sine over frequency range')
        else:
            plt.plot(xf, self.magnitude_list)
            plt.grid()
            plt.title('fft of sine over frequency range')

        plt.savefig(name)


    def generate_volume_list(self, second_to_transform:int):
        self.fft_at_time(second_to_transform)
        channel_volume = list()

        for i in range(10):
            channel_volume.append(int(max(self.magnitude_list[i*50:(i+1)*50])/400))
            #print("Channel ",(i+1)," max (", i*50, ":", (i+1)*50, ") is: ", channel[i])
            # print("channel vol: ", channel_volume[i])
        for x in range(5):
            channel_volume.append(int(max(self.magnitude_list[500+x*100:500+(x+1)*100])/400))
            #print("Channel ",(x+11)," max (", 500+x*100, ":", 500+(x+1)*100, ") is: ", channel[x])
            # print("channel vol: ", channel_volume[x])
        for n in range(5):
            channel_volume.append(int(max(self.magnitude_list[1000+n*200:1000+(n+1)*200])/400))
            #print("Channel ",(n+16)," max (", 1000+n*200, ":", 1000+(n+1)*200, ") is: ", channel[n])
            #rint("channel vol: ", channel_volume[n])
        
        return channel_volume
