"""
将m4a格式转换成wav格式
"""
import os
import ffmpeg
# path = 'D:/hnu/python/sens/m4aFiles/'
path = 'D:\hnu\Auth\dataset\m4a'
filter = [".m4a"]

def all_path(file_path):
    result = []  # 所有文件
    for maindir, subdir, file_name_list in os.walk(file_path):
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)  # 合并成一个完整路径
            ext = os.path.splitext(apath)[1]  # 获取文件后缀 [0]获取的是除了文件名以外的内容

            if ext in filter:
                result.append(apath)
    return result

filenames = all_path(path)

for filename in filenames:
    filename = str(filename)
    temp = filename.split('.')
    try:
        ffmpeg.input(filename).output(temp[0]+".wav", acodec="pcm_s16le", ar=44100).run(overwrite_output=True)
        print(f"转换成功")
        os.remove(filename)  # 删除源文件
    except Exception as e:
        print(f"转换失败: {e}")


