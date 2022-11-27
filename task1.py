import wave 
import numpy as np
#from tqdm import trange
from scipy.io import wavfile

#samplerate0, data = wavfile.read('clean_z.wav')
#samplerate1, data = wavfile.read('degraded_z.wav')
#samplerate2, data = wavfile.read('detectionfile_z.wav')



clean_wav =  wavfile.read('clean_z.wav')
degraded_wav = wavfile.read('degraded_z.wav')
detect_wave = wavfile.read('detectionfile_z.wav')
#degraded_wav = list(degraded_wav)
#degraded_wav.append(0)
#degraded_wav = np.array(degraded_wav)
len(clean_wav) == len(degraded_wav) ==len(detect_wave)

value = max(detect_wave)
bk_positions = np.where(detect_wave > value-1000)[0]

bk_inf= [[]]
for i in range(len(bk_positions)-1):
      bk_inf[-1].append(bk_positions[i])
      if bk_positions[i+1] - bk_positions[i]>1  : 
            bk_inf.append([])
      if i == len(bk_positions)-2:
          bk_inf[-1].append(bk_positions[i+1])  


#用中位数信息替换 噪声信息

def get_median(data):
      data = sorted(data)
      window_size = len(data)
      if window_size % 2 == 0: # 判断列表长度为偶数
            median = (data[window_size//2]+data[window_size//2-1])/2
            data[0] = median
      if window_size % 2 == 1: # 判断列表长度为奇数
            median = data[(window_size-1)//2]
            data[0] = median
      return data[0]


def median_replece(pos_list,data_steam,filter_len = 5):
      data = data_steam.copy()
      diff = (filter_len-1)/2
      if filter_len % 2 == 0:
            print(" filter length is not a odd number")
           # raise
      all= len(pos_list)
      count = 0
      for pos_s in pos_list:
            count +=1
            for pos in pos_s:
                  pos_start = int(pos-diff)
                  pos_end = int(pos+diff)

                  window = data[pos_start:pos_end+1]
                  data[pos] = get_median(window)
            print(int(100*count/all),'%')
      return data

output_wav = median_replece(bk_inf,degraded_wav)

def mse(y1,y2):
      return sum((y1-y2)**2)/len(y1)
print('MSE:',mse(clean_wav,output_wav))
