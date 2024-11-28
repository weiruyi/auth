import os

import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf
from scipy.io import wavfile


#获取音频文件路径
#音频路径举例：  ./dirs/wavdir/x.wav
def getwavfiles(path):
    wav = []
    for root, _, files in os.walk(path):
        for file in files:
            if ".png" not in str(file):
                wav.append(os.path.join(path, file))
    return wav



#读取音频
def waveplot(file):   

    
    x, fs = librosa.load(file,sr=44100)
    librosa.display.waveshow(x, sr=fs, color='blue')
    
    
    return x, fs
    

#使用librosa得到mfcc图谱
def mel(x, fs):
    #这里具体的hop_length,win_length,window需要根据音频时间调整
    #hop_length=1,win_length=128,window=0.01
    #目前参数是对1000/44100=0.022675737秒的音频取的
    #若音频为2秒左右，则参数可以依次调整为
    #hop_length=64,win_length=128,window=0.1

    mel_spect = librosa.feature.melspectrogram(y=x,sr=fs,hop_length=1,win_length=128,window=0.01)
    mel_spect = librosa.power_to_db(mel_spect, ref=np.max)
    
    
    return mel_spect





#将mfcc画成图谱
def drawspec(mel, savename,savepath):
    import matplotlib.font_manager as fm
    plt.figure(figsize=(10,4))
    #log
    librosa.display.specshow(mel, y_axis='mel',cmap='coolwarm')
    plt.tight_layout()
    # print(savepath)
    print(savename)
    dir_name = os.path.dirname(savename)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    plt.savefig(savename)
    plt.close('all')


#主函数

def mel_main(root,pic_dir):
    # wavs = getwavfiles(root)
    #
    #
    # for wav in wavs:
    prename = "D:\hnu\Auth\dataset\melPng_wry"
    for root, dirs, files in os.walk(root):
        for file in files:
            if file.endswith('.wav'):
                wav = os.path.join(root,file)
                x, fs = waveplot(wav)
        
                mfccs = mel(x, fs)
                wav = wav.replace("f", "mel_f")
                lt = wav.split("/")
                label = lt[8]
                no = lt[9]
                filename = os.path.basename(wav).replace(".wav","_" + no + "_mel.png")
                # filePath = os.path.join(prename, label, filename)
                filePath = ""
                if no <= '5' :
                    filePath = os.path.join(prename, "train", label, filename )
                else:
                    filePath = os.path.join(prename, "val", label, filename)
                drawspec(mfccs, filePath,pic_dir)



#第一个路径填写音频路径，第二个参数为图片存储路径
mel_main("/Users/lance/Downloads/Auth/dataset/split", "")




