
import wave 
import numpy as np
import unittest
from scipy import interpolate
from playsound import playsound#,SND_FILENAME
import matplotlib.pyplot as plt


def write_wav(data,file_path,sampwidth,framerate):
      # create wav file
      with wave.open(file_path,'wb') as f:
            f.setnchannels(1)
            f.setsampwidth(sampwidth)
            f.setframerate(framerate)
            f.writeframes(data.tobytes()) 
            f.close()
            playsound(file_path)#PlaySound(file_path,SND_FILENAME) # paly wav file



def mse(y1,y2):
      return sum((y1-y2)**2)/len(y1)


def read_wav(path):
      # open wav file
      with wave.open(path, 'rb') as wr:
            # parameters：(nchannels, sampwidth, framerate, nframes, comptype, compname)
            params = wr.getparams()
            sampwidth = params[1]
            framerate = params[2]
            allframes = params[3]
            # read audio
            data = wr.readframes(allframes)
            w = np.frombuffer(data,dtype=np.int16)
      return w,sampwidth,framerate


def cublic_replece(pos_list,data_steam,filter_len = 2):
      data_steam = list(data_steam)
      data = data_steam.copy()
      half = int((filter_len)/2)
      if filter_len % 2 == 1:
            print(" filter length is not a even number")

      all= len(pos_list)
      count = 0
      for pos_s in pos_list:
            count +=1
            replace_num = len(pos_s)   #the number of missing values in the interval

            start_pos = pos_s[0] - half 
            end_pos   =  pos_s[-1] +half 
            
            #build an interpolation model
            temp1 = data_steam[start_pos:pos_s[0]]
            temp2 = data_steam[pos_s[-1]+1:end_pos+1]
            temp1.extend(temp2)
            y = temp1

            x1 = [i for i in range(half)]
            x2 = [i for i in range(half+replace_num,2*half+replace_num)] 
            x_hat  = np.array(range(half,half+replace_num))
            x = []
            x.extend(x1)
            x.extend(x2)
            #print(pos_s,x,y,(start_pos,pos_s[0]),end_pos,data_steam[pos_s[-1]])
            model = interpolate.interp1d(x,y,kind='cubic')
            new = model(x_hat)
            #print(new,y)

#Assign the interpolation result
            for i,pos in enumerate(pos_s):
                  data[pos] = new[i]
            print(int(100*count/all),'%')
      print("Done")
      return np.array(data,dtype=np.int16)


def cublic_filiter(clean_wav,degraded_wav,detect_wave,out_wave):
      clean_wav,sampwidth,framerate =  read_wav('clean_z.wav')
      degraded_wav,_,_ =  read_wav('degraded_z.wav')
      detect_wave,_,_ = read_wav('detectionfile_z.wav')

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


      output_data = cublic_replece(bk_inf,degraded_wav,filter_len = 8)
      print(type(output_data))
      print(type(clean_wav))
      write_wav(clean_wav,out_wave,sampwidth,framerate)

      plt.plot(range(len(output_data)),degraded_wav)
      plt.title("degraded_wav")
      plt.show()

      plt.plot(range(len(output_data)),output_data)
      plt.title("output wave")
      plt.show()
      print('MSE:',mse(clean_wav,output_data))
      return mse(clean_wav,output_data)



import unittest
class forTestTest(unittest.TestCase):  
      def test1(self):
            clean_wav =  read_wav('clean_z.wav')
            degraded_wav =  read_wav('degraded_z.wav')
            detect_wave = read_wav('detectionfile_z.wav')
            result = cublic_filiter(clean_wav,degraded_wav,detect_wave,'c.wav')
            self.assertNotEqual(result,0)

            print(result,'result')

if __name__ == '__main__':
      unittest.main()
            
