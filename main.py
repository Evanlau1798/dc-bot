import os
import discord                                #導入 Discord.py
import keep_alive
import picture
import help
#import time
from datetime import datetime,timezone,timedelta


token = os.environ['token']


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
        tmp = message.content.split("#",2)    #切兩刀訊息
        if len(tmp) == 1:   #如果分割後串列長度只有1
            await message.channel.send("輸入錯誤")
        else:
            tmp = message.content.split(" ",3)

            if 'help' in tmp:   #指令幫助
              await message.channel.send(help())

            if 'status' in tmp:
              game = discord.Game(tmp[2])
              #discord.Status.<狀態>，可以是online,offline,idle,dnd,invisible
              await client.change_presence(status=discord.Status.online, activity=game)
              await message.channel.send(f'已設定我的狀態為{tmp[2]}囉!')
              return
            
            if 'random' in tmp:
              picture.pic_random(tmp[1])
              if 'http' in picture.pic1:
                await message.channel.send(picture.pic1)
              elif 'http' in picture.pic2:
                await message.channel.send(picture.pic1)
                await message.channel.send(picture.pic2)
              elif 'http' in picture.pic3:
                await message.channel.send(picture.pic1)
                await message.channel.send(picture.pic2)
                await message.channel.send(picture.pic3)
    
    if message.content == '嗨':
        await message.channel.send(f'早安啊,{name}君❤️')

    if message.content == '早安':
        await message.channel.send(f'早安啊,{name}君❤️')

    if message.content == '🤔':
        await message.channel.send('🤥')

    if '🤥' in message.content:
        await message.channel.send('🤥🤥🤥')

    if '🎤' in message.content:
        await message.channel.send('https://media.discordapp.net/attachments/903285693655162932/904025706286178334/1.gif')
  
    if '好' in message.content:
      if '好耶' in message.content:
        return
      if '「好」' in message.content:
        return 
      if '還好' in message.content:
        return
      if '你好' in message.content:
        if message.content == '你好':
          await message.channel.send(f'你好啊,{name}君❤️')
          return
      
      await message.channel.send('知道就好☺️')
        

    if 'rick' in message.content:
        await message.channel.send('有人提到rickroll嗎😀?')
        await message.channel.send('<a:yellow_guy:910197305540481056>')
        
keep_alive.keep_alive()
client.run(token)

def help():
  const embed = new Discord.MessageEmbed()