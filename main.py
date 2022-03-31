from bs4 import BeautifulSoup
import os
import discord
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option
from discord_slash.utils import manage_components
from discord_slash.model import ButtonStyle
from discord.ext import tasks, commands
import webserver
import asyncio
import pixivpy3
import picture
import requests
from googletrans import Translator
import conversation
import help
from itertools import cycle
import random
from youtube_dl import YoutubeDL
from dotenv import load_dotenv
import keep_alive
import sqlite3
import subprocess
import time
from word_count import count,opencv

load_dotenv()
players = {}
translator = Translator()
bot = discord.Client(intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)
token = 'OTA5Nzk2NjgzNDE4ODMyOTU2.YZJgMA.AlQ8-N21uVYsVwqANPvi2fYyBBk'
guild_ids = [887172437903560784]
_REFRESH_TOKEN = 'eiDaafkFze2rPaw-X2yaOXdiGpwpNpwvrIr_1jVTQww'
api_key = '576bfa89b78416c5bb19d6bc92f97a1e'
base_url = "http://api.openweathermap.org/data/2.5/weather?"
headers = {'Referer': 'https://www.pixiv.net/'}
verify = False


status = cycle(['超異域公主連結☆Re:Dive'])


@tasks.loop(seconds=5)
async def change_status():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(next(status)))


@slash.slash(name="ping", description="測試機器人延遲")
async def ping(message):
    conversation.print_cmd(message, 'test')
    await message.send(f"延遲:{round(bot.latency*1000)}ms")


@slash.slash(name="help", description="查看可用指令")  # , guild_ids=guild_ids)
async def _help(message):
    conversation.print_cmd(message, 'help')
    embed = discord.Embed(
        title="機器人指令使用說明", description="讓您了解如何活用我的力量!", color=0xd98d91)
    file = discord.File("/home/evanlau/dc-bot/introduction.jpg", filename="introduction.jpg")
    embed = help.help(embed)
    await message.send(file=file, embed=embed)


# , guild_ids=guild_ids)
@slash.slash(name="trans", description="翻譯任何語言至繁體中文(吧?")
async def _trans(message, *, text):
    conversation.print_cmd(message, 'trans')
    try:
        output = translator.translate(text, dest='zh-tw').text
        await message.send(f'翻譯：{output}')
        return
    except:
        await message.send("指令錯誤...\n可以請您再說一次嗎?\n指令用法為：# trans [欲翻譯的文字或句子]")
        await message.send('https://i.imgur.com/V1P5kV2.jpg')


@slash.slash(name="weather", description="查詢指定地區")
async def _weather(message, *, city):
    conversation.print_cmd(message, 'weather')
    city_name = city
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()
    if x["cod"] != "404":
        y = x["main"]
        current_temperature = y["temp"]
        current_temperature_celsiuis = str(round(current_temperature - 273.15))
        current_pressure = y["pressure"]
        current_humidity = y["humidity"]
        z = x["weather"]
        city_name = translator.translate(city, dest='zh-tw').text
        embed = discord.Embed(title=f"這是在 {city_name} 的天氣", color=0xd98d91)
        weather_description = translator.translate(
            z[0]["description"], dest='zh-tw').text
        embed.add_field(
            name="天氣狀況", value=f"**{weather_description}**", inline=False)
        embed.add_field(
            name="溫度（°C）", value=f"**{current_temperature_celsiuis}°C**", inline=False)
        embed.add_field(
            name="濕度(%)", value=f"**{current_humidity}%**", inline=False)
        embed.add_field(name="大氣壓力(hPa)",
                        value=f"**{current_pressure}hPa**", inline=False)
        embed.set_thumbnail(url="https://i.ibb.co/CMrsxdX/weather.png")
        embed.set_footer(text=f"要求自：{message.author.name}")
        await message.send(embed=embed)
    else:
        await message.send("我找不到這個城市喔😨")


@slash.slash(name="random", description="隨機香香圖片😋")
async def _random(message):
    conversation.print_cmd(message, 'random')
    picture.locate = 1
    picture.pic_random('random')
    embed = discord.Embed(color=0xd98d91)
    if picture.locate == 1:
        if 'http' in picture.pic1:
            embed.set_image(url=picture.pic1)
            await message.send(embed=embed)
        elif 'http' in picture.pic2:
            embed.set_author(name=picture.pic1)
            embed.set_image(url=picture.pic2)
            await message.send(embed=embed)
        elif 'http' in picture.pic3:
            embed.set_author(name=picture.pic1)
            embed.set_image(url=picture.pic2)
            await message.send(embed=embed)
            embed.set_image(url=picture.pic3)
            await message.send(embed=embed)
        if picture.locate == 0:
            await message.send('您指定的這位老婆，我不認識她誒...😰')
            await message.send('https://i.imgur.com/nbs4CXK.jpg')


@slash.slash(name="picture", description="搜尋指定角色的圖片😋")
async def _picture(message, *, text):
    conversation.print_cmd(message, 'picture')
    picture.locate = 1
    picture.pic_random(text)
    embed = discord.Embed(color=0xd98d91)
    if picture.locate == 1:
        if 'http' in picture.pic1:
            embed.set_image(url=picture.pic1)
            await message.send(embed=embed)
        elif 'http' in picture.pic2:
            embed.set_author(name=picture.pic1)
            embed.set_image(url=picture.pic2)
            await message.send(embed=embed)
        elif 'http' in picture.pic3:
            embed.set_author(name=picture.pic1)
            embed.set_image(url=picture.pic2)
            await message.send(embed=embed)
            embed.set_image(url=picture.pic3)
            await message.send(embed=embed)
        if picture.locate == 0:
            await message.send('您指定的這位，我不認識她誒...😰')
            await message.send('https://i.imgur.com/nbs4CXK.jpg')


@slash.slash(name="pixiv", description="在pixiv上搜尋指定關鍵字的圖片", options=[
    create_option(
        name="text",
        description="以此關鍵字在pixiv上搜尋",
        option_type=3,
        required=True
    ),
    create_option(
        name="num",
        description="搜尋後的結果順位",
        option_type=4,
        required=True
    )
])
async def pixiv(message, text, num):
    conversation.print_cmd(message, 'pixiv')
    aapi = pixivpy3.AppPixivAPI()
    search = text
    if num:
        num = 1
    try:
        if int(num) > 30:
            await message.send('最多只能查詢30張圖片喔')
            return
        elif int(num) > 1:
            tmp = int(num) - 1
        elif int(num) == 1:
            tmp = 0
    except:
        tmp = 0
    try:
        aapi.auth(refresh_token=_REFRESH_TOKEN)
        json_result = aapi.search_illust(
            search, search_target='partial_match_for_tags')
        illust = json_result.illusts[tmp]
    except:
        await message.send('pixiv上沒有關於這個關鍵字的圖片喔')
        return
    url = illust.image_urls['large']
    url = url.split('https://i.pximg.net', 2)
    #url = 'https://i.pixiv.cat' + url[1]
    url = 'https://pixiv.runrab.workers.dev' + url[1]
    embed = discord.Embed(color=0xd98d91)
    embed.set_image(url=url)
    embed.set_author(name=illust.title)
    await message.send(embed=embed)


@slash.slash(name="create", description="創建語音頻道")
async def create(message, *, name, num):
    conversation.print_cmd(message, 'create')
    voice = message.guild.voice_channels
    c = open('/home/evanlau/dc-bot/channelID/T_ChannelID.txt', 'r')
    temp = eval(c.read())
    if str(message.channel.id) in str(temp):
        print('相符')
    else:
        await message.send('這個頻道無法使用此指令喔')
        return
    c.close()
    for i in voice[:len(voice)]:
        if str(i) == str(name):
            await message.send('此頻道已存在')
            return
    await message.guild.create_voice_channel(name=name, overwrites=None, category=message.channel.category, reason=None, user_limit=num)
    await message.send('頻道創建成功!')
    voice = message.guild.voice_channels
    for i in voice:
        if str(name) == str(i):
            f = open('/home/evanlau/dc-bot/channelID/V_ChannelID.txt', 'r')
            temp = eval(f.read())
            temp.append(str(i.id))
            f.close()
            t = open('/home/evanlau/dc-bot/channelID/V_ChannelID.txt', 'w')
            # print(temp)
            t.write(str(temp))
            t.close()


@slash.slash(name="vcset", description="設定指定的頻道為動態語音創建用文字頻道")
async def vcset(message):
    conversation.print_cmd(message, 'vcset')
    if message.author.guild_permissions.manage_channels or str(message.author.id) == '540134212217602050':
        id = str(message.channel.id)
        output = ""
        try:
            for i in conn.execute(f'''SELECT guild,name,id,create_by from T_ChannelID where id = "{id}"'''):
                output = output+str(i)
            print(output)
            if len(output) != 0:
                raise ValueError("已登記")
            else:
                print("搜尋無結果")
        except:
            await message.send('此頻道已登記')
            return
        channel = bot.get_channel(int(id))
        if channel != None:
            new_guild = message.guild.id
            new_name = message.channel.name
            new_id = message.channel.id
            new_create_by = message.author.id
            x = (new_guild, new_name, new_id, new_create_by)
            conn.execute('''insert into T_ChannelID values(?,?,?,?)''', x)
            conn.commit()
            await message.send(f'已設定{channel.name}為動態語音產生頻道')
            return
        else:
            await message.send('未找到此頻道')
            return
    else:
        await message.send('您沒有權限執行此操作')
        return


@slash.slash(name="vcdel", description="取消動態語音創建用文字頻道")
async def vcdel(message):
    conversation.print_cmd(message, 'vcdel')
    id = str(message.channel.id)
    if message.author.guild_permissions.manage_channels or str(message.author.id) == '540134212217602050':
        c = open('/home/evanlau/dc-bot/channelID/T_ChannelID.txt', 'r')
        temp = eval(c.read())
        c.close()
        if str(id) in str(id):
            channel = bot.get_channel(int(id))
            # print(channel)
            if channel != None:
                f = open('/home/evanlau/dc-bot/channelID/T_ChannelID.txt', 'w')
                temp.remove(id)
                f.write(str(temp))
                f.close()
                await message.send(f'刪除{channel.name}成功')
                return
            else:
                await message.send('未找到此頻道')
                return
    else:
        await message.send('您沒有權限執行此操作')
        return


@slash.slash(name="dvcset", description="設定指定的語音頻道為動態語音創建用語音頻道")
async def dvcset(message, *, id):
    conversation.print_cmd(message, 'dvcset')
    if message.author.guild_permissions.manage_channels or str(message.author.id) == '540134212217602050':
        c = open('/home/evanlau/dc-bot/channelID/DV_ChannelID.txt', 'r')
        temp = eval(c.read())
        c.close()
        if str(id) in str(temp):
            await message.send('此頻道已登記')
            return
        channel = bot.get_channel(int(id))
        if channel != None:
            f = open('/home/evanlau/dc-bot/channelID/DV_ChannelID.txt', 'w')
            temp.append(str(id))
            f.write(str(temp))
            f.close()
            await message.send(f'已設定{channel.name}為動態語音產生頻道')
            return
        else:
            await message.send('未找到此頻道')
            return
    else:
        await message.send('您沒有權限執行此操作')
        return


@slash.slash(name="pool", description="有問題就問問我吧！我可以幫你解答的😆")
async def pool(message, *, question):
    name = str(message.author).split('#')
    conversation.print_cmd(message, 'pool')
    conv = ['一定的', '沒有異議', '你會依靠他的', '好喔',
            '你不會想知道的', '基於我的看法：不要！', '不要。', '你要確定誒',
            '不好說', '等等再問我吧', '好問題，我需要思考一下', '我現在沒辦法決定🤔']
    await message.send(f'對於{name[0]}的問題:\n{question}\n我的回答是：{random.choice(conv)}')


@slash.slash(name="leave", description="讓機器人離開頻道")
async def leave(message):
    voice = discord.utils.get(bot.voice_clients, guild=message.guild)
    if voice.is_connected():
        await voice.disconnect()
    await message.send(f'斷開連接成功')


@slash.slash(name="play", description="從Youtube撥放音樂!")
async def play(message, *, url):
    url = str(url)
    channel = message.author.voice.channel
    voice = discord.utils.get(bot.voice_clients, guild=message.guild)
    if voice == None:
        await channel.connect()
        voice = discord.utils.get(bot.voice_clients, guild=message.guild)
        print(message.voice_client)
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
    URL = info['url']
    await message.send('開始撥放')
    voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
    voice.is_playing()


@slash.slash(name="resume", description="繼續撥放音樂")
async def resume(message):
    voice = discord.utils.get(bot.voice_clients, guild=message.guild)
    if not voice == None:
        voice.resume()
        await message.send('正在繼續撥放...')


@slash.slash(name="pause", description="暫停音樂")
async def pause(message):
    voice = discord.utils.get(bot.voice_clients, guild=message.guild)
    if not voice == None:
        voice.pause()
        await message.send('音樂已暫停')


@slash.slash(name="stop", description="停止撥放音樂")
async def stop(message):
    voice = discord.utils.get(bot.voice_clients, guild=message.guild)
    if not voice == None:
        voice.stop()
        await message.send('音樂已停止')


@slash.slash(name="n", description="開車囉!", options=[
    create_option(
        name="number",
        description="以此數字搜索指定漫畫(0為隨機)",
        option_type=3,
        required=True
    )])
async def _n(message, number):
    if message.channel.is_nsfw() == True or str(message.author.id) == '540134212217602050':
        sended_message = await message.reply('查詢中...')
        black_list=[228922]
        while True:
            if int(number) in black_list:
                await sended_message.edit(content="不受理此號碼")
                return
            if int(number) == 0:
                number = str(random.randint(1, 394241))
            else:
                number = str(number)
            url = "https://nhentai.net/g/" + number
            requests.get(url, headers={'Connection': 'close'})
            res = requests.post(url, headers={
                                'Connection': 'close', "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"})
            if res.status_code == 404:
                if int(number) == 0:
                    continue
                else:
                    await sended_message.edit(content="查詢錯誤，此漫畫不存在。")
                    return
            Soup = BeautifulSoup(res.text, 'html.parser')
            title = Soup.title.string.replace(
                " » nhentai: hentai doujinshi and manga", "")
            image = Soup.find("meta", itemprop="image").get('content')
            print(message)
            print(title, image, url)
            embed = discord.Embed(title=title, color=0xd98d91)
            embed.set_image(url=image)
            embed.add_field(name="漫畫連結", value=url, inline=False)
            await sended_message.edit(embed=embed, content="")
            return
    else:
        await message.send("不可以色色!")


@slash.slash(name="roll", description="擲骰子")
async def roll(message):
    await message.send(f"您擲到了{random.choice(range(0,9))}")

@slash.slash(name="rank", description="查看本伺服器總字數排名")
async def rank(message):
    conversation.print_cmd(message, 'rank')
    name=str(message.author)
    guild=int(message.guild.id)
    tmp = count.rank_query(name, guild)
    file = discord.File(f"/home/evanlau/dc-bot/rank_tmp/{str(guild)}.jpg", filename="rank.jpg")
    if len(tmp) != 0:
        embed = discord.Embed(title=f"{str(message.guild)}的伺服器排名",color=0xd98d91)
        embed.set_image(url=f"attachment://rank.jpg")
        await message.reply(embed=embed, file=file)
        os.system(f"rm /home/evanlau/dc-bot/rank_tmp/{str(guild)}.jpg")
        return
    else:
        await message.reply("這裡居然沒有人講過話...")
        return
  

@slash.slash(name="startmcserver", description="啟動亞太嘎麥塊伺服器", guild_ids=[628525243543060480])
async def startmcserver(message):
    sended_message = await message.send('檢測伺服器是否可運行...')
    try:
        subprocess.check_output(
            'nc -vz mcserver.duacodie.com 41760', shell=True)
        output = subprocess.check_output('screen -ls', shell=True)
        print(output)
        if ".mcserver" in str(output):
            await sended_message.edit(content='伺服器已正在運行，請嘗試重新連接伺服器')
            return
        await sended_message.edit(content='端口已被占用\n請確認伺服器為尚未啟動狀態後瘋狂標記<@!540134212217602050>叫他出來')
        return
    except:
        await sended_message.edit(content='端口未被占用，啟動伺服器中...')
        try:
            output = subprocess.check_output(
                'screen -Sdm mcserver bash -c "cd mcserver; ./run_server.sh;"', shell=True)
            print(output)
            time.sleep(1)
            await sended_message.edit(content='伺服器成功執行啟動動作，請稍等伺服器啟動完成')
        except:
            await sended_message.edit(content='伺服器啟動失敗\n請瘋狂標記<@!540134212217602050>叫他出來')
        return


@slash.slash(name="stopmcserver", description="關閉亞太嘎麥塊伺服器", guild_ids=[628525243543060480])
async def stopmcserver(message):
    sended_message = await message.send('檢測伺服器是否正在運行...')
    output = subprocess.check_output('screen -ls', shell=True)
    if ".mcserver" in str(output):
        try:
            subprocess.check_output('screen -X -S mcserver quit', shell=True)
            await sended_message.edit(content='伺服器關閉成功')
            return
        except:
            try:
                output = subprocess.check_output(
                    'nc -vz mcserver.duacodie.com 41760', shell=True)
                print(output)
                await sended_message.edit(content='端口已被占用\n請瘋狂標記<@!540134212217602050>叫他出來')
                return
            except:
                await sended_message.edit(content='伺服器尚未啟動\n如要啟動伺服器請輸入/startmcserver')
    else:
        await sended_message.edit(content='伺服器未在運行中')


@bot.event
async def on_message(message):
    name = message.author.mention
    conversation.print_ctx(message)
    if message.author.bot == True:  # 排除自己的訊息
        return
    if message.content.startswith('#'):  # 個人指令判斷
        tmp = message.content.split(" ")
        if 'send' == tmp[1]:
            if str(message.author.id) == '540134212217602050':
                tmp = message.content.split("# send ",)
                await message.delete()
                await message.channel.send(tmp[1])
                return
            else:
                await message.reply(f'<@!540134212217602050>，<@{str(message.author.id)}>在亂玩指令')
                return

        if 'vcconfig' == tmp[1]:
            if str(message.author.id) == '540134212217602050':
                c = open('/home/evanlau/dc-bot/channelID/T_ChannelID', 'r')
                f = open('/home/evanlau/dc-bot/channelID/V_ChannelID', 'r')
                temp1 = eval(c.read())
                temp2 = eval(f.read())
                c.close()
                f.close()
                config = ""
                for i in temp1:
                    channel = bot.get_channel(int(i))
                    config = str(config) + str(channel) + '\n'
                config = config + '以上為文字頻道\n\n'
                for i in temp2:
                    channel = bot.get_channel(int(i))
                    config = str(config) + str(channel) + '\n'
                config = str(config) + '以上為語音頻道\n'
                await message.reply(config)
                return

            else:
                await message.reply(f'<@!540134212217602050>，<@{str(message.author.id)}>在亂玩指令')
                return

        if 'public' == tmp[1]:
            if str(message.author.id) == '540134212217602050':
                tmp = message.content.split("# public ",)
                c = open('channelID/T_ChannelID', 'r')
                temp = eval(c.read())
                c.close()
                progress = 0
                for i in temp:
                    progress = progress + 1
                    channel = bot.get_channel(int(i))
                    await channel.send(str(tmp[1]))
                    await message.channel.send(f"已在{channel}發送公告，進度為{progress}/{len(temp)}")
                return
            else:
                await message.reply(f'<@!540134212217602050>，<@{str(message.author.id)}>在亂玩指令')
                return

        if 'PSend' == tmp[1]:
            if str(message.author.id) == '540134212217602050':
                tmp = message.content.split(" ")
                channel = bot.get_channel(int(tmp[2]))
                print(channel.name)
                await channel.send(str(tmp[3]))
                return
            else:
                await message.reply(f'<@!540134212217602050>，<@{str(message.author.id)}>在亂玩指令')
                return

        if 'check' == tmp[1]:
            activeservers = bot.guilds
            for i in activeservers:
                await message.channel.send(i)
            print(activeservers)
            return

        if 'join' == tmp[1]:
            print('join')
            channel = message.author.voice.channel
            await channel.connect()
            return

        if 'leave' == tmp[1]:
            await channel.voice_client.disconnect()
            return

        if 'announcement' == tmp[1]:
            if str(message.author.id) == '540134212217602050':
                guilds = bot.guilds
                for i in guilds:
                    current_guild = bot.get_guild(int(i.id))
                    print(current_guild.owner_id, current_guild.owner)
                    dm = await i.owner.create_dm()
                    await dm.send(tmp[2])
                return
            else:
                await message.reply(f'<@!540134212217602050>，<@{str(message.author.id)}>在亂玩指令')
                return

        if 'bot_leave' == tmp[1]:
            guild = bot.get_guild(int(tmp[2]))
            print(guild)
            print(await guild.leave())
            return

        if 'sqladd' == tmp[1]:
            print("testing addsql...")
            db = sqlite3.connect("/home/evanlau/dc-bot/word_count.db")
            num = 0
            guild=message.guild.id
            for i in db.execute(f'''SELECT Msg_count from Count where ID = 540134212217602050 and Guild = {guild}'''):
                num = int(i[0])
                print(i[0],num)
            num = num + int(tmp[2])
            guild=int(guild)
            db.execute(f'''UPDATE Count set Msg_count = {num} WHERE ID = 540134212217602050 AND Guild = {guild}''')
            db.commit()
            await message.delete()
            return

        if 'sqldel' == tmp[1]:
            db = sqlite3.connect("/home/evanlau/dc-bot/word_count.db")
            num = 0
            guild=message.guild.id
            for i in db.execute(f'''SELECT Msg_count from Count where ID = 540134212217602050 and Guild = {guild}'''):
                num = int(i[0])
                print(i[0],num)
            num = num - int(tmp[2])
            guild=int(guild)
            db.execute(f'''UPDATE Count set Msg_count = {num} WHERE ID = 540134212217602050 AND Guild = {guild}''')
            db.commit()
            await message.delete()
            return

        if 'sqlprint' == tmp[1]:
            output = ""
            print("testing printing sql...")
            try:
                for i in conn.execute(f'''SELECT guild,name,id,create_by from T_ChannelID where {tmp[2]} = "{tmp[3]}"'''):
                    output = output+str(i)
                print(output)
            except:
                output = "搜尋無結果"
            print(f"內容為:{output}")
            await message.reply(output)
            return

        if 'WordC' in tmp[1]:
            db = sqlite3.connect("/home/evanlau/dc-bot/word_count.db")
            for i in db.execute(f'''SELECT Msg_count from Count where ID = {message.author.id} and Guild = {message.guild.id}'''):
                tmp = str(i[0])
            await message.reply(f"您目前在{message.guild.name}總共說過的字數為:{i[0]}")
            return

        if 'test' == tmp[1]:
            buttons = [
                manage_components.create_button(
                    style=ButtonStyle.green,
                    label="測試"
                ),
            ]
            action_row = manage_components.create_actionrow(*buttons)
            await message.delete()
            await message.channel.send('按鈕測試', components=[action_row])
            i = cycle(
                ['測試!', '🤔', '<:emoji_think:902897966304591883>', '按爽沒', 'SUS', '😡'])
            for temp in i:
                button_message = await manage_components.wait_for_component(bot, components=action_row)
                await button_message.edit_origin(content=temp)

        if 'one' == tmp[1]:
            buttons = [
                manage_components.create_button(
                    style=ButtonStyle.green,
                    label="+1"
                ),
            ]
            action_row = manage_components.create_actionrow(*buttons)
            await message.delete()
            await message.channel.send('0', components=[action_row])
            i = 1
            while True:
                button_message = await manage_components.wait_for_component(bot, components=action_row)
                await button_message.edit_origin(content=i)
                i = i + 1

        if 'CInvite' == tmp[1]:
            if str(message.author.id) == '540134212217602050':
                tmp = message.content.split(" ")
                channel = bot.get_channel(int(tmp[2]))
                link = await channel.create_invite()
                await message.channel.send(link)
                print(link)
                return
            else:
                await message.reply(f'<@!540134212217602050>，<@{str(message.author.id)}>在亂玩指令')
                return

        if 'addrole' == tmp[1]:
            if str(message.author.id) == '540134212217602050':
                tmp = message.content.split(" ")
                temp = message.guild.get_member(message.author.id)
                await temp.add_roles(message.guild.get_role(int(tmp[2])))
                print(temp)
                return
            else:
                await message.reply(f'<@!540134212217602050>，<@{str(message.author.id)}>在亂玩指令')
                return

        if 'removerole' == tmp[1]:
            if str(message.author.id) == '540134212217602050':
                tmp = message.content.split(" ")
                temp = message.guild.get_member(message.author.id)
                await temp.remove_roles(message.guild.get_role(int(tmp[2])))
                print(temp)
                return
            else:
                await message.reply(f'<@!540134212217602050>，<@{str(message.author.id)}>在亂玩指令')
                return

        if 'calendar' == tmp[1]:
            await message.channel.send('日曆女裝！')
            await message.delete()
            return

    if message.content == '嗨':
        await message.content.reply(f'早安啊,{name}王子先生', mention_author=True)
        return

    if message.content == '早安' or message.content == '午安' or message.content == '晚安':
        await message.reply(conversation.feedback(message.content))
        return

    if 'rick' in message.content:
        await message.channel.send('有人提到rickroll嗎😀?')
        await message.channel.send('<a:wellow_guy:910197305540481056>')
        return
    else:
        conv = str(message.content)
        conv = conversation.gif(conv)
        count.word_count(name=str(message.author), id=int(message.author.id), guild=int(message.guild.id), message=str(message.content))
        if conv == False:
            return
        else:
            await message.channel.send(conv)
            return


@bot.event
async def on_voice_state_update(member, before, after):
    await asyncio.sleep(0.5)
    ChName = ['的自閉小黑屋', '的語音頻道', '的秀肌肉專區', '的直播間', '大佬在此🛐', '的線上賭場開張囉']
    name = member.name.split('#', 2)
    try:
        channelID = after.channel.id
        DV = open('/home/evanlau/dc-bot/channelID/DV_ChannelID.txt', 'r')
        temp = eval(DV.read())
        DV.close()
        print('使用者目前頻道:', after.channel.name, after.channel.id)
        if str(after.channel.id) in str(temp):
            for i in temp:
                if int(i) == int(channelID):
                    print("trigger DVchannel", channelID)
                    channel = bot.get_channel(int(i))
                    channelID = await member.guild.create_voice_channel(name=f'{name[0]}{random.choice(ChName)}', overwrites=None, category=channel.category, reason=None)
                    print(channelID)
                    await member.move_to(channelID)
                    f = open(
                        '/home/evanlau/dc-bot/channelID/V_ChannelID.txt', 'r')
                    temp = eval(f.read())
                    f.close()
                    temp.append(str(channelID.id))
                    f = open(
                        '/home/evanlau/dc-bot/channelID/V_ChannelID.txt', 'w')
                    f.write(str(temp))
                    f.close()
                    print(name[0], '創建成功')
                    raise ValueError("ERROR")
        else:
            raise ValueError("ERROR")
    except:
        print("trigger cancel channel")
        path = '/home/evanlau/dc-bot/channelID/V_ChannelID.txt'
        f = open(path, 'r')
        temp = eval(f.read())
        f.close()
        for i in temp:
            if int(i) == int(before.channel.id):
                channel = bot.get_channel(before.channel.id)
                members = channel.members
                if len(members) == 0 or len(members) == 1 and str(909796683418832956) in str(members):
                    channeltemp = await channel.delete()
                    print(channeltemp)
                    temp.remove(str(i))
                    t = open(path, 'w')
                    t.write(str(temp))
                    t.close()
                    print(f'{channel}刪除成功')


@bot.event
async def on_ready():
    change_status.start()
    print(f'目前登入身份：{bot.user}')
    global conn
    conn = sqlite3.connect("/home/evanlau/dc-bot/channelID/ChannelID.db")

bot.run(token)


'''@slash.slash(name="vcset",description="設定指定的頻道為動態語音創建用文字頻道")
async def vcset(message):
  conversation.print_cmd(message,'vcset')
  if message.author.guild_permissions.manage_channels or str(message.author.id) == '540134212217602050':
    id=str(message.channel.id)
    c = open('/home/evanlau/dc-bot/channelID/T_ChannelID.txt', 'r')
    temp = eval(c.read())
    c.close()
    if str(id) in str(temp):
      await message.send('此頻道已登記')
      return
    channel = bot.get_channel(int(id))
    if channel != None:
      f = open('/home/evanlau/dc-bot/channelID/T_ChannelID.txt', 'w')
      temp.append(str(id))
      f.write(str(temp))
      f.close()
      await message.send(f'已設定{channel.name}為動態語音產生頻道')
      return
    else:
      await message.send('未找到此頻道')
      return
  else:
    await message.send('您沒有權限執行此操作')
    return'''
