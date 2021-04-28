# Radar Target Generation And Detection Project

[//]: # (Image References)

[image1]: ./images/2d_fft.jpg "2D FFT"
[image2]: ./images/cfar.jpg "2D CFAR"
[image3]: ./images/fft.jpg "FFT"
[image4]: ./images/project_layout.png "Project Layout"
[image5]: ./images/radar.png "Radar"
[image6]: ./images/range_fft.jpg "Range FFT"
[image7]: ./images/tgnd.png "Target Generation And Detection"
[image8]: ./images/radar_spec.png "Radar Specs"

![alt text][image5]

This project implements a Radar target generation and detection system for the Udacity Sensor Fusion Nanodegree program. In the text bellow I will address each point in the [project rubric](https://review.udacity.com/#!/rubrics/2548/view). 

![alt text][image4]

## FMCW Waveform Design
In the scope of this project I have modeled a FMCW (Frequency-Modulated Continuous Wave) Radar. The FMWC signal in which the signal increases and decreases over time. Based on the radar specifications in the image bellow we can calculate the basic FMCW wave characteristics such as: Chirp Time, Bandwidth and Slope. The Chirp Time is time in which the radar transmits one upramp or downramp. The Bandwidth represents the amplitude of the signal. The Slope is the ratio of Bandwidth over Chirp Time.  

![alt text][image8]

## Simulation Loop
The initial target range is 110 meters with the velocity of -20. The model implemented in this project assumes the constant target velocity. For simulating the interaction between the radar and target I iterate over an array of evenly spaced timestamps. For each time stamp the target range is updated. The transmitted and received signals are defined by the equations in the image bellow. The received signal is the same as the transmitted signals only with a time delay which is the time it takes for the signal to make a round trip from the radar to the target and back to radar. By mixing the transmitted and received signal we calculate the beat signal which contains the range and doppler information.  

![alt text][image7]

## Range FFT (1st FFT)
By applying the 1D FFT on the beat signal along the range axis we extract the information of the original position of the target.

![alt text][image6]

In this image we see the output of 2D FFT

![alt text][image1]
## 2D CFAR
By applying the 2D CFAR method for determining a noise suppression threshold we are able to clearly identify the target. The first step in the implementation of 2D CFAR is determining the number of training and guard cells in both the range and doppler direction and the offset. The offset is used for adjusting the SNR (Sound-to-Noise Ratio) calculated and is set to 6. 
* The number of Training cells are: 
  * Tr = 14
  * Td = 6
* The number of Guard cells are:
  * Gr = 6
  * Gd = 3

After setting the hyperparameters we apply the CFAR sliding window method to the matrix with a margin. We use a margin in order to apply noise suppression to the cells at the edges. We want to avoid using the cells on the edges as cells under test (CUT). Instead those cells should fall under training cells. This way we ensure the noise suppression in all cells in the matrix. For every iteration we calculate the sum of the signal levels withing the training cells. The sum is converted from logarithmic to linear value using db2pow function. Then we average the summed values for all training cells used. The average is converted back to logarithmic value and the offset is added to determine the threshold. The we compare the value of the signal in the CUT with the threshold value and if the value of the signal in CUT is above the threshold we assign 1, if not 0. 

![alt text][image2]


