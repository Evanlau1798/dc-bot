import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

def cv2ImgAddText(img, text, left, top,color):
    if (isinstance(img, np.ndarray)):
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    fontStyle = ImageFont.truetype("/home/evanlau/opencv/Iansui094-Regular.ttf", 35, encoding="utf-8")
    draw.text((left, top), text, color, font=fontStyle)
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)


img = cv2.imread('/home/evanlau/dc-bot/rank_tmp/rank.jpg',-1)
print(img.shape)
name=["萌音米花#9717","冬茹#0106","矮木aimu#6738","小祐xiaoyo#7669","星之所在#8848","火耀爆龍#1216","Nobu150#3987","Noar#5476","Evanlau#0857","DC不要亂ban好不好#1077"]
num=[10000,20000,30000,40000,50000,60000,70000,80000,90000,100000]
for i,j,x in zip(name,num,range(19,919,90)):
    img = cv2ImgAddText(img,str(i),110,x,"black")
    img = cv2ImgAddText(img,str(j),540,x,"white")
cv2.imwrite('/home/evanlau/opencv/output.jpg', img)