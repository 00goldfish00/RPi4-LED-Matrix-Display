from scipy.io import wavfile
from scipy.fftpack import fft, fftfreq
import numpy as np
import matplotlib.pyplot as plt
import math


class AudioHandler:
    '''class to handle fourier transforming audio data samples'''

    def __init__(self, song_title, display_length:int, columns:int) -> None:
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

        self.x = list()
        self.xf = list()
        self.y = list()
        self.yf = list()

        # maximum points that can be generated as a volume setting
        self.points_per_column = math.ceil(display_length // columns)
        self.columns = columns
    

    def fft_at_time(self, second_to_transform):

        # first data point of sample to transform
        start_point = second_to_transform
        #print('start point:', start_point, type(start_point))

        # last data point of sample to transform
        stop_point = second_to_transform+1
        #print('stop point:', stop_point, type(stop_point))

        # x-axis is frequency
        self.x = np.linspace(start_point, stop_point, self.samplerate, endpoint=False)
        # fft of frequency range
        self.xf = fftfreq(self.samplerate, self.T)[:self.samplerate//2]

        # y-axis input sinewaves
        self.y = self.song_data[start_point*self.samplerate:stop_point*self.samplerate]
        # fft of input signal
        self.yf = fft(self.y)
        #y-axis of the fourier tranform graph 
        self.magnitude_list = 2.0/self.samplerate * np.abs(self.yf[:self.samplerate//2])


    # plot
    def plot_fft(self, name = 'Fourier Plot'):
        plt.subplot(2, 1, 1)
        plt.plot(self.x, self.y)
        plt.title('Song Data Sample')

        plt.subplot(2, 1, 2)
        plt.plot(self.xf, self.magnitude_list)
        plt.title('Frequnecy Magnitudes of Sample')
        plt.subplots_adjust(hspace=.2)
        plt.tight_layout()
        plt.show()

        plt.savefig(name)



    def scale_to_volume(self, freq_mag_list:list):
        '''scales frequency magnitudes to volumes based on the number of LEDs in a column'''
        volume_list = list()
        max_freq = max(freq_mag_list)

        for mag in freq_mag_list:
            volume_list.append(int(mag * self.points_per_column // max_freq))

        return volume_list


    def generate_volume_list(self, second_to_transform:int):
        '''generates a list of frequency volumes for a given second of song data\n
        assumes 20 columns!'''
        self.fft_at_time(second_to_transform)
        
        mag_maxes = np.zeros(20, dtype = int)

        bound = self.columns // 5
        for x in range (bound):
            mag_maxes[x] = (max(self.magnitude_list[x*10:(x+1)*10]))
            mag_maxes[x + bound] = (max(self.magnitude_list[40+x*52:40+(x+1)*52]))
            mag_maxes[x + 2*bound] = (max(self.magnitude_list[248+x*438:248+(x+1)*438]))
            mag_maxes[x + 3*bound] = (max(self.magnitude_list[2000+x*1125:2000+(x+1)*1125]))
            mag_maxes[x + 4*bound] = (max(self.magnitude_list[6500+x*2375:6500+(x+1)*2375]))
        
        #print(self.scale_to_volume(mag_maxes))
        return self.scale_to_volume(mag_maxes)
