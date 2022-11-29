
import wave 
import numpy as np
#from winsound import PlaySound,SND_FILENAME
#import matplotlib.pyplot as plt

def write_wav(data,file_path,sampwidth,framerate):
      # create wav file
      with wave.open(file_path,'wb') as f:
            f.setnchannels(1)
            f.setsampwidth(sampwidth)
            f.setframerate(framerate)
            f.writeframes(data.tostring()) 
            f.close()
            #PlaySound(file_path,SND_FILENAME) # paly wav file



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

#use median information replace noise information

def get_median(data):
      data = sorted(data)
      size = len(data)
      if size % 2 == 0: # even
            median = (data[size//2]+data[size//2-1])/2
            data[0] = median
      if size % 2 == 1: # odd
            median = data[(size-1)//2]
            data[0] = median
      return data[0]

def cublic_replece(pos_list,data_steam,filter_len = 8):
      data_steam = list(data_steam)
      data = data_steam.copy()
      half = int((filter_len)/2)
      if filter_len % 2 == 1:
            print(" filter length is not a even number")
            raise
      all= len(pos_list)
      count = 0
      for pos_s in pos_list:
            count +=1
            replace_num = len(pos_s)   #the number of missing values in the interval

            start_pos = pos_s[0] - half 
            end_pos   =  pos_s[-1] +half 
            
            #Build an interpolation model
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
            
