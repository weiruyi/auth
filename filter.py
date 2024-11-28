
import os

import librosa
import numpy as np
import scipy.signal
from scipy.io import wavfile

#注意修改路径



#低通
lowcut = 3000
#高通
highcut =22000
FRAME_RATE = 44100

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = scipy.signal.butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = scipy.signal.lfilter(b, a, data)
    return y

def bandpass_filter(buffer):
    return butter_bandpass_filter(buffer, lowcut, highcut, FRAME_RATE, order=3)




def getwavfiles(path):
    wav = []
    for root, _, files in os.walk(path):
        for file in files:
            wav.append(os.path.join(path, file))
    return wav



def filtered_write(wave, filtered_path):
    print(wave)
    #samplerate, data=librosa.load(os.path.join(wave), sr=44100)
    samplerate, data = wavfile.read(os.path.join(wave))
    print(type(data))
    #print(data.shape)
    #assert samplerate == FRAME_RATE
    filtered = np.apply_along_axis(bandpass_filter, 0, data).astype('int16')
    print(filtered)
    #
    print(type(filtered))
    # print(filtered.shape)
    # wave_file = wave.split("/")[2]
    wave_file = wave.replace("split", "filtered")
    print(wave_file)
    file_name = os.path.basename(wave_file)
    dir_path = os.path.dirname(wave_file)
    print(dir_path)
    # filtered_dir_path = os.path.join(filtered_path+dir_path)
    # print(filtered_dir_path)
    # if not os.path.exists(filtered_dir_path):
    #     os.makedirs(filtered_dir_path)
    # wavfile.write(os.path.join(filtered_path+wave.split("/")[2]), samplerate, filtered)

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    wavfile.write(os.path.join(wave_file), samplerate, filtered)







path = "/Users/lance/Desktop/Auth/dataset/split/"
for root, dirs, files in os.walk(path):
    # 遍历当前目录下的所有文件
    for file in files:
        if (file.startswith(".")):
            continue
        wave = os.path.join(root, file)
        print("=========================================")
        print(wave)
        # wave_path = wave.split("/")[2]
        # print(wave_path.split("/"))
        # pos = wave_path.split("/")[1]
        # finger = wave_path.split("/")[2]
        # count = wave_path.split("/")[3]
        filtered_path = "/Users/lance/Desktop/Auth/dataset/filtered/"
        print(filtered_path)
        filtered_write(wave, filtered_path)
        print("==============filter completed================")

# dict = ["zz1","zz2", "zz3", "zz4", "zz5", "zz6", "zz7", "zz0"]
# # dict = ["zz2"]
# for name in dict:
#     root = "data/split/8/zz/" + name
#     print("===============" + name + "=================")
#     print(root.split("/")[4])
#     filtered_path="data/filtered/8/"+ root.split("/")[3] + "/"
#     print(filtered_path)
#     wavs = getwavfiles(root)
#     for wav in wavs:
#         print(wav)
#         filtered_write(wav)
