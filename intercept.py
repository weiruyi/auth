
import os

import librosa
import numpy as np
import scipy.signal
from scipy.io import wavfile


def getwavfiles(path):
    wav = []
    for root, _, files in os.walk(path):
        for file in files:
            if ".png" not in str(file):
                wav.append(os.path.join(path, file))
    return wav





### 根据能量阈值进行去噪，截取高于4000的部分
def filtered_write(wave,w):
    print("*************start*************")
    samplerate, data = wavfile.read(os.path.join(wave))
    np.set_printoptions(threshold=np.inf)
    
    left_data=data[:,0]
    
    right_data=data[:,1]

    bound = []
    bound_r=[]
    count = 0
    sum_left=0
    sum_right=0
    lenl=len(left_data)
    lenr=len(left_data) #?

    while count < lenl - 2001 and count<lenr-2001:
        count += 1
        if abs(left_data[count])  <1800 and abs(right_data[count])<1800:
            # bound_r.append(0)
            # bound.append(0)

            continue
        else:
            i=-300
            while(i<700):
                bound_r.append(right_data[count+i])
                bound.append(left_data[count+i])
                i=i+1
            i=len(left_data)-len(bound)
            # while(i!=0):
            #     # bound_r.append(0)

            #     # bound.append(0)
            #     i=i-1




        break
    
    a=bound
    b=bound_r

    if len(a)<999:
        return a
    e=np.stack((a,b), axis=1)
    # with  open('after.txt','w') as f:
    #     f.write(str(e))
    #     f.close()
    
    e= np.ascontiguousarray(e)
    print(w)
    wavfile.write(w, samplerate,e)
    return e












#注意修改路径
prefix_path="/Users/lance/Desktop/Auth/dataset/filtered_esr/"
for root, dirs, files in os.walk(prefix_path):
    for file in files:
        if (file.startswith(".")):
            continue
        if file.endswith(".wav"):
            wave=os.path.join(root, file)
            print(wave)
            # filtered_path = "data/f/my_data/" + wave.split("/")[3]
            filtered_path = wave.replace("filtered_esr", "f")
            dir_name = os.path.dirname(filtered_path)
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
            print(filtered_path)
            e = filtered_write(wave, w=filtered_path)



    # for dir in dirs:
    #     print(dir)
    #     path=str(prefix_path)+str(dir)
    #     print(path)
    #     wavs = getwavfiles(path)
    #     print(wavs)
    #     for wav in wavs:
    #         print(wav)
    #         # 去噪后存储的路径，注意修改
    #         filtered_path="data/f/8/"+wav.split("/")[3]
    #         e=filtered_write(wav,w=filtered_path)






