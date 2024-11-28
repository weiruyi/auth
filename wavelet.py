import os

import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import pywt
import soundfile as sf
from scipy.io import wavfile


#获取音频文件路径
def getwavfiles(path):
    wav = []
    for root, _, files in os.walk(path):
        for file in files:
            if ".png" not in str(file):
                wav.append(os.path.join(path, file))
    return wav










def func(infile,outfile):
    # 读取双声道音频文件
    input_audio_file = infile
    output_audio_file = outfile

    # 读取音频数据
    sample_rate,audio_data =  wavfile.read(input_audio_file)

    # 小波包去噪的参数设置
    wavelet = 'db14'  
    level = 20    

    # 对每个声道应用小波包去噪
    denoised_audio_data = []
    for channel in range(audio_data.shape[1]):
        channel_data = audio_data[:, channel]
        coeffs = pywt.wavedec(channel_data, wavelet, level=level)
        denoised_coeffs = [pywt.threshold(coeff, 0.1, 'soft') for coeff in coeffs]
        denoised_channel_data = pywt.waverec(denoised_coeffs, wavelet)
        denoised_audio_data.append(denoised_channel_data)

    # 将处理后的数据保存为双声道音频文件
    denoised_audio_data = np.array(denoised_audio_data).T
    wavfile.write(output_audio_file,sample_rate, denoised_audio_data)

    print("音频去噪完成，已保存为", output_audio_file)






# def main(root,pic_dir):
#     wavs = getwavfiles(root)
#
#
#     for wav in wavs:
#         print(wav)
#         print(pic_dir+wav.split("/")[4])
#         func(wav,pic_dir+wav.split("/")[4])
#     return pic_dir



#注意修改路径
# dict = ["zz1","zz2", "zz3", "zz4", "zz5", "zz6", "zz7", "zz0"]
# # dict = ["zz0"]
# for name in dict:
#     after_intercept="data/f/8/zz/" + name
#     print(after_intercept.split("/")[3])
#
#     prepare_for_wavelet="data/wavelet/8/"+after_intercept.split("/")[3]+"/"
#
#     main(after_intercept,prepare_for_wavelet)


path = "/Users/lance/Desktop/Auth/dataset/f/"
for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith(".wav"):
            wav_path = os.path.join(root, file)
            print(wav_path.split("/"))
            print(wav_path)
            prepare_for_wavelet=wav_path.replace("f", "wavelet")
            # prepare_for_wavelet="/Users/lance/Desktop/Auth/dataset/wavelet/" + wav_path.split("/")[3]
            dir_name = os.path.dirname(prepare_for_wavelet)
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
            func(wav_path, prepare_for_wavelet)