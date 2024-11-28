import librosa
import matplotlib.pyplot as plt
import librosa.display
import numpy as np
import wave
import datetime
import os

from scipy.io import wavfile

file_path = 'data/split/my/5/ys/ys0U2.04.0.wav'
# class_name = ["cyw-1", "gjh-1", "gjh-2", "cyw-2", "cyw-3"]
# file_dict = ["cyw-1", "gjh-1", "gjh-2", "cyw-2", "cyw-3"]
# 打印所有文件名
n_fft = 1024
hop_length = 32
y, sr = librosa.load(file_path, sr=None)
print(y)
# 计算分割时间点
total_duration = len(y) / sr  # 音频总时长
print(total_duration)

y_normalized = y / np.max(np.abs(y))
current_time = datetime.datetime.now()


samplerate, data = wavfile.read(file_path)
print(data)
# 计算音频时长
duration = len(data) / samplerate

# 创建时间数组，用于绘制波形图
time = np.arange(0, duration, 1 / samplerate)

# 绘制波形图
plt.figure(figsize=(10, 4))
plt.plot(time, data[:, 0], label='Left Channel')  # 左声道数据
plt.plot(time, data[:, 1], label='Right Channel')  # 右声道数据
plt.xlabel('Time (seconds)')
plt.ylabel('Amplitude')
plt.title('Audio Waveform')
plt.legend()
plt.grid()
plt.show()
print(np.max(data))
# librosa.display.waveshow(y=data, sr=sr, color="blue")
# plt.title(f'Waveform')
# plt.xlabel('Time (s)')
# plt.ylabel('Amplitude')
# plt.show()

# 计算 STFT（短时傅里叶变换）
D = librosa.stft(y_normalized, n_fft=n_fft, hop_length=hop_length, window='hann')
x = np.abs(D)
plt.figure(figsize=(10, 4))
librosa.display.specshow(librosa.amplitude_to_db(x, ref=np.max), sr=sr, n_fft=n_fft, hop_length=hop_length, x_axis='time', y_axis='mel', cmap="coolwarm")
plt.colorbar(shrink=0.7)
plt.title(f'Spectrogram')
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
plt.show()
plt.close()  # 关闭当前图形，防止内存泄漏

# # 计算梅尔谱图
mel_spec = librosa.feature.melspectrogram(y=y_normalized, sr=sr, n_fft=n_fft, hop_length=hop_length)
log_mel_spec = librosa.power_to_db(mel_spec, ref=np.max)

# 绘制梅尔谱图
plt.figure(figsize=(10, 4))
librosa.display.specshow(log_mel_spec, sr=sr, n_fft=n_fft, hop_length=hop_length, x_axis='time', y_axis='mel', cmap="coolwarm")
# plt.colorbar(format='%+2.0f dB')
# plt.colorbar(shrink=0.7)
plt.title(f'Mel Spectrogram')
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
plt.show()
plt.close()  # 关闭当前图形，防止内存泄漏

