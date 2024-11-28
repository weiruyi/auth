# import wave
#
# def get_audio_channels(filename):
#     with wave.open(filename, 'rb') as wf:
#         channels = wf.getnchannels()
#     return channels
#
# # 示例用法
# filename = '../data/my_data/5/ys/ys-5-1.wav'
# channels = get_audio_channels(filename)
# print(f'Audio file "{filename}" has {channels} channels.')


import os
path = "d:/my_data"


for root, dirs, files in os.walk(path):
    # 遍历当前目录下的所有文件
    for file in files:
        print("-----------------------")
        wav = os.path.join(root, file)
        if file.endswith(".wav"):
            os.remove(wav)



# def ensure_directory_exists(directory_path):
#     """
#     确保给定的文件夹路径存在。如果不存在，则创建它。
#     """
#     if not os.path.exists(directory_path):
#         os.makedirs(directory_path)
#         print(f"Directory created at {directory_path}")
#     else:
#         print(f"Directory already exists at {directory_path}")
#
#     # 使用示例
#
#
# folder_path = "d:/2024/3/4"
# ensure_directory_exists(folder_path)
