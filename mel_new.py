import os
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from multiprocessing import Pool


# 获取音频文件路径
def getwavfiles(path):
    wav_files = []
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith('.wav'):
                wav_files.append(os.path.join(root, file))
    return wav_files


# 读取音频
def waveplot(file):
    x, fs = librosa.load(file, sr=44100)
    return x, fs


# 使用librosa得到mel图谱
def mel(x, fs):
    # 这里具体的hop_length,win_length,window需要根据音频时间调整
    # hop_length=1,win_length=128,window=0.01
    # 目前参数是对1000/44100=0.022675737秒的音频取的
    # 若音频为2秒左右，则参数可以依次调整为
    # hop_length=64,win_length=128,window=0.1

    mel_spect = librosa.feature.melspectrogram(y=x, sr=fs, hop_length=1, win_length=128, window=0.01)
    mel_spect = librosa.power_to_db(mel_spect, ref=np.max)

    return mel_spect


# 将mel图谱绘制成图像
def drawspec(mel, savename):
    import matplotlib.font_manager as fm
    plt.figure(figsize=(10,4))
    #log
    librosa.display.specshow(mel, y_axis='mel',cmap='coolwarm')
    plt.tight_layout()
    # print(savepath)
    # print(savename)
    dir_name = os.path.dirname(savename)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    plt.savefig(savename)
    plt.close()


# 处理每个音频文件
def process_wav_file(wav):
    prename = "/Users/lance/Downloads/Auth/dataset/melPng"

    # 加载和处理音频
    x, fs = waveplot(wav)
    mel_spect = mel(x, fs)

    # 若mel_spect为None，跳过保存
    if mel_spect is None:
        return

    lt = wav.split("/")
    label = lt[8]
    no = lt[9]
    n1 = lt[7]
    filename = os.path.basename(wav).replace(".wav", "_" + n1 +"_" + no + "_mel.png")
    # filePath = os.path.join(prename, label, filename)
    filePath = ""
    if int(no) <= 5:
        filePath = os.path.join(prename, "train", label, filename)
    else:
        filePath = os.path.join(prename, "val", label, filename)
    drawspec(mel_spect, filePath)
    print(f"Saved: {filePath}")


# 主函数
def mel_main(root):
    wav_files = getwavfiles(root)

    # 使用多进程池并行处理
    with Pool(processes=6) as pool:
        pool.map(process_wav_file, wav_files)

# 运行代码
if __name__ == "__main__":
    mel_main("/Users/lance/Downloads/Auth/dataset/f")