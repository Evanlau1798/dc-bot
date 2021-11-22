import os
import discord                                #導入 Discord.py
import keep_alive
import picture
import replit
#import readme
#import time
from datetime import datetime,timezone,timedelta
ver = '姬宮真步#4176  discord bot  V1.1.1 beta測試版'


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
    tmp = message.content.split("#",2)    #切兩刀訊息
    if len(tmp) == 1:   #如果分割後串列長度只有1
      await message.reply("我不知道您在說什麼誒...\n可以請您再說一次嗎?")
      await message.channel.send('https://i.imgur.com/V1P5kV2.jpg')
      return
    else:
      tmp = message.content.split(" ",2)

      if len(tmp[0]) > 1:
        await message.reply("指令錯誤...\n可以請您再說一次嗎?")
        await message.channel.send('https://i.imgur.com/V1P5kV2.jpg')
        return
        
      if 'help' in tmp[1]:   #指令幫助
        embed=discord.Embed(title="機器人指令使用說明", description="讓您了解如何活用我的力量!", color=0xd98d91)
        embed.set_author(name="姬宮真步#4176",icon_url="https://cdn.discordapp.com/app-icons/909796683418832956/13e44ec11c3a69d1bd042e3c41e5e320.png?size=128")
        embed.set_image(url="https://i.imgur.com/4P71nBG.jpg")
        embed.add_field(name="** **", value="** **", inline=False)
        embed.add_field(name="# help", value="開啟幫助列表", inline=True)
        embed.add_field(name="# random", value="直接打出指令，可以召喚香圖🤩\n(圖庫由 優衣 linebot 機器人提供)", inline=True)
        embed.add_field(name="# picture", value="用法: # picture [狀態]\n可以召喚指定角色的香圖\n(圖庫依然由 優衣 linebot 機器人提供)", inline=True)
        embed.add_field(name="** **", value="** **", inline=False)
        embed.add_field(name="額外指令", value="** **", inline=False)
        embed.add_field(name="文字中只要包含rick", value="就可以呼叫👞🎙️🎵", inline=True)
        embed.add_field(name="說[嗨][早安]", value="讓我跟你說早安", inline=True)
        embed.add_field(name="說[你好]", value="讓我跟你說好", inline=True)
        embed.add_field(name="好", value="好佳在你知道", inline=False)
        embed.add_field(name="** **", value="就醬", inline=True)
        embed.set_footer(text=ver)
        await message.channel.send(embed=embed)
        return

      if '狀態' in tmp[1]:
        game = discord.Game(tmp[2])
        #discord.Status.<狀態>，可以是online,offline,idle,dnd,invisible
        await client.change_presence(status=discord.Status.online, activity=game)
        await message.channel.send(f'已設定我的狀態為{tmp[2]}囉!')
        return

      if 'update' in tmp[1]:
        update = "V1.1 預計更新：\n可指定角色的隨機圖片\n增加日常對話的句子\n優化指令判斷"
        await message.channel.send(update)
        return


      if 'random' in tmp[1] or 'picture' in tmp[1]:
        tmp = message.content.split(" ",3)
        try:
          picture.locate = 1
          if 'random' == tmp[1]:
            picture.pic_random(tmp[1])
          if 'picture' == tmp[1]:
            picture.pic_random(tmp[2])
          embed=discord.Embed(color=0xd98d91)
          if picture.locate == 1:
            if 'http' in picture.pic1:
              embed.set_image(url=picture.pic1)
              await message.channel.send(embed=embed)
            elif 'http' in picture.pic2:
              embed.set_author(name=picture.pic1)
              embed.set_image(url=picture.pic2)
              await message.channel.send(embed=embed)
            elif 'http' in picture.pic3:
              embed.set_author(name=picture.pic1)
              embed.set_image(url=picture.pic2)
              await message.channel.send(embed=embed)
              embed.set_image(url=picture.pic3)
              await message.channel.send(embed=embed)
          if picture.locate == 0:
            await message.reply('您指定的這位老婆，我不認識她誒...😰')
            await message.channel.send('https://i.imgur.com/nbs4CXK.jpg')
            return
        except:
          await message.reply("指令錯誤...\n可以請您再說一次嗎?")
          await message.channel.send('https://i.imgur.com/V1P5kV2.jpg')
          return

      else:
        await message.reply("指令錯誤...\n可以請您再說一次嗎?")
        await message.channel.send('https://i.imgur.com/V1P5kV2.jpg')
        return

  if message.content == '嗨':
    await message.reply(f'早安啊,{name}君❤️',mention_author=True)
    return

  if message.content == '早安':
    await message.reply(f'早安啊,{name}君❤️',mention_author=True)
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
        await message.reply(f'你好啊,{name}君❤️',mention_author=True)
        return
    await message.reply('知道就好😌', mention_author=True)
    return
        
  if 'rick' in message.content:
        await message.channel.send('有人提到rickroll嗎😀?')
        await message.channel.send('<a:yellow_guy:910197305540481056>')
        return
        
keep_alive.keep_alive()
client.run(token)