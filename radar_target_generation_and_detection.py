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

speed_of_light = 3e8
target_distance = 110
target_velocity = -20

class Radar:
    def __init__(self, frequency, max_range, range_resolution, max_velocity):
        self.frequency = frequency
        self.max_range = max_range
        self.range_resolution = range_resolution
        self.max_velocity = max_velocity

    def get_bandwidth(self):
        return speed_of_light / (2 * self.range_resolution)

    def get_chirp(self):
        return (5.5 * 2 * self.max_range) / speed_of_light 

    def get_slope(self):
        return self.get_bandwidth() / self.get_chirp()


radar = Radar(77, 200, 1, 100)

print("Get slope: ", radar.get_slope())
