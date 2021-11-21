import os
import discord                                #導入 Discord.py
import keep_alive
import picture
import replit
#import readme
#import time
from datetime import datetime,timezone,timedelta


token = os.environ['token']
replit.clear()


client = discord.Client()                     #client連結Discord

@client.event                                 #調用 event 函式庫
async def on_ready():                         #當機器人完成啟動時
  print(f'目前登入身份：{client.user}')

print('機器人啟動')


@client.event                                 #調用 event 函式庫
async def on_message(message):                #當有訊息時
  dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
  dt2 = dt1.astimezone(timezone(timedelta(hours=8))) # 轉換台灣時區
  ticks = dt2.strftime("%Y-%m-%d %H:%M:%S")
    
  if message.author == client.user:         #排除自己的訊息
    return

  name = message.author.mention 
  print('於',ticks,f'偵測到訊息:{message.content}')

  if message.content.startswith('#'):       #指令判斷
    #print('偵測到指令')
    tmp = message.content.split("#",2)    #切兩刀訊息
    if len(tmp) == 1:   #如果分割後串列長度只有1
      await message.channel.send("我不知道您在說什麼誒...\n可以請您再說一次嗎?")
      await message.channel.send('https://i.imgur.com/V1P5kV2.jpg')
      return
    else:
      tmp = message.content.split(" ",2)

      if len(tmp[0]) > 1:
        await message.channel.send("指令錯誤...\n可以請您再說一次嗎?")
        await message.channel.send('https://i.imgur.com/V1P5kV2.jpg')
        return
        
#      if ['help','status','update','picture','random'] in tmp[1]:
      if 'help' in tmp[1]:   #指令幫助
        path = 'readme.md'
        f = open(path, 'r')
        await message.channel.send(f.read())
        f.close()
        return

      if 'status' in tmp[1]:
        game = discord.Game(tmp[2])
        #discord.Status.<狀態>，可以是online,offline,idle,dnd,invisible
        await client.change_presence(status=discord.Status.online, activity=game)
        await message.channel.send(f'已設定我的狀態為{tmp[2]}囉!')
        return

      if 'update' in tmp[1]:
        update = "V1.1 預計更新：\n可指定角色的隨機圖片\n增加日常對話的句子\n優化指令判斷"
        await message.channel.send(update)
        return

#      print(tmp[1])

      if 'random' in tmp[1] or 'picture' in tmp[1]:
#        print(tmp)
        tmp = message.content.split(" ",3)
        try:
#          print(f'{tmp[1]}')
          picture.locate = 1
          if 'random' == tmp[1]:
#            print('圖片random')
            picture.pic_random(tmp[1])
          if 'picture' == tmp[1]:
#            print('圖片picture')
            picture.pic_random(tmp[2])
#            print(f'locate={picture.locate}')
          if picture.locate == 1:
            if 'http' in picture.pic1:
              await message.channel.send(picture.pic1)
            elif 'http' in picture.pic2:
              await message.channel.send(picture.pic1)
              await message.channel.send(picture.pic2)
            elif 'http' in picture.pic3:
              await message.channel.send(picture.pic1)
              await message.channel.send(picture.pic2)
              await message.channel.send(picture.pic3)
          if picture.locate == 0:
            print('找不到圖片')
            await message.channel.send('您指定的這位老婆，我不認識她誒...😰')
            await message.channel.send('https://i.imgur.com/nbs4CXK.jpg')
            return
        except:
          await message.channel.send("指令錯誤...\n可以請您再說一次嗎?")
          await message.channel.send('https://i.imgur.com/V1P5kV2.jpg')
          return

      else:
        await message.channel.send("指令錯誤...\n可以請您再說一次嗎?")
        await message.channel.send('https://i.imgur.com/V1P5kV2.jpg')
        return

  if message.content == '嗨':
    await message.channel.send(f'早安啊,{name}君❤️')
    return

  if message.content == '早安':
    await message.channel.send(f'早安啊,{name}君❤️')
    return

  if message.content == '🤔':
    await message.channel.send('🤥')
    return

  if '🤥' in message.content:
    await message.channel.send('🤥🤥🤥')
    return

  if '🎤' in message.content:
    await message.channel.send('https://media.discordapp.net/attachments/903285693655162932/904025706286178334/1.gif')
    return
  
  if '好' in message.content:
    if '好耶' in message.content:
      return
    if '「好」' in message.content:
      return 
    if '還好' in message.content:
      return
    if (len(message.content) > 7 ):
      return
    if '你好' in message.content:
      if message.content == '你好':
        await message.channel.send(f'你好啊,{name}君❤️')
        return
      await message.channel.send('知道就好😌')
      return
        
  if 'rick' in message.content:
        await message.channel.send('有人提到rickroll嗎😀?')
        await message.channel.send('<a:yellow_guy:910197305540481056>')
        return
        
keep_alive.keep_alive()
client.run(token)