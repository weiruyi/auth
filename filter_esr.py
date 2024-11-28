import os

import librosa
import numpy as np
import pandas as pd
import scipy.signal
from pydub import AudioSegment
from scipy.io import wavfile


def getwavfiles(path):
    wav = []
    for root, _, files in os.walk(path):
        for file in files:
            if ".png" not in str(file):
                wav.append(os.path.join(path, file))
    wav.sort()
    return wav






#ESR去噪
def esr(wave,w):

    print(wave)
    audio = AudioSegment.from_wav(wave)
    left_channel = audio.split_to_mono()[0]
    right_channel = audio.split_to_mono()[1]

    left_channel_array = np.array(left_channel.get_array_of_samples())
    right_channel_array = np.array(right_channel.get_array_of_samples())
    np.set_printoptions(threshold=np.inf)
    lenleft=len(left_channel_array)
    i=0
    j=0
    sumleft=1
    sumright=1
    cnt=0
    avg_esr=0.000
    print(lenleft)
    print(len(right_channel_array))
    #计算连续1000个采样点的平均ESR
    while(i+j+1000<=lenleft):
        if(abs(left_channel_array[i])>1 and abs(right_channel_array[i])>1 ):
            while(j<1000):
                sumleft+=abs(left_channel_array[i+j])
                sumright+=abs(right_channel_array[i+j])
                j=j+1
            j=0
            print(sumright)
            print(sumleft)
            print((sumright/(sumleft)))
            avg_esr=((sumright/(sumleft)))
            if avg_esr<1.0:
                while(j<1000):
                    left_channel_array[i+j]=0
                    right_channel_array[i+j]=0
                    j=j+1
            j=0
            
        
        #避免除0
        sumleft=1
        sumright=1
        
        avg_esr=0
        i=i+1000
    e=np.stack((left_channel_array,right_channel_array), axis=1)
    #下句不可用，会影响音频的绝对大小
    #e= np.ascontiguousarray(e)
    dir_path = os.path.dirname(filtered_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    wavfile.write(filtered_path,44100,e)
    print("*******************ESR****************************")
    print(avg_esr)

    print("\n\n")
    
    return avg_esr


# #注意修改两个路径
# dict = ["zz1","zz2", "zz3", "zz4", "zz5", "zz6", "zz7", "zz0"]
# # dict = ["zz2"]
# for name in dict:
#     root = "data/filtered/8/zz/" + name
#     filtered_path="data/filtered_esr/8/"+root.split("/")[3]
#
#     data = []
#     wavs = getwavfiles(root)
#     for wav in wavs:
#         # print(wav)
#         x=esr(wav,w=filtered_path)

path = "/Users/lance/Desktop/Auth/dataset/filtered/"
for root, dirs, files in os.walk(path):
    # 遍历当前目录下的所有文件
    for file in files:
        if (file.startswith(".")):
            continue
        wave = os.path.join(root, file)
        print("=========================================")
        print(wave)
        # wave_path = wave.split("/")[2]
        # print(wave_path)
        # print(wave_path.split("\\"))
        # pos = wave_path.split("\\")[1]
        # finger = wave_path.split("\\")[2]
        # count = wave_path.split("\\")[3]
        # filtered_path = "/Users/lance/Desktop/Auth/dataset/filtered_esr/"+wave_path
        filtered_path = wave.replace("filtered", "filtered_esr")
        x=esr(wave,w=filtered_path)
        print(filtered_path)
        print("==============filter_esr completed================")



# def estimate_snr(x, window_size):
#     x = x.astype(np.float32)
#     eps = np.finfo(x.dtype).eps  # 避免除数为0的情况
#     x_var = np.var(x)
#     sum_snr=0.0000
#     for i in range(window_size, len(x)):
#         x_seg = x[i-window_size:i]
#         x_seg_var = np.var(x_seg)

#         snr = x_seg_var / max(x_var - x_seg_var, eps)

#         sum_snr+=snr
#     snr_ava=sum_snr/window_size
#     # print("sum_snr:"+str(sum_snr))
#     # print("snr_ava:"+str(snr_ava))
#     return snr_ava









#频域esr， 此处代码错误
# root_path = './4_1/batch/9'
# fil="./4_1/fre/9/"
# for folder in os.listdir(root_path):
#     folder_path = os.path.join(root_path, folder)
#     if os.path.isdir(folder_path):
#         filtered_path = folder_path.replace('batch', 'fre')
#         for file in os.listdir(folder_path):
#             if file.endswith('.wav'):
#                 file_path = os.path.join(folder_path, file)
#                 filtered_folder = folder.replace('batch', 'fre')
#                 filtered_file_path = file_path.replace('batch', 'fre')
#                 filtered_file_path = filtered_file_path.replace(folder, filtered_folder)
#                 if os.path.exists(fil+filtered_folder):
#                     print("######################")
#                 else:
#                     os.mkdir(fil+filtered_folder)
#                 esr3(file_path,filtered_file_path)


#时域esr


