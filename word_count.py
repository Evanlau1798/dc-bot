import sqlite3
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
global db
db = sqlite3.connect("/home/evanlau/dc-bot/word_count.db")

class opencv:
    def cv2ImgAddText(img, text, left, top,color):
        if (isinstance(img, np.ndarray)):
            img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img)
        fontStyle = ImageFont.truetype("/home/evanlau/opencv/Iansui094-Regular.ttf", 35, encoding="utf-8")
        if fontStyle.getsize(text)[0] > 390:
            for i in range(len(list(text))+1,0,-1):
                if fontStyle.getsize(text[:i])[0] < 400:
                    text=str(text[:i]) + "..."
                    break
        draw.text((left, top), text, color, font=fontStyle)
        return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)

class count:
    def word_count(name,id,guild,message):
        msg_list = list(enumerate(message))
        tmp = ""
        num = len(message)
        for i in msg_list:
            if str(i[1]) == "<":
                tmp = i
            if str(i[1]) == ">":
                if tmp[1] == "<":
                    num = num - i[0] + int(tmp[0])
        try:
            for i in db.execute(f'''SELECT Msg_count from Count where ID = {id} and Guild = {guild}'''):
                tmp = i
            if len(tmp) < 0:
                raise ValueError("None")
            num = num + int(tmp[0])
            guild=int(guild)
            db.execute(f'''UPDATE Count set Msg_count = {num}, Name = "{name}" WHERE ID = {id} AND Guild = {guild}''')
            db.commit()
        except:
            print("NewUser")
            x=(str(name),int(id),int(guild),int(num))
            db.execute("INSERT INTO Count VALUES(?,?,?,?)",x)
            db.commit()
        return

    def old_rank_query(name,guild):
        db = sqlite3.connect("/home/evanlau/dc-bot/word_count.db")
        tmp=""
        for i in db.execute(f'''SELECT Name,Msg_count from Count where Guild = {guild} ORDER BY Msg_count DESC LIMIT 10;'''):
            tmp = tmp + str(i[0]) + "，字數為" + str(i[1]) + "\n"
        return tmp
    
    def rank_query(name,guild):
        db = sqlite3.connect("/home/evanlau/dc-bot/word_count.db")
        img = cv2.imread('/home/evanlau/opencv/rank.jpg',-1)
        shader = cv2.imread('/home/evanlau/opencv/rank_shader.jpg',0)
        tmp=[]
        for i in db.execute(f'''SELECT Name,Msg_count from Count where Guild = {guild} ORDER BY Msg_count DESC LIMIT 10;'''):
            tmp.append(i)
        for i,x in zip(tmp,range(19,919,90)):
            img = opencv.cv2ImgAddText(img,str(i[0]),110,x,"black")
            if x in [19,109,199]:
                img = opencv.cv2ImgAddText(img,str(i[1]),540,x,"black")
            else:
                img = opencv.cv2ImgAddText(img,str(i[1]),540,x,"white")
        cv2.imwrite(f'/home/evanlau/dc-bot/rank_tmp/{guild}.jpg', img)
        return tmp