import serial
import re
import io
from matplotlib import pyplot as plt
from scipy import signal
import numpy as np
from librosa.feature import melspectrogram
from PIL import Image
import tensorflow as tf



SAMPLE_RATE = 500
PERIOD = 1/SAMPLE_RATE
EPSILON = 15

s = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
nums = re.compile(r"[+-]?\d+(?:\.\d+)?")

model = tf.keras.models.load_model('iot_model.h5')


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

                
                derivative = []

                for i in range(1, 513):
                    
                    delta = (samples[i+1]-samples[i-1])/(2*PERIOD)
                    if abs(delta) > EPSILON:
                        # print(delta)
                        sign += delta

                    derivative.append(delta)
                    
                    
                    if sign >= 0:
                        sign = +1.0
                    else:
                        sign = -1.0
                
                    # print(sign)
                S = melspectrogram(y=np.array(derivative, dtype='float32'),sr=SAMPLE_RATE,n_mels=128,n_fft=1024,hop_length=16)
                S = S * sign
                
                fig = plt.figure(figsize=(128, 33))
                plt.pcolormesh(np.arange(0, 33), np.arange(0, 128), S)
                plt.axis('off')
                
                def fig2img(fig):
                    import io
                    buf = io.BytesIO()
                    fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
                    buf.seek(0)
                    img = Image.open(buf)
                    img = img.resize((128, 32)) 
                    return img

                img = fig2img(fig) 
                img = img.convert('RGB')
                nimg = np.array(img)
                print(nimg.shape)
                a = np.transpose(nimg, (1, 0, 2))
                a = a.reshape((1, 128, 32, 3))
                tensor1 = tf.convert_to_tensor(a)

                print(model(tensor1))
                    # plt.savefig('data/'+str(num)+'-'+str(j)+'3.png', bbox_inches='tight', pad_inches=0)
                    # plt.close()

                num+=1
                samples = []
                sign = 0
                

