from pydub import AudioSegment
import os

path = "D:\hnu\Auth\dataset\data_cyw"

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
        t1 = 5 * 1000
        t2 = 6.5 * 1000
        # print(wave)
        newAudio = AudioSegment.from_wav(wave)
        total_time = len(newAudio)
        print(total_time)
        total = 0
        while (1):
            total = total+1
            new = newAudio[t1:t2]
            # 分割的音频命名
            new.export(file_root + finger + "-" + pos + "-" + count + "-" + str(total) + '.wav', format="wav")
            t1 += 5 * 1000
            t2 += 5 * 1000
            # 注意修改截止时间t
            t = 0
            if (t2 > total_time):
                break
        print("================spilt complete====================")
