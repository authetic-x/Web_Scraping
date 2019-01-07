'''
So boring, let's merge the photos of wechat list into one photo.
'''

import os
import itchat
import math
from PIL import Image

def download():
    itchat.auto_login()
    friends = itchat.get_friends(update=True)
    dirname = './image/'
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    num = 1
    for friend in friends:
        name = str(num) + '.jpg'
        num += 1
        if num > 60:
            break
        img = itchat.get_head_img(userName=friend['UserName'])
        with open(dirname+name, 'wb') as file:
            file.write(img)
            print("Download image %s.jpg" % num)

def merge_images(path):
    print("Merging photos....")

    # 设置每张头像大小
    photo_width = 200
    photo_height = 200

    photo_list = []
    dirName = os.getcwd() + path

    for root, dirs, files in os.walk(dirName):
        for file in files:
            if 'jpg' in file and os.path.getsize(os.path.join(root, file)) > 0:
                photo_list.append(os.path.join(root, file))

    pic_num = len(photo_list)
    column = int(math.sqrt(pic_num))
    row = column
    print("%s * %s" % (column, row))

    # 设置一行最大图片数
    if column > 20:
        column = 20
        row = 20

    toImage = Image.new('RGBA', (photo_width*row, photo_height*column))

    num = 0
    for i in range(0, row):
        for j in range(0, column):
            picture = Image.open(photo_list[num])
            pic = picture.resize((photo_height, photo_width))
            location = (int(j * photo_width), int(i * photo_height))
            toImage.paste(pic, location)
            print("Put image %s" % num)
            num += 1

    print("生成图片大小为：" + str(toImage.size))
    toImage.save('BigPhoto.png')

def main():
    #download()
    merge_images('/image')

main()