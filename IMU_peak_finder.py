import numpy as np 
from scipy import signal
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

test_data = pd.read_csv('test_filtered_accelerometer_data.csv')

right_accel_SUM = test_data['right SUM']
left_accel_SUM = test_data['left SUM']

#NOW WE DO PEAK FIND 
right_accel_SUM_peaks = find_peaks(right_accel_SUM, prominence = 0.1, distance = 25)
right_accel_SUM_peaks = right_accel_SUM_peaks[0]
print(right_accel_SUM_peaks)

left_accel_SUM_peaks = find_peaks(left_accel_SUM, prominence = 0.1, distance = 25)
left_accel_SUM_peaks = left_accel_SUM_peaks[0]
print(left_accel_SUM_peaks)

