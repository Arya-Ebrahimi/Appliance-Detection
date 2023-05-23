import serial
import re
from matplotlib import pyplot as plt
from scipy import signal
import numpy as np
from librosa.feature import melspectrogram

SAMPLE_RATE = 500
PERIOD = 1/SAMPLE_RATE

s = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
nums = re.compile(r"[+-]?\d+(?:\.\d+)?")

samples = []
derivatives = []
index = 0
counter = 0
num = 1

while True:
    ser = s.readline()
    a = str(ser)
    if 'Irms' in a:
        search = nums.search(a)
        if search != None:
            i_rms = float(search.group(0))
            if i_rms > 10.0: continue
            print('Irms: ' + str(i_rms))
            samples.append(i_rms)
            counter+=1
            if counter >= 3:
                derivative = (samples[counter-1] - samples[counter-3])/(2*PERIOD)
                derivatives.append(derivative)
                print(derivative)
            if len(derivatives) >= 256:
                S = melspectrogram(y=np.array(derivatives, dtype='float32'),sr=SAMPLE_RATE,n_mels=128,n_fft=1024,hop_length=8)
                plt.pcolormesh(np.arange(0, 33), np.arange(0, 128), S)
                plt.savefig('data/'+str(num)+'.png')
                plt.show()
                num+=1
                samples = []
                derivatives = []
                counter = 0

