import os

# 判断文件是否是指定类型
def check_file_type(filename):
    # splitext()  把图片名分成了陈述名 和 后缀名两部分 ('asd', '.jpg')
    ext = os.path.splitext(filename)
    if ext and len(ext) > 1:
        # 把后缀名的 . 去掉
        ext = ext[1].strip('.')
    else:
        return False
    return ext.lower() in ['png', 'jpg', 'jpeg', 'gif']

# 判断文件文件大小
def check_file_size(fileSize):
    return fileSize <= 2*1024*1024