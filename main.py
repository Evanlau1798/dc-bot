import os
import discord                                #導入 Discord.py
import keep_alive
#import subprocess
client = discord.Client()                     #client 是我們與 Discord 連結的橋樑

token = os.environ['token']
@client.event                                 #調用 event 函式庫
async def on_ready():                         #當機器人完成啟動時
  print(f'目前登入身份：{client.user}')
#  subprocess.run(["python3", "-m", "http.server", "8000"])

print('機器人啟動')

@client.event                                 #調用 event 函式庫
async def on_message(message):                #當有訊息時

    if message.author == client.user:         #排除自己的訊息
        return

    print('偵測到訊息')
    
    if message.content == '嗨':
        await message.channel.send('早安')

    if message.content == '🤔':
        await message.channel.send('🤥')

    if message.content == '🤥':
        await message.channel.send('🤥🤥🤥')

    if message.content.startswith('更改狀態'):
        #切兩刀訊息
        tmp = message.content.split(" ",2)
        #如果分割後串列長度只有1
        if len(tmp) == 1:
            await message.channel.send("輸入錯誤\n應輸入:更改狀態[狀態]")
        else:
            game = discord.Game(tmp[1])
            #discord.Status.<狀態>，可以是online,offline,idle,dnd,invisible
            await client.change_presence(status=discord.Status.online, activity=game)
        
keep_alive.keep_alive()
client.run(token)