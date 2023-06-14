import serial
import re
from matplotlib import pyplot as plt
from scipy import signal
import numpy as np
from librosa.feature import melspectrogram

SAMPLE_RATE = 500
PERIOD = 1/SAMPLE_RATE
EPSILON = 15

s = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
nums = re.compile(r"[+-]?\d+(?:\.\d+)?")

samples = []
Derivatives=[]
index = 0
num = 1
sign = 0

while True:
    ser = s.readline()
    a = str(ser)
    if 'Irms' in a:
        search = nums.search(a)
        if search != None:
            i_rms = float(search.group(0))
            if i_rms > 10.0: continue
            samples.append(i_rms)

            if len(samples) > 515:
                Samples = []
                Samples.append(samples)
                samples_nump = np.array(samples)
                for i in range(4):
                    noise = np.random.normal(0, 0.004, len(samples))
                    new_ = samples_nump + noise
                    Samples.append(new_)
                
                for j in range(len(Samples)):    
                    derivative = []

                    for i in range(1, 513):
                        
                        delta = (Samples[j][i+1]-Samples[j][i-1])/(2*PERIOD)
                        if abs(delta) > EPSILON:
                            # print(delta)
                            if j == 0:
                                sign += delta

                        derivative.append(delta)
                    
                    if j == 0:
                        if sign >= 0:
                            sign = +1.0
                        else:
                            sign = -1.0
                    
                    # print(sign)
                    S = melspectrogram(y=np.array(derivative, dtype='float32'),sr=SAMPLE_RATE,n_mels=128,n_fft=1024,hop_length=16)
                    S = S * sign
                        
                    plt.figure(figsize=(128, 33))
                    plt.pcolormesh(np.arange(0, 33), np.arange(0, 128), S)
                    plt.axis('off')
                    plt.savefig('data/'+str(num)+'-'+str(j)+'3.png', bbox_inches='tight', pad_inches=0)
                    plt.close()

                num+=1
                samples = []
                sign = 0
                

