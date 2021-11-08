from scipy.io import wavfile
from scipy.fftpack import fft, fftfreq
import numpy as np
import matplotlib.pyplot as plt
import math


class AudioHandler:
    '''calss to handle '''

    def __init__(self, song_title, display_length:int, max_vol:int) -> None:
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

        # maximum points that can be generated as a volume setting
        self.points_per_column = max_vol
        self.columns = display_length // max_vol
    

    def fft_at_time(self, second_to_transform):
        # data sample step
        second_to_transform = second_to_transform

        # first data point of sample to transform
        start_point = second_to_transform
        #print('start point:', start_point, type(start_point))

        # last data point of sample to transform
        stop_point = second_to_transform+1
        #print('stop point:', stop_point, type(stop_point))

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



    def scale_to_volume(self, freq_mag_list:list):
        '''scales frequency magnitudes to volumes based on the number of LEDs in a column'''
        volume_list = list()
        max_freq = max(freq_mag_list)

        for mag in freq_mag_list:
            volume_list.append(int(mag * self.points_per_column / max_freq))

        return volume_list


    def generate_volume_list(self, second_to_transform:int):
        '''generates a list of frequency volumes for a given second of song data'''
        self.fft_at_time(second_to_transform)
        mag_maxes = list()

        for i in range(math.ceil(self.columns/2)):
            mag_maxes.append(max(self.magnitude_list[i*50:(i+1)*50]))
            #print("Channel ",(i+1)," max (", i*50, ":", (i+1)*50, ") is: ", channel[i])
            # print("channel vol: ", channel_volume[i])
        for x in range(math.floor(self.columns/4)):
            mag_maxes.append(max(self.magnitude_list[500+x*100:500+(x+1)*100]))
            #print("Channel ",(x+11)," max (", 500+x*100, ":", 500+(x+1)*100, ") is: ", channel[x])
            # print("channel vol: ", channel_volume[x])
        for n in range(math.floor(self.columns/4)):
            mag_maxes.append(max(self.magnitude_list[1000+n*200:1000+(n+1)*200]))
            #print("Channel ",(n+16)," max (", 1000+n*200, ":", 1000+(n+1)*200, ") is: ", channel[n])
            #rint("channel vol: ", channel_volume[n])
        
        return self.scale_to_volume(mag_maxes)
