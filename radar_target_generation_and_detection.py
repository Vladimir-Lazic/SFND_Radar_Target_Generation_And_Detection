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
User Defined Range and Velocity of target
"""

import math
import numpy as np
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


radar = Radar(frequency=77, max_range=200, range_resolution=1, max_velocity=100)

print("Get slope: ", radar.get_slope())

number_of_chirps = 128
number_of_samples_per_chirp = 1024

time_stamps = np.linspace(
    0,
    number_of_chirps * radar.get_chirp(),
    number_of_samples_per_chirp * number_of_chirps,
)

Tx = np.zeros(len(time_stamps))
Rx = np.zeros(len(time_stamps))
Mix = np.zeros(len(time_stamps))

delay_time = 2 * target_distance / speed_of_light

for i in range(len(time_stamps)):
    time = time_stamps[i]
    Tx[i] = radar.transmit_signal(time)
    Rx[i] = radar.receive_signal(time, delay_time)
    range_freq = 2 * radar.get_slope() * target_distance / speed_of_light
    doppler_freq = 2 * radar.fc * target_velocity / speed_of_light
    Mix[i] = math.cos(2 * math.pi * (range_freq + doppler_freq) * time)


print(Mix)
plt.plot(Mix)
plt.show()
