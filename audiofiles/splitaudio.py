import wave
import contextlib
import math
import sys
import os
from pydub import AudioSegment
from scipy.io import wavfile

# filename = "17-1594"
filename = sys.argv[1]

## preprocessing
myfile = "../audiofiles/"+filename+".wav"
# myfile = filename+".wav"

with contextlib.closing(wave.open(myfile,'r')) as f:
    frames = f.getnframes()
    rate = f.getframerate()
    duration = frames / float(rate)

fs, data = wavfile.read(myfile)            # reading the file

newfilename = filename + "_1.wav"

wavfile.write(newfilename, fs, data[:, 0])   # saving first column which corresponds to channel 1
# wavfile.write('guitar_channel_2.wav', fs, data[:, 1])   # saving second column which corresponds to channel 2

# print(duration)

totaldur = math.ceil(duration) * 1000 # in millis

# t1 = 1 * 1000 #Works in milliseconds
# t2 = 2 * 1000

length = 60000-1 # 1 minute segments

tofile = "../audiofiles/sentdata/" + filename + "/splitfiles/" + filename + "-partX.wav"
# tofile = "./splitfiles/" + filename + "-partX.wav"

ct = 1
for i in range(0,totaldur, length):
    newAudio = AudioSegment.from_wav(newfilename)
    newAudio = newAudio[i:i+length]

    newAudio.export(tofile.replace("X", str(ct)), format="wav") #Exports to a wav file in the current path.
    ct += 1

os.remove("../textdata/"+newfilename)
# os.remove("./"+newfilename)
