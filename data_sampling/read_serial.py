import serial
import re
from matplotlib import pyplot as plt
from scipy import signal
import numpy as np


s = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
nums = re.compile(r"[+-]?\d+(?:\.\d+)?")

samples = []
index = 0
counter = 0
num = 1

while True:
    ser = s.readline()
    if 'Irms' in str(ser):
        i_rms = nums.search(str(ser)).group(0)
        samples.append(i_rms)
        counter+=1
        if counter == 255:
            # f, t, Sxx = signal.spectrogram(np.array(samples, dtype='float32'), 200, nperseg=200 ,noverlap=200*4/5)
            # plt.pcolormesh(t, f, Sxx, shading='gouraud')
            plt.specgram(np.array(samples, dtype='float32'), Fs=200, cmap='gray')
            plt.show()
            # plt.savefig('data/'+str(num)+'.png')
            num+=1
            samples = []
            counter = 0

