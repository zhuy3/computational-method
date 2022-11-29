import wave 
import numpy as np
import unittest
import time
from tqdm import tqdm
from playsound import playsound#,SND_FILENAME
import matplotlib.pyplot as plt


#create audio wav
def write_wav(data,file_path,sampwidth,framerate):
      
      with wave.open(file_path,'wb') as f:
            f.setnchannels(1)
            f.setsampwidth(sampwidth)
            f.setframerate(framerate)
            #f.setnframes(length)
            f.writeframes(data.tobytes()) 
            f.close()
            playsound(file_path)#,SND_FILENAME) # paly wav
            playsound('degraded_z.wav')
            playsound('median.wav')




def mse(y1,y2):
      return sum((y1-y2)**2)/len(y1)

#open audio wav
def read_wav(path):
     
      with wave.open(path, 'rb') as wr:
            # parameters：(nchannels, sampwidth, framerate, nframes, comptype, compname)
            params = wr.getparams()
            sampwidth = params[1]
            framerate = params[2]
            nframes = params[3]
            # read data of audio
            data = wr.readframes(nframes)
            w = np.frombuffer(data,dtype=np.int16)
      return w,sampwidth,framerate

#use median data replace noise data

def get_median(data):
      data = sorted(data)
      size = len(data)
      median = data[(size-1)//2]
      data[0] = median

      return data[0]


def median_replece(pos_list,data_steam,filter_len = 17):
      data = data_steam.copy()
      diff = (filter_len-1)/2
      if filter_len % 2 != 0:
            print(" filter length is a odd number")

      all= len(pos_list)     
      count = 0
      for pos_s in pos_list:#pos_s : adjacent group of noise
            count +=1
            for pos in pos_s:#pos : location of each noise
                  pos_start = int(pos-diff)
                  pos_end = int(pos+diff)
                  window = data[pos_start:pos_end+1]
                  data[pos] = get_median(window)
            print(int(100*count/all),'%')
      return data


def median_filter(clean_wav,degraded_wav,detect_wave,out_wave):
      clean_wav,sampwidth,framerate =  read_wav('clean_z.wav')
      degraded_wav,_,_ =  read_wav('degraded_z.wav')
      detect_wave,_,_ = read_wav('detectionfile_z.wav')

      len(clean_wav) == len(degraded_wav) ==len(detect_wave)

      value = max(detect_wave)
      bk_positions = np.where(detect_wave > value - 1000)[0]#the noise filter value is much larger than the surrounding value

      bk_inf= [[]]
      for i in range(len(bk_positions)-1):
            bk_inf[-1].append(bk_positions[i])
            if bk_positions[i+1] - bk_positions[i]>1  : 
                  bk_inf.append([])
            if i == len(bk_positions)-2:
                  bk_inf[-1].append(bk_positions[i+1])  

      for i in tqdm(range(10)):
           time.sleep(0.5)


      output_data = median_replece(bk_inf,degraded_wav)

      write_wav(output_data,out_wave,sampwidth,framerate)
      print('MSE:',mse(clean_wav,output_data))

      plt.plot(range(len(output_data)),degraded_wav)
      plt.title("degraded_wav")
      plt.show()

      plt.plot(range(len(output_data)),output_data)
      plt.title("final wave")
      plt.show()

      return mse(clean_wav,output_data)





import unittest
class forTestTest(unittest.TestCase):  
      def test1(self):
            clean_wav =  read_wav('clean_z.wav')
            degraded_wav =  read_wav('degraded_z.wav')
            detect_wave = read_wav('detectionfile_z.wav')
            result = median_filter(clean_wav,degraded_wav,detect_wave,'median.wav')
            self.assertNotEqual(result,0)

            print(result,'result')


if __name__ == '__main__':
      unittest.main()