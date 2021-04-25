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

class Radar:
      def __init__(self, frequency, max_range, range_resolution, max_velocity):
          self.frequency = frequency
          self.max_range = max_range
          self.range_resolution = range_resolution
          self.max_velocity = max_velocity


radar = Radar(77, 200, 1, 100)

