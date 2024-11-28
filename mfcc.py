import os

import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import scipy
import sklearn


def getwavfiles(path):
    wav = []
    for root, _, files in os.walk(path):
        for file in files:
            if ".png" not in str(file):
                wav.append(os.path.join(path, file))
    return wav

def waveplot(file):   
    x, fs = librosa.load(file)
    librosa.display.waveshow(x, sr=fs, color='blue')
    
    return x, fs
    
def mfcc(x, fs):
    mfccs = librosa.feature.mfcc(y=x,sr=fs,hop_length=1,win_length=128,window=0.01)
    return mfccs

    
def drawspec(mfcc, savename):
    plt.figure(figsize=(10, 4))
    #log
    librosa.display.specshow(mfcc)
    
    plt.title('MFCC')
    plt.tight_layout()
    plt.savefig(savename)

def mfcc_main(root,pic_dir):
    wavs = getwavfiles(root)
    # 指定要创建的文件夹路径
    folder_path = root + "/" + "mfcc/"

    # 使用 os.makedirs 创建文件夹，如果已存在则不会重复创建
    os.makedirs(folder_path, exist_ok=True)

    for wav in wavs:
        print(wav)
        x, fs = waveplot(wav)
        
        mfccs = mfcc(x, fs)
        file_name = os.path.basename(wav)
        print(file_name)
        savename = folder_path + file_name
        print(savename)
        drawspec(mfccs, savename.replace(".wav", "_mfcc.png"))

# mfcc_main("data/wavelet/bus/ys/bus_ys1","")
# mfcc_main("data/wavelet/bus/yz/bus_yz1","")
# mfcc_main("data/wavelet/bus/zs/bus_zs1","")
# mfcc_main("data/wavelet/bus/zz/bus_zz1","")

mfcc_main("data/wavelet/static/zz/zz1","")
mfcc_main("data/wavelet/static/zz/zz2","")
mfcc_main("data/wavelet/static/zz/zz3","")
mfcc_main("data/wavelet/static/zz/zz4","")
mfcc_main("data/wavelet/static/zz/zz5","")
mfcc_main("data/wavelet/static/zz/zz6","")
mfcc_main("data/wavelet/static/zz/zz7","")
mfcc_main("data/wavelet/static/zz/zz8","")
mfcc_main("data/wavelet/static/zz/zz9","")






