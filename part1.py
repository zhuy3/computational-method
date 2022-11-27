import wave
import numpy as np

def read_wav(path):
    with wave.open(path, 'rb') as wr:
        params = wr.getparams()
        sampwidth = params[1]
        framerate = params[2]
        nframes = params[3]
        data = wr.readframes(nframes)
        w = np.fromstring(data,dtype=np.int16)
    return w

clean_wav = read_wav('clean_z.wav')
degraded_wav = read_wav('degraded_z.wav')
detect_wave = read_wav('detectionfile_z.wav')
#degraded_wav = list(degraded_wav)
#degraded-wav.append(0)
#degraded_wav = np.array(degraded_wav)
len(clean_wav) == len(degraded_wav) ==len(detect_wave)
value = max(detect_wave)
bk_position = np.where(detect_wave > value-1000)[0]

