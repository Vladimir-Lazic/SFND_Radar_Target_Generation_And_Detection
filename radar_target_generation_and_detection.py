"""
Python Implementation of Sensor Fusion Radar Project 

Radar Specifications 
###########################
Frequency of operation = 77GHz
Max Range = 200m
Range Resolution = 1 m
Max Velocity = 100 m/s
###########################

speed of light = 3e8
User Defined Range adoppler_samples Velocity of target
"""

import math
import numpy as np
import scipy.fft as fft
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

speed_of_light = 3e8
target_distance = 110
target_velocity = -20


class Radar:
    def __init__(self, frequency, max_range, range_resolution, max_velocity):
        self.frequency = frequency
        self.max_range = max_range
        self.range_resolution = range_resolution
        self.max_velocity = max_velocity

        self.fc = 77e9  # Operating carrier frequency of radar

    def get_bandwidth(self):
        return speed_of_light / (2 * self.range_resolution)

    def get_chirp(self):
        return (5.5 * 2 * self.max_range) / speed_of_light

    def get_slope(self):
        return self.get_bandwidth() / self.get_chirp()

    def transmit_signal(self, time):
        return math.cos(
            2 * math.pi * (self.fc * time + ((self.get_slope() * time * time) / 2))
        )

    def receive_signal(self, time, delay_time):
        time_diff = time - delay_time
        return math.cos(
            2
            * math.pi
            * (self.fc * time_diff + ((self.get_slope() * time_diff * time_diff) / 2))
        )

    def calculate_beat_signal(self):
        pass


# FMCW Waveform Generation
radar = Radar(frequency=77, max_range=200, range_resolution=1, max_velocity=100)

print("Get slope: ", radar.get_slope())

doppler_samples = 128
range_samples = 1024

time_stamps = np.linspace(
    0,
    doppler_samples * radar.get_chirp(),
    range_samples * doppler_samples,
)

Tx = np.zeros(len(time_stamps))
Rx = np.zeros(len(time_stamps))
Mix = np.zeros(len(time_stamps))

target_range = np.zeros(len(time_stamps))
delay_time = np.zeros(len(time_stamps))

for i in range(len(time_stamps)):
    time = time_stamps[i]

    target_range[i] = target_distance * target_velocity * time
    delay_time[i] = 2 * target_range[i] / speed_of_light

    Tx[i] = radar.transmit_signal(time)
    Rx[i] = radar.receive_signal(time, delay_time[i])
    Mix[i] = Tx[i] * Rx[i]

# RANGE MEASUREMENT

Mix = np.reshape(Mix, (range_samples, doppler_samples))

## Performing FFT along the range_samples axis
beat_signal_fft = fft.fft(Mix, axis=0)

## Normalizing the output
normalized_length = radar.get_chirp() * radar.get_bandwidth()
beat_normalize = np.absolute( beat_signal_fft / normalized_length)
beat_signal = beat_normalize[: int(normalized_length / 2)]
print(beat_signal.shape)

axis = np.linspace(0, normalized_length/2)
f = radar.get_bandwidth()*(axis)/normalized_length
plt.plot(f, beat_signal)
plt.show()
