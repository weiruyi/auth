from pydub import AudioSegment
import os

#注意修改路径，此处应该输入录制的原始长音频,每隔5s分割一次，得到一个2s的音频
# dict = ["zz1","zz2", "zz3", "zz4", "zz5", "zz6", "zz7", "zz8", "zz9"]
# dict = ["pos3_yz1"]
# for name in dict:
#     wave="../data/pos_data/" + name + ".wav"
#     file_root="data/split/pos/pos3/yz/"
#     t1 = 2 * 1000
#     t2 = 4 * 1000
#     print(wave)
#     newAudio = AudioSegment.from_wav(wave)
#     total_time = len(newAudio)
#     print(total_time)
#     while(1):
#         new=newAudio[t1:t2]
#         #分割的音频命名
#         new.export(file_root + str("U")+str(t1/1000)+str(t2/1000)+'.wav', format="wav")
#         t1+=5*1000
#         t2+=5*1000
#         #注意修改截止时间t
#         t=0
#         if(t2>total_time):
#             break

path = "D:\hnu\Auth\dataset\data_cyw"


# root: 当前目录下所有文件夹
#
for root, dirs, files in os.walk(path):
    # 遍历当前目录下的所有文件
    for file in files:
        if(file.startswith(".")):
            continue
        wave = os.path.join(root, file)
        print("=========================================")
        print(wave)
        filename = os.path.basename(wave)
        finger = filename.split('-')[0]
        pos = filename.split('-')[1]
        count = filename.split('-')[2].split('.')[0]
        file_root = "D:\hnu\Auth\dataset\split_cyw/" + pos + "/" + finger + "/" + count + "/"
        if not os.path.exists(file_root):
            os.makedirs(file_root)
        t1 = 1.9 * 1000
        t2 = 4 * 1000
        print(wave)
        newAudio = AudioSegment.from_wav(wave)
        total_time = len(newAudio)
        print(total_time)
        total = 0
        while (1):
            new = newAudio[t1:t2]
            # 分割的音频命名
            # new.export(file_root + str("U") + str(t1 / 1000) + str(t2 / 1000) + '.wav', format="wav")
            new.export(file_root + finger + "-" + pos + "-" + count + "-" + str(total) + '.wav', format="wav")
            total += 1
            t1 += 5 * 1000
            t2 += 5 * 1000
            # 注意修改截止时间t
            t = 0
            if (t2 > total_time):
                break
        print("================spilt complete====================")
