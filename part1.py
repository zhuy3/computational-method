import wave
import numpy as np
import time
import matplotlib.pyplot as plt

from time import sleep
from tqdm import tqdm


#from progressbar import progressbar
start = time.time()

#import scipy

#from scipy.io import wavfile

def read_wav(path):
    with wave.open(path, 'rb') as wr:
        params = wr.getparams()
        sampwidth = params[1]
        framerate = params[2]
        nframes = params[3]
        data = wr.readframes(nframes)
        w = np.frombuffer(data,dtype=np.int16)
    return w



clean_wav = read_wav('clean_z.wav')
degraded_wav = read_wav('degraded_z.wav')
detect_wave = read_wav('detectionfile_z.wav')
#degraded_wav = list(degraded_wav)
#degraded-wav.append(0)
#degraded_wav = np.array(degraded_wav)
len(clean_wav) == len(degraded_wav) ==len(detect_wave)

value = max(detect_wave)
bk_positions = np.where(detect_wave > value-500)[0]

bk_inf = [[]]
for i in range (len(bk_positions)-1):
    bk_inf[-1].append(bk_positions[i])
    if bk_positions[i+1] - bk_positions[i]>1:
        bk_inf.append([])
    if i == len(bk_positions)-2:
        bk_inf[-1].append(bk_positions[i+1])


def get_median(data):
      data = sorted(data)
      win_size = len(data)
      if win_size % 2 == 0:
              median1 = (data[win_size//2]+data[win_size//2-1])/2
              data[0] = median1
      if win_size % 2 == 1:
              median2 = data[(win_size-1)//2]
              data[0] = median2
      
      return data[0]

def median_replace(pos_list,data_steam,filter_len = 5):
      data = data_steam.copy()
      diff = (filter_len-1) // 2
      if filter_len % 2 != 0:
            print("Filter length is a odd number")


            for i in tqdm(range(10)):
                  #for i in range(len(bk_positions)):
                        #print(bk_positions[i])
                        #if bk_positions[i] > 0:
                              #data[i - diff : i + diff] = get_median(bk_positions[i - diff : i + diff].tolist(), filter_len)
                  sleep (0.5) 
        
        
      #all = len(pos_list)
      count = 0
      for pos_s in pos_list:
            count +=1
            for pos in pos_s:
                  pos_start = int(pos-diff)
                  pos_end = int(pos+diff)
                  window = data[pos_start:pos_end+1]
                  data[pos] = get_median(window)
                  
            
            #print(int(100*count/all),'%')
            #if int(100*count/all) == 100:
              #print('Done')
      return data     
end = time.time()

output_wav = median_replace(bk_inf, degraded_wav)


def mse(y1,y2):
      return sum((y1-y2)**2)/len(y1)
print('MSE:',mse(clean_wav,output_wav))

